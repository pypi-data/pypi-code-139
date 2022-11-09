"""
None of the existing empirical models perfectly describes the training data. More
specifically, at the end of the training, the measurement uncertainties do not explain
the dispersion of the residuals at the fitted model.
This means that there is variability from SN to SN,
bearing on the shape of the light curves, or on the spectral structure that cannot be
captured by a two parameter model.
It is therefore essential to model this intrinsic residual variability of SNe by an
error model. This one is an empirical function of the phase and the wavelength. It
depends on parameters that must be adjusted during the training procedure.

In this study, we have implemented a simple error model, as a proof of concept.
of concept. It includes a purely diagonal part (error snake), as well as a non-diagonal
part, which describes a specific error mode (color scatter) observed on the training.
"""

import numpy as np
import pylab as pl
from scipy.sparse import coo_matrix, dia_matrix, csc_matrix
from ..lib.bspline import BSpline, CardinalBSplineC, integ, BSpline2D, lgram
from ..lib.fitparameters import FitParameters
try:
    from sksparse.cholmod import cholesky_AAt
except ImportError:
    from scikits.sparse.cholmod import cholesky_AAt


class ColorScatter(object):
    r"""
    To model the residual variability of the SNe color not described by the model, we allow the relative amplitude of
    each light curve to vary by a quantity :math:`(1+kappa)`:

    .. math::
        \phi_{phot}(p_0) = X_0 (1+z) (1+kappa) \int S(\lambda, p) T\left( \lambda \right) \frac{\lambda}{hc} d\lambda

    where :math:`\kappa` is an additional parameter, depending on the SN and the observation band.

    The variability of :math:`\kappa` is defined by a centered Gaussian a priori and whose variance depends on the
    wavelength restframe, and must be determined during the adjustment.
    In our model, this term is implemented by a polynomial of the wavelength restframe of the SN. For a light curve
    observed in a band :math:`X`, of average wavelength :math:`\lambda^X`, the corresponding variance is:

    .. math::
        \sigma_\kappa^2 = P\left(\frac{\lambda^X}{1+z}\right)

    where :math:`z` is redshift of the supernova and :math:`P` is a polynomial of the wavelength restframe.
    In practice, :math:`P` is implemented in terms of a reduced restframe wavelength: :math:`\lambda_{r}`

    Attributes
    ----------
    WL_REDUCED : numpy.array
        Reduced SN-restframe mean wavelength
    pars : nacl.lib.fitparameters.FitParameters
        Color scatter parameter.
    """
    U_WAVELENGTH = 3650.88
    B_WAVELENGTH = 4302.57
    V_WAVELENGTH = 5428.55
    R_WAVELENGTH = 6418.01
    I_WAVELENGTH = 7968.34
    WAVELENGTH = {"U": U_WAVELENGTH, "B": B_WAVELENGTH, "V": V_WAVELENGTH,
                  "R": R_WAVELENGTH, "I": I_WAVELENGTH}

    def __init__(self, wavelength_rest_reduced, sigma_kappa):
        """
        Constructor - computes the arguments

        Parameters
        ----------
        wavelength_rest_reduced :
            Reduced SN-restframe mean wavelength
        sigma_kappa : numpy.array
            Color scatter parameter initialisation.
        """
        self.WL_REDUCED = wavelength_rest_reduced
        self.pars = self.init_pars(sigma_kappa)

    @staticmethod
    def init_pars(sigma_kappa):
        """
        Parameters initialisation.

        Parameters
        ----------
        sigma_kappa : numpy.array
            Color scatter parameter initialisation.

        Returns
        -------
        pars : nacl.lib.fitparameters.FitParameters
            Color scatter parameter.
        """
        pars = FitParameters([('sigma_kappa', len(sigma_kappa))])
        pars['sigma_kappa'] = sigma_kappa
        return pars
        
    def __call__(self, sk, jac=False):
        """
        Evaluate the color scatter.

        Parameters
        ----------
        sk : numpy.array
            Color scatter parameter

        Returns
        -------
        val : numpy.array
            Color scatter evaluation, square root of the diagonal term of the color scatter 
            matrix.
        if jac:
            jacobian of the color scatter.
        """
        self.pars.free = sk
        sigma_kappa = self.pars.full[:]
        val = np.polyval(sigma_kappa, self.WL_REDUCED)  # * self.WL_REDUCED
    
        if jac:
            vander = (np.vander(self.WL_REDUCED, len(sigma_kappa)).T )  # * self.WL_REDUCED)
            jj = (vander * val * 2).T
            return val, jj  # coo_matrix(jj)
        return val


