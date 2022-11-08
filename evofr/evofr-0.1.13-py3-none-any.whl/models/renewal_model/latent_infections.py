from functools import partial
import jax.numpy as jnp
import numpy as np
from jax import jit, vmap, lax
from numpyro.contrib.control_flow import scan
import numpyro
import numpyro.distributions as dist
from .model_functions import _apply_delays, reporting_to_vec
from .model_options import GARW, NegBinomCases, DirMultinomialSeq


# def get_latent_infections(m, R, g_rev, seed_L, sigma_I):
#     max_age = len(g_rev)
#
#     def transition_fn(infections, xs):
#         R, im = xs
#         latent_I = numpyro.sample(
#             "latent_I",
#             dist.Normal(R * jnp.dot(infections, g_rev) + im, sigma_I),
#         )
#         return jnp.append(infections[-(max_age - 1) :], latent_I), latent_I
#
#     _, infections = lax.scan(
#         transition_fn,
#         init=jnp.zeros(max_age),
#         xs=(jnp.pad(R, (seed_L, 0), constant_values=1.0), m),
#     )
#     return infections
#
#
# @partial(jit, static_argnums=4)
# def forward_simulate_latent(m, R, gen_rev, delays, seed_L, sigma_I):
#     infections = get_latent_infections(m, R, gen_rev, seed_L, sigma_I)
#     infections, _ = lax.scan(_apply_delays, init=infections, xs=delays)
#     return infections


def simulate_latent_by_variant(m, R, g_rev, delays, seed_L, sigma_I):
    max_time, num_variants = R.shape
    max_age = g_rev.shape[-1]
    R_padded = jnp.vstack(
        (jnp.ones((seed_L, num_variants)), R)
    )

    def transition_fn(infections, ts):
        infectivity = jnp.einsum("dv, vd -> v", infections, g_rev)
        # latent_I = numpyro.sample(
        #     "latent_I",
        #     dist.Normal(
        #         (R_padded[ts, :] * infectivity) + m[ts,:],
        #         scale=sigma_I * 1e-10),
        # )
        latent_I = (R_padded[ts, :] * infectivity) + m[ts,:]

        # Add errors
        # latent_err = numpyro.sample("latent_error", dist.Normal(latent_I, sigma_I))
        # latent_I = numpyro.sample("latent_I", latent_err + latent_I)

        return jnp.vstack((infections[-(max_age-1):, :], latent_I)), latent_I

    _, infections = scan(
        transition_fn,
        init=jnp.zeros((max_age, num_variants)),
        xs=jnp.arange(max_time + seed_L)
    )

    delay_by_variant = vmap(
        lambda infect: lax.scan(_apply_delays, init=infect, xs=delays)[0],
        in_axes=-1,
        out_axes=-1
    )

    return jnp.squeeze(delay_by_variant(infections))


def _latent_renewal_model_factory(
    g_rev,
    delays,
    seed_L,
    forecast_L,
    RLik=None,
    CaseLik=None,
    SeqLik=None,
    v_names=None,
):
    if RLik is None:
        RLik = GARW()
    if CaseLik is None:
        CaseLik = NegBinomCases()
    if SeqLik is None:
        SeqLik = DirMultinomialSeq()

    # If single generation time
    if g_rev.ndim == 1:
        gmap_dim = None  # Use same generation time
    else:
        gmap_dim = 0  # Use each row
        # Specifying variant name map to column
        if v_names is not None:
            which_col = {s: i for i, s in enumerate(v_names)}

    def _variant_model(cases, seq_counts, N, X, var_names, pred=False):
        T, N_variant = seq_counts.shape
        obs_range = jnp.arange(seed_L, seed_L + T, 1)

        # Computing first introduction dates
        first_obs = (np.ma.masked_invalid(np.array(seq_counts)) != 0).argmax(
            axis=0
        )
        intro_dates = np.concatenate(
            [first_obs + d for d in np.arange(0, seed_L)]
        )
        # intro_idx = (first_obs, np.arange(N_variant)) # Single introduction
        intro_idx = (
            intro_dates,
            np.tile(np.arange(N_variant), seed_L),
        )  # Multiple introductions

        _R = RLik.model(
            N_variant, X
        )  # likelihood on effective reproduction number

        # Add forecasted R
        if forecast_L > 0:
            R_forecast = numpyro.deterministic(
                "R_forecast", jnp.vstack((_R[-1, :],) * forecast_L)
            )
            R = jnp.vstack((_R, R_forecast))
        else:
            R = _R

        # Getting initial conditions
        intros = jnp.zeros((T + seed_L + forecast_L, N_variant))
        # I0_scale = numpyro.sample("I0_scale", dist.HalfNormal(100))
        with numpyro.plate("N_variant", N_variant):
            I0 = 300_000.0 * numpyro.sample("I0", dist.Uniform())
            # I0 = numpyro.sample("I0", dist.LogNormal(jnp.log(300_000), scale=I0_scale))
        intros = intros.at[intro_idx].set(jnp.tile(I0, seed_L))

        with numpyro.plate("rho_parms", 7):
            rho = numpyro.sample("rho", dist.Beta(5.0, 5.0))
        rho_vec = reporting_to_vec(rho, T)

        _g_rev = g_rev  # Assume we're using original g_rev
        if gmap_dim is not None:  # Match variants to correct generation time
            v_idx = [
                which_col[s] for s in var_names
            ]  # Find which variants present
            _g_rev = _g_rev[v_idx, :]

        # This is where we add latent part
        sigma_I = numpyro.sample("sigma_I", dist.HalfNormal(1.0))

        I_prev = jnp.clip(
            simulate_latent_by_variant(intros, R, _g_rev, delays, seed_L, sigma_I),
            a_min=0.0,
            a_max=None,
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

        # Compute expected cases
        total_prev = I_prev.sum(axis=1)
        numpyro.deterministic(
            "total_smooth_prev",
            jnp.mean(rho_vec) * jnp.take(total_prev, obs_range),
        )

        EC = numpyro.deterministic(
            "EC", jnp.take(total_prev, obs_range) * rho_vec
        )

        # Evaluate case likelihood
        CaseLik.model(cases, EC, pred=pred)

        # Compute frequency
        _freq = jnp.divide(I_prev, total_prev[:, None])
        freq = numpyro.deterministic(
            "freq", jnp.take(_freq, obs_range, axis=0)
        )

        SeqLik.model(
            seq_counts, N, freq, pred
        )  # Evaluate frequency likelihood

        numpyro.deterministic(
            "R_ave", (_R * freq).sum(axis=1)
        )  # Getting average R

        if forecast_L > 0:
            numpyro.deterministic("freq_forecast", _freq[(seed_L + T):, :])
            I_forecast = numpyro.deterministic(
                "I_smooth_forecast",
                jnp.mean(rho_vec) * I_prev[(seed_L + T):, :],
            )
            numpyro.deterministic(
                "r_forecast",
                jnp.diff(jnp.log(I_forecast), prepend=jnp.nan, axis=0),
            )

    return _variant_model
