from typing import Dict, Optional
from evofr.data.data_spec import DataSpec
import jax.numpy as jnp
from jax.nn import logsumexp
import numpy as np

from evofr.models.model_spec import ModelSpec
from .basis_functions import BasisFunction, Spline

from .LAS import LaplaceRandomWalk
from .model_functions import forward_simulate_I, reporting_to_vec
from .model_options import NegBinomCases

import numpyro
import numpyro.distributions as dist


def tent_kinetics(ages, to, tp, tr, height, lod):
    return jnp.piecewise(
        ages,
        condlist=[
            ages <= to,
            (to < ages) * (ages <= tp),
            (tp < ages) * (ages <= tr),
            ages > tr,
        ],
        funclist=[
            lambda a: lod * jnp.ones(a.shape),
            lambda a: lod + (height / (tp - to)) * (a - to),
            lambda a: lod + height - (height / (tr - tp)) * (a - tp),
            lambda a: lod * jnp.ones(a.shape),
        ],
    )


def expected_ct(D_max):
    # Sample paramters
    height = numpyro.sample("height", dist.Normal(-20.0))
    to = numpyro.sample("to", dist.Normal(loc=0.5, scale=0.01))
    delta_tp = numpyro.sample("delta_tp", dist.Normal(loc=4.0, scale=0.01))
    delta_tr = numpyro.sample("delta_tr", dist.Normal(loc=6.0, scale=0.01))
    tp = numpyro.deterministic("tp", to + delta_tp)
    tr = numpyro.deterministic("tr", delta_tr + tp)

    # Compute age_ct from tent function
    ages = jnp.arange(D_max)
    ect = tent_kinetics(ages, to, tp, tr, height, lod=40)
    return ect


def ct_likelihood(values, times, prev, D_max, pred=False):
    # At each time compute the empirical age distribution
    unique_times = np.unique(times)
    possible_times = unique_times - np.arange(D_max)[:, None]
    age_dist = prev[possible_times].at[possible_times < 0].set(0.0)

    # Make sure negative times don't ruin things
    age_dist = age_dist / age_dist.sum(axis=0)  # Average across all delays
    numpyro.deterministic("age_dist", age_dist)

    # Get expected CT by age
    ECT = numpyro.deterministic("expected_ct", expected_ct(D_max))

    numpyro.deterministic("expected_ct_obs", jnp.einsum("dt, d -> t", age_dist, ECT))

    # CT model: Can reframe with mixture same family
    with numpyro.plate("age_sigma", D_max):
        sigma = numpyro.sample("sigma", dist.Exponential(1.0))
    # log_prob = dist.Gumbel(ECT, sigma).logprob(values) + jnp.log(age_dist)
    # numpyro.factor("CT_prob", logsumexp(log_prob, axis=-1).sum())

    mixing_dist = dist.Categorical(probs=age_dist[:, times].T)
    component_dist = dist.TruncatedNormal(loc=ECT, scale=sigma, high=40., low=0.0)
    obs = None if pred else values
    numpyro.sample(
        "CT", dist.MixtureSameFamily(mixing_dist, component_dist), obs=obs
    )


def ct_renewal_factory(
    g_rev,
    delays,
    seed_L,
    forecast_L,
    CaseLik=None,
):
    if CaseLik is None:
        CaseLik = NegBinomCases()

    def _model(cases, ct_values, ct_times, X, pred=False):
        # Unpacking arguments
        T, k = X.shape
        obs_range = jnp.arange(seed_L, seed_L + T, 1)

        # Effective Reproduction number likelihood
        gam = numpyro.sample("gam", dist.HalfNormal(1.0))
        beta_0 = numpyro.sample("beta_0", dist.Normal(0.0, 1.0))
        beta_rw = numpyro.sample(
            "beta_rw", LaplaceRandomWalk(scale=gam, num_steps=k)
        )
        beta = beta_0 + beta_rw
        _R = numpyro.deterministic("R", jnp.exp(X @ beta))

        # Add forecasted values of R
        R = _R
        if forecast_L > 0:
            R_forecast = numpyro.deterministic(
                "R_forecast", jnp.vstack((_R[-1],) * forecast_L)
            )
            R = jnp.concatenate((_R, jnp.squeeze(R_forecast)))

        # Getting initial conditions
        I0 = numpyro.sample("I0", dist.Uniform(0.0, 300_000.0))
        intros = jnp.zeros((T + seed_L + forecast_L,))
        intros = intros.at[np.arange(seed_L)].set(I0 * jnp.ones(seed_L))

        # Generate day-of-week reporting fraction
        with numpyro.plate("rho_parms", 7):
            rho = numpyro.sample("rho", dist.Beta(5.0, 5.0))
        rho_vec = reporting_to_vec(rho, T)

        I_prev = jnp.clip(
            forward_simulate_I(intros, R, g_rev, delays, seed_L),
            a_min=1e-12,
            a_max=1e25,
        )

        # Smooth trajectory for plotting
        numpyro.deterministic(
            "I_smooth", jnp.mean(rho_vec) * jnp.take(I_prev, obs_range, axis=0)
        )

        # Compute growth rate assuming I_{t+1} = I_{t} \exp(r_{t})
        numpyro.deterministic(
            "r",
            jnp.diff(
                jnp.log(jnp.take(I_prev, obs_range, axis=0)),
                prepend=jnp.nan,
                axis=0,
            ),
        )

        # Given I_smooth, compute likelihood of Ct values

        # Do we want to pass in seed values as well? Yes, this will require some edits tho.
        ct_likelihood(
            ct_values,
            ct_times,
            jnp.take(I_prev, obs_range, axis=0),
            D_max=20,
            pred=pred,
        )

        # Compute expected cases
        numpyro.deterministic(
            "total_smooth_prev",
            jnp.mean(rho_vec) * jnp.take(I_prev, obs_range),
        )
        EC = numpyro.deterministic("EC", jnp.take(I_prev, obs_range) * rho_vec)

        # Evaluate case likelihood
        CaseLik.model(cases, EC, pred=pred)

    return _model


class CTRenewalModel(ModelSpec):
    def __init__(
        self,
        g,
        delays,
        seed_L: int,
        forecast_L: int,
        k: Optional[int] = None,
        CLik=None,
        basis_fn: Optional[BasisFunction] = None,
    ):
        self.g_rev = jnp.flip(g, axis=-1)
        self.delays = delays
        self.seed_L = seed_L
        self.forecast_L = forecast_L

        # Making basis expansion for Rt
        self.k = k if k else 10
        self.basis_fn = (
            basis_fn if basis_fn else Spline(s=None, order=4, k=self.k)
        )

        # Defining model likelihoods
        self.CLik = CLik
        self.make_model()

    def make_model(self):
        self.model_fn = ct_renewal_factory(
            self.g_rev,
            self.delays,
            self.seed_L,
            self.forecast_L,
            self.CLik,
        )

    def augment_data(self, data):
        # Add feature matrix for parameterization of R
        data["X"] = self.basis_fn.make_features(data, T=data["cases"].shape[0])


class CTData(DataSpec):
    def __init__(self):
        pass

    def make_data_dict(self, data: Optional[Dict] = None):
        if data is None:
            data = dict()
        return data