class SimpleVarianceModel(object):
    r"""
    Implementation of the error snake,  residuals variability coming from SN Ia variability
    not modeled and instrumental uncertainty not took into account.
    The diagonal part of the error model (error snake) can be understood as the contribution
    of the higher order terms of the PCA, having been truncated.

    Variance model, function of the flux both for photometry and spectroscopy
    (indiscriminately represented by X)

    .. math::
    V(\lambda, p) = \sigma_{Err}^2 + \sigma_{\mathrm{Mod}}^2(\lambda,p)

    where :

    .. math::
        \sigma_{\mathrm{Mod}}^{spec} &= g(\lambda, p) \times \phi_{\mathrm{spec}}(p,\lambda)\ \ (\mathrm{spectra}) \\
        \sigma_{\mathrm{Mod}}^{phot} &= g(\lambda, p) \times \phi_{\mathrm{phot}}(p,\lambda)\ \ (\mathrm{photometric})

    :math:`\gamma(\lambda, p)` is a global surface describing the spectral residual of
    a 2D spline surface defined on the same ranges as the corresponding model.


    Attributes
    ----------
    disconnect_sp : bool
        Whether error snake of spectral data is considered.
    model : nacl.salt
        Model.
    sp : nacl.dataset.SpectrumData
        Spectral data
    lc : nacl.dataset.LcData
        Photometric data
    filter_db : nacl.instruments.FilterDb
        Filter transmission projected on B-splines
    bands : numpy.array
        Bands used for photometric data
    threshold : int
        Fix the spline parameters for bin that gather less data points than this threshold value.
    wl_grid : numpy.array
        Wavelength grid.
    phase_grid : numpy.array
        Phase grid.
    basis : nacl.lib.bspline.BSpline2D
        2D spline basis.
    factor_int : float
        Model normalisation.
    lambda_c : numpy.array
        Mean wavelength of the filter in the SN-restframe.
    pars : nacl.lib.fitparameters.FitParameters
        Parameters :math:`\gamma`.
    pars0 : numpy.array
        Parameters used to initialize the error snake.
    """
    def __init__(self, model, gamma_init=0.01,  disconnect_sp=False, threshold=None,
                 adaptative_grid=False, bins=(3, 3), order=4):
        r"""
        Constructor.
        - instantiate the bases (phase, wavelength)
        - compute the \lambda_c for each light curve
        - initiate the parameters
        

        Parameters
        ----------
        model : nacl.salt
            Model.
        gamma_init : numpy.array ou float
            Parameters used to initialize the error snake.
        disconnect_sp : bool
            Whether error snake of spectral data is considered.
        threshold : int
            Fix the spline parameters for bin that gather less data points than this threshold value.
        adaptative_grid : bool
            It true, define Bspline knots where parameter space has data.
        bins : tuple
            Number of bins if the grid is not adaptative.
        order :
            Spline order.
        """
        self.disconnect_sp = disconnect_sp
        
        self.model = model
        self.lc = self.model.training_dataset.lc_data
        self.sp = self.model.training_dataset.spec_data
        self.filter_db = self.model.filter_db
        self.bands = self.model.bands
        self.threshold = threshold
        
        ph_bin, wl_bin = bins
        order = order

        if adaptative_grid:
            phase_lc = self.model.get_restframe_phases(self.lc)
            phase_sp = self.model.get_restframe_phases(self.sp)
            wavelength_lc = self.lc['Wavelength']/(1 + self.lc['ZHelio'])
            wavelength_sp = self.sp['Wavelength']/(1 + self.sp['ZHelio'])
            phase = np.hstack((phase_sp, phase_lc))
            wavelength = np.hstack((wavelength_sp, wavelength_lc))
            _, self.wl_grid, self.phase_grid, _ = pl.hist2d(wavelength, phase, bins=2)

        else:
            
            print(f'\n VarModel N bins : ph : {ph_bin}, wl {wl_bin}')
            self.phase_grid = np.linspace(model.basis.by.range[0], model.basis.by.range[-1], ph_bin)
            self.wl_grid = np.linspace(model.basis.bx.range[0], model.basis.bx.range[-1], wl_bin)

        self.basis = BSpline2D(self.wl_grid, self.phase_grid,
                               x_order=order,
                               y_order=order)
        
        self.factor_int = self.model.norm
        if self.lc['Wavelength'].sum() == 0:
            filter_mean_wl = [self.model.filter_db.transmission_db[bd].mean() for bd in self.model.bands.astype(str)]
            self.lambda_c = np.array(filter_mean_wl)[self.lc['band_id']]/(1+self.lc['ZHelio']) 
        else:
            self.lambda_c = self.lc['Wavelength']/(1+self.lc['ZHelio'])

        self.pars = self.init_pars(gamma_init=gamma_init)
        self.pars0 = self.pars.full.copy()

    def fix_non_constrain_pars(self, threshold):
        """
        Return index of parameters of the parameter space that don't have enough data to constraint the error snake.

        Parameters
        ----------
        threshold : int
            Threshold value defining the "enough". If the sum of the data in a bin is less than this value,
            the corresponding parameter is fixed.

        Returns
        ----------
        idx : numpy.array
            Index of parameters that will be fixed.
        """
        lcs = self.model.training_dataset.lc_data
        sps = self.model.training_dataset.spec_data
        ph_sp = self.model.get_restframe_phases(sps)
        ph_lc = self.model.get_restframe_phases(lcs)
        wl_sp = sps['Wavelength']/(1 + sps['ZHelio'])
        wl_lc = lcs['Wavelength']/(1 + lcs['ZHelio'])

        x = np.hstack((wl_sp, wl_lc))
        y = np.hstack((ph_sp, ph_lc))
        jj = self.basis.eval(x, y)

        idx = np.where(np.bincount(np.sort(jj.col)) < threshold)
        return idx[0] 

    def init_pars(self, gamma_init):
        """
        Initiate model parameters.

        Parameters
        ----------
        gamma_init : float
            Parameters used to initialize the error snake.

        Returns
        ----------
        gamma : nacl.lib.fitparameters.FitParameters
            Parameters :math:`\gamma`.
        """
        gamma = FitParameters([('gamma', self.basis.bx.nj * self.basis.by.nj)])
        gamma['gamma'] = gamma_init
        if self.threshold is not None:
            idx = self.fix_non_constrain_pars(self.threshold)
            print(idx)
            print(gamma.free.shape)
            gamma.fix(idx)
            print(gamma.free.shape)
        return gamma
                    
    def __call__(self, gamma, beta, jacobian=None, debug_mode=False, lc=None, sp=None):
        r"""
        Evaluate the model for a set of parameter :math:`\gamma` (variance model parameters)
        and :math:`\beta` (flux model parameters).
        

        Parameters
        ----------
        gamma : np.array
           set of parameter of the variance model;
        beta : np.array
           set of parameter of the flux model;
        jacobian : None or scipy.sparse.coo_matrix
           derivative of the flux, not necessary if derivative of variance model not needed,
        debug_mode : bool
           to get some variables...
        lc : nacl.dataset.LcData
           to get variance model of a set of light curve and is None will get for all
        sp : nacl.dataset.SpectrumData
           to get variance model of a set of spectra and is None will get for all

        Returns
        ----------
        var : numpy.array
            Variance value of the model, quadratic sum of the error measurement and the error snake.
        if jacobian is not None:
        var : numpy.array
            Variance value of the model, quadratic sum of the error measurement and the error snake.
        jacobian_var : scipy.sparse.coo_matrix
            Jacobian (derivatives wrt :math:`\beta` and :math:`\gamma`)matrix of the error model.
        """
        if lc is None:
            lc = self.lc
        if sp is None:
            sp = self.sp
        lambda_c = self.lambda_c[lc['i']]

        self.model.pars.free = beta
        flux = self.model(beta, jac=False)
        self.pars.full[:] = gamma

        phase_lc = (lc['Date']-self.model.pars['tmax'].full[lc['sn_id']])/(1+lc['ZHelio'])
        phase_sp = (sp['Date']-self.model.pars['tmax'].full[sp['sn_id']])/(1+sp['ZHelio'])

        if self.disconnect_sp:
            sigma_spectra = np.zeros_like(phase_sp)
        else:
            wl_sp = np.array(sp['Wavelength'])/(1+sp['ZHelio'])
            spline_sp = self.basis.eval(wl_sp, phase_sp)
            flux_sp = flux[sp['i']]
            ss_sp = (spline_sp * self.pars['gamma'].full)
            sigma_spectra = ss_sp * flux_sp

        spline_lc = self.basis.eval(lambda_c, phase_lc)
        flux_lc = flux[lc['i']] 
        ss_lc = (spline_lc * self.pars['gamma'].full)
        sigma_lightcurve = ss_lc * flux_lc
        sig = np.hstack((sigma_lightcurve, sigma_spectra))
        flux_err = np.hstack((lc['FluxErr'], sp['FluxErr']))
        var = sig**2 + flux_err**2 
        
        if jacobian is not None:
            n_pars, n_data = len(self.model.pars.free) + len(self.pars.free), len(sig)
            v, jacobian = self.model(beta, jac=True)

            if self.disconnect_sp:
                i_dp, j_dp, jacobian_pars, i_dg0, j_dg0, jacobian_gamma = [], [], [], [], [], []
            else:
                jacobian_spectra = jacobian.tocsc()[sp['i']].tocoo()
                # dp
                i_dp = jacobian_spectra.row.copy()
                j_dp = jacobian_spectra.col.copy()
                jacobian_pars = 2 * jacobian_spectra.data * (sigma_spectra * ss_sp)[i_dp]
                
                # dtmax
                idx = self.model.pars['tmax'].indexof(sp['sn_id'])
                jacobian_wrt_phase, jacobian_wrt_wavelength = self.basis.gradient(wl_sp,
                                                                                  phase_sp + self.model.delta_phase)
                if len(jacobian_pars) != 0.:
                    jacobian_pars[idx] -= 2 * (jacobian_wrt_phase * self.pars['gamma'].full) / \
                                          (1+sp['ZHelio']) * v[sp['i']] * sigma_spectra
                # dg
                i_dg0 = spline_sp.row.copy()
                j_dg0 = self.pars['gamma'].indexof(spline_sp.col) + len(self.model.pars.free)
                jacobian_gamma = 2 * v[sp['i']][i_dg0]**2 * spline_sp.data * ss_sp[i_dg0]
                if debug_mode:
                    return i_dp, j_dp, jacobian_pars, i_dg0, j_dg0, jacobian_gamma, v, sp, spline_sp, ss_sp

            v_lc = v[lc['i']]
            jacobian_lightcurve = jacobian.tocsc()[lc['i']].tocoo()
            
            i_dp_lc = jacobian_lightcurve.row.copy()
            j_dp_lc = jacobian_lightcurve.col.copy()
            jacobian_pars_lightcurve = 2 * jacobian_lightcurve.data * (sigma_lightcurve * ss_lc)[i_dp_lc]
            
            # dtmax
            if self.model.pars['tmax'].indexof().sum() != len(self.model.pars['tmax'].full) * -1:
                jacobian_wrt_phase, jacobian_wrt_wavelength = self.basis.gradient(lambda_c,
                                                                                        phase_lc +
                                                                                        self.model.delta_phase)
                idx_lc = np.where(np.in1d(jacobian_lightcurve.col, self.model.pars['tmax'].indexof()))
                if len(jacobian_pars_lightcurve) != 0.:
                    jacobian_pars_lightcurve[idx_lc] -= 2 * (jacobian_wrt_phase * self.pars['gamma'].full) / (1+lc['ZHelio']) * v_lc * sigma_lightcurve
                
            # dg
            i_dg0_lc = spline_lc.row.copy()
            j_dg0_lc = self.pars['gamma'].indexof(spline_lc.col) + len(self.model.pars.free)
            jacobian_gamma_lightcurve = 2 * v_lc[i_dg0_lc] ** 2 * spline_lc.data * ss_lc[i_dg0_lc]
            
            if len(i_dg0) != 0:
                i_dg0 += len(lc)
            if len(i_dp) != 0:
                i_dp += len(lc)
            
            i = np.hstack((i_dp, i_dg0, i_dp_lc, i_dg0_lc))
            j = np.hstack((j_dp, j_dg0, j_dp_lc, j_dg0_lc))
            val = np.hstack((jacobian_pars, jacobian_gamma, jacobian_pars_lightcurve, jacobian_gamma_lightcurve))
             
            idx_zeros = np.where((j != -1))[0]
            jacobian_var = coo_matrix((val[idx_zeros], (i[idx_zeros], j[idx_zeros])), shape=(n_data, n_pars))

            return var, jacobian_var.T
        return var
