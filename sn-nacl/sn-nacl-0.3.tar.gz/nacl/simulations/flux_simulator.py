import numpy as np
import pickle

from ..lib import bspline
from . import etc, reindex
from ..dataset import TrainingDataset


try:
    from sksparse.cholmod import cholesky_AAt
except ImportError:
    from scikits.sparse.cholmod import cholesky_AAt

NORM_SNSIM = 290090.4311080577


class Simulator(object):
    r"""
    From data generator model flux and error
    on measurements.

    Flux are created with SALT2.4
    Flux error come from different sources.
    For ideal simulation there are simulated, always constant  fraction of flux of spectral data.
    For LSST, flux error are calculated from an ETC, otherwise they are constant fraction of flux.

    .. math::
        \sigma^2 = \left\{
         \sigma_{Err}^2 + \sigma_{mod}^2 + \sigma_{seuil}^2 \quad for spectral data \\
        \sigma_{Err}^2 + \sigma_{mod}^2 + \sigma^2_{\eta} + \sigma_{\kappa}^2 + \sigma_{seuil}^2  \quad otherwise


    Return lc and sp array, with the conventional format.

    Attributes
    ----------
    model_func : nacl.models.salt.SALT2Like
        Model to generated data.
    degree : int
        Degree of the spectral recalibration polynomial function.
    normalization_band_name : str
        Band name for normalization of the model.
    init_from_salt2_file : str
        File salt2, created by script 'nacl.simulation.make_salt2_npz.py'.
    disconnect_sp :
        Whether spectral data are considered.

    variance_model_func : nacl.models.variancemodels
        Error snake model to add as a noise in the simulated data.
    gamma_init : numpy.array ou float
        Parameters used to initialize the error snake.
    seed : int
        Seed for cadence.

    CS : nacl.models.ColorScatter
        Model of the color scatter to add as a noise.

    sigma_kappa_init : numpy.array
        Color scatter parameters to add in simulation.
    eta_covmatrix : float or array
        Covariance of calibration uncertainty to add in simulation as a noise.

    sig_calib : float or numpy.array
        Dispersion of the :math:`\eta` parameters.

    kappa_init : numpy.array
        Color scatter parameter used in the simulation.

    color_scatter_eval : numpy.array
        Evaluation of color scatter for each light curve.
    kappa : numpy.array
        :math:`\kappa` drawn according to normal distribution of standard deviation equal to poly.

    sig : numpy.array
        Variance model evaluation (quadratic sum of measurement error and error snake).

    calib : numpy.array
        Value of :math:`\eta` of each light curve data point.
    eta_band : dict
        Value of :math:`\eta` parameters used model evaluation of the simulation distributed by centred
        gaussian of standard deviation equal to  sig_calib for each band.

    lambda_c : numpy.array
        Mean wavelength of the filter in the SN-restframe.

    lambda_c_red : numpy.array
        Reduced mean wavelength of the filter in the SN-restframe.

    data_generator : nacl.jla.generator or nacl.ideal.generator or nacl.k21.generator
        Cadence and SNe information.

    sigma_lc : numpy.array
        Dispersion of photometric data
    filterpath : str
        Path to the filters files repository in nacl.dev/data/
    Sne ; numpy.array
        SNe names
    lc : numpy.rec.array
        Light curves data with data_type as type.
    sp : numpy.rec.array
        Spectral data, with data_type as type.

    idx_sp : numpy.array
        Spectral data index cuts.
    idx_lc : numpy.array
        Photometric data index cuts.

    trainingDataset
    """
    def __init__(self, data_generator, model_func, variance_model_func, 
                 init_from_salt2_file, degree=3, normalization_band_name='SWOPE::B',
                 noise=True, seed=0, gamma_init=0.0001, sigma_kappa_init=None,
                 disconnect_sp=False, eta_covmatrix=None, color_scatter_func=None,
                 init_filename=None):
        r"""
        Constructor.

        Parameters
        ----------
        data_generator : nacl.jla.generator or nacl.ideal.generator or nacl.k21.generator
            Cadence and SNe information.
        model_func : nacl.models.salt.SALT2Like
            Model to generated data.
        variance_model_func : nacl.models.variancemodels
            Error snake model to add as a noise in the simulated data.
        degree : int
            Degree of the spectral recalibration polynomial function.
        normalization_band_name : str
            Band name for normalization of the model.
        init_from_salt2_file : str
            File salt2, created by script 'nacl.simulation.make_salt2_npz.py'.
        disconnect_sp :
            Whether spectral data are considered.
        noise : bool
            Whether error snake is considered in simulation.
        gamma_init : numpy.array ou float
            Parameters used to initialize the error snake.
        seed : int
            Seed for cadence.
        color_scatter_func : nacl.models.ColorScatter
            Model of the color scatter to add as a noise.
        sigma_kappa_init : numpy.array
            Color scatter parameters to add in simulation.
        eta_covmatrix : float or array
            Covariance of calibration uncertainty to add in simulation as a noise.
        init_filename : str
            If simulation is already stored somewhere.
        """
        self.model_func = model_func
        self.degree = degree
        self.seed = seed
        np.random.seed(self.seed)
        self.gamma_init = gamma_init

        self.sigma_kappa_init = sigma_kappa_init
        
        self.eta_covmatrix = eta_covmatrix
        self.init_from_salt2_file = init_from_salt2_file
        self.variance_model_func = variance_model_func
        self.normalization_band_name = normalization_band_name
        self.disconnect_sp = disconnect_sp

        self.sig_calib = None
        self.kappa = None
        
        if init_filename is not None:
            self.init_from_data(init_filename)
        else:
            self.sig, self.seed = None, None
            self.calib, self.eta_band, self.lambda_c_red, self.lambda_c, self.color_scatter_eval = None, None, None, None, None
            self.kappa_init, self.sigma_lc = None, None
            self.data_generator = data_generator
            try:
                self.data_generator.lsst_simu
            except AttributeError:
                self.data_generator.lsst_simu = False

            try:
                self.Sne = data_generator.Sne[np.unique(self.lc['sn_id'])]
            except AttributeError:
                self.Sne = None
            self.filterpath = self.data_generator.trainingDataset.filterpath
            self.model = self.model_func(self.data_generator.trainingDataset,
                                         init_from_salt2_file=None, spectrum_recal_degree=self.degree,
                                         normalization_band_name=self.normalization_band_name)
            
            self.sigma_kappa_init = sigma_kappa_init
            self.CS = None
            if (self.sigma_kappa_init is not None) & (color_scatter_func is not None):
                self.CS = color_scatter_func(self.model.lambda_c_red, self.sigma_kappa_init)
                
            self.model_pars_initialisation(self.init_from_salt2_file)

            self.lc = self.data_generator.trainingDataset.lc_data
            self.sp = self.data_generator.trainingDataset.spec_data

            self.idx_sp, self.idx_lc = self.data_cuts()
            self.lc, self.sp = self.lc[self.idx_lc], self.sp[self.idx_sp]
            
            self.snInfo = self.data_generator.snInfo[np.unique(self.lc['sn_id'])]
            
            self.recreate_model_from_new_data_set()

            if np.unique(self.lc['sn_id']).shape[0] != self.lc['sn_id'][-1]+1:
                raise ValueError('All lcs from a SN have been remove')

            self.make_data()
            print(f"LC: {self.lc['i'][-1]+1} should be {len(np.unique(self.lc['i']))}")
            print(f"SP: {self.sp['i'][-1]+1} should be {len(np.unique(self.sp['i']))}")
            self.recreate_model_from_new_data_set()

            print(f"LC: {self.lc['i'][-1]+1} should be {len(np.unique(self.lc['i']))}")
            print(f"SP: {self.sp['i'][-1]+1} should be {len(np.unique(self.lc['i']))+len(np.unique(self.sp['i']))}")

            if noise:
                self.variance_model = self.variance_model_func(self.model, gamma_init=self.gamma_init,
                                                               # kappa_init = self.kappa_init,
                                                               disconnect_sp=self.disconnect_sp)
                
                self.adding_noise()

        self.trainingDataset = TrainingDataset(self.lc, self.sp, self.snInfo,
                                               filterpath=self.filterpath)

    def adding_noise(self):
        """
        Add error snake to as a noise to the flux simulated.
        """
        var = self.variance_model(self.variance_model.pars.free, self.model.pars.free)
        sigma = np.sqrt(var)
        print("Adding noise \n")
        self.sig = np.random.normal(0, sigma)
        self.lc['Flux'] += self.sig[self.lc['i']]
        self.sp['Flux'] += self.sig[self.sp['i']]
        
    def recreate_model_from_new_data_set(self):
        """
        Recreate a model and initiated its parameters from new data set, where cuts were apply,
        and index (of light_curve, spectra, sn) have changed.
        """
        if self.kappa is not None:
            idx = np.unique(self.lc['lc_id']).copy()
            self.kappa = self.kappa[idx]
        
        self.lc['lc_id'] = reindex.reindex(self.lc['lc_id'])
        self.lc['band_id'] = reindex.reindex(self.lc['band_id'])
        self.sp['spec_id'] = reindex.reindex(self.sp['spec_id'])

        n_lc = len(self.lc['i'])
        n_sp = len(self.sp['i'])
        self.lc['i'] = np.arange(n_lc)
        self.sp['i'] = n_lc + np.arange(n_sp)

        ts = TrainingDataset(self.lc, self.sp, self.snInfo)
        self.model = self.model_func(ts, init_from_salt2_file=None,
                                     spectrum_recal_degree=self.degree,
                                     normalization_band_name=self.normalization_band_name)
        self.model_pars_initialisation(self.init_from_salt2_file)

    def model_pars_initialisation(self, filename):
        r"""
        Initiated model parameters, global parameters are salt2's.
        Sne parameters are taken from data_generator.snInfo.
        Photometric calibration parameters are zero and spectroscopic are 1 !!!

        Parameters
        ----------
        filename : str
            File salt2, created by script 'nacl.simulation.make_salt2_npz.py'.
        """
        self.model.pars['X0'].full[:] = self.data_generator.snInfo['x0']
        print(f"model init X1 {self.data_generator.snInfo['x1'].mean()}; {self.data_generator.snInfo['x1'].std()}")
        self.model.pars['X1'].full[:] = self.data_generator.snInfo['x1']
        self.model.pars['c'].full[:] = self.data_generator.snInfo['c']
        self.model.pars['tmax'].full[:] = self.data_generator.snInfo['tmax']

        if self.eta_covmatrix is not None:
            if self.sig_calib is None:
                if type(self.eta_covmatrix) == float:
                    self.sig_calib = np.sqrt(self.eta_covmatrix) * np.ones(len(self.model.bands))
                else:
                    self.sig_calib = np.sqrt(self.eta_covmatrix)
                eta = np.random.normal(0, self.sig_calib)
                self.eta_band = {self.model.bands[i]: eta_i for i, eta_i in enumerate(eta)}

            self.calib = [self.eta_band[bd] for bd in self.model.bands]
                
        else:
            self.calib = 0.
        self.model.pars['eta_calib'].full[:] = self.calib 

        self.lambda_c = self.model.lambda_c 
        self.lambda_c_red = self.model.lambda_c_red
        pcl = self.model.pars.full[self.model.pars['CL'].indexof()]
        cl_i, _ = self.model.color_law(self.lambda_c, pcl)
        
        if (self.kappa is None) & (self.sigma_kappa_init is not None):
            self.color_scatter_eval = self.CS(self.CS.pars.free)
            self.kappa = np.random.normal(0, self.color_scatter_eval)
            self.model.pars['kappa_color'].full[:] = self.kappa

        elif self.sigma_kappa_init is None:
            self.model.pars['kappa_color'].full[:] = 0.
            
        else:
            self.model.pars['kappa_color'].full[:] = self.kappa

        self.kappa_init = self.model.pars['kappa_color'].full[:].copy()
        f = np.load(filename)
        phase_grid = f['phase_grid']
        wl_grid = f['wl_grid']
        basis = bspline.BSpline2D(wl_grid, phase_grid, x_order=4, y_order=4)
        
        xx = np.linspace(wl_grid[0], wl_grid[-1], basis.bx.nj)
        yy = np.linspace(phase_grid[0], phase_grid[-1], basis.by.nj)
        
        x, y = np.meshgrid(xx, yy)
        x, y = x.ravel(), y.ravel()
        basis_eval = self.model.basis.eval(x, y)
        factor = cholesky_AAt(basis_eval.T, beta=1e-10)

        surface_0, surface_1, color_law = factor(basis_eval.T * f['M0']), factor(basis_eval.T * f['M1']), f['CL_pars']
        self.model.pars['M0'][:] = surface_0
        self.model.pars['M1'][:] = surface_1
        self.model.pars['CL'][:] = color_law
        self.model.norm = self.model.normalization(band_name=self.normalization_band_name)

    def make_photometric_sigma(self, sigmalc):
        r"""
        Make the photometric error measurement if the surveys is a simulation of LSST,
        it will use the error simulation of saunerie psf
        Else it used sigmalc, from Data generator.

        Parameters
        ----------
        sigmalc : float
            Part of the photometric flux to be the error measurements.
        """
        if self.data_generator.lsst_simu:
            zlc = self.lc['ZHelio']
            n_lc = len(zlc)
            exptime = np.zeros(n_lc)
            flux_sky = np.zeros(n_lc)
            seeing = np.zeros(n_lc)

            exptime[np.where(zlc > 0.4)[0]] = 600
            exptime[np.where(zlc <= 0.4)[0]] = 30

            lsst = etc.find('LSST')
            lsst.dump()
            for ib in range(len(lsst.data['band'])):
                idx = np.where(self.lc['Filter'] == lsst.data['band'][ib].encode('UTF-8'))[0]
                flux_sky[idx] = lsst.data['flux_sky'][ib]
                seeing[idx] = lsst.data['iq'][ib]

            band = np.array([i.decode('UTF-8') for i in self.lc['Filter']])
            
            variance = lsst.flux_variance(exptime=exptime, flux=self.lc['Flux']*NORM_SNSIM,
                                          skyflux=flux_sky, seeing=seeing,
                                          band=band)
            self.sigma_lc = np.sqrt(variance)/np.abs(self.lc['Flux']*NORM_SNSIM)
        else:
            if type(sigmalc) == np.ndarray:
                sigmalc = sigmalc[self.idx_lc]
            self.sigma_lc = sigmalc

    def make_data(self):
        r"""
        Create flux from the model evaluation.
        Measurement error are the product of the flux and
        the sigma array defined in the data_generator.
        """
        res = self.model(self.model.pars.free, jac=False)
        self.sp['Flux'] = res[len(self.lc):] 

        if type(self.data_generator.sigma_sp) == float:
            sig = self.data_generator.sigma_sp
        elif type(self.data_generator.sigma_sp) == np.ndarray:
            sig = self.data_generator.sigma_sp[self.idx_sp]
        
        self.sp['FluxErr'] = np.abs(sig * self.sp['Flux'])
        
        # Offset per SPs ... otherwise data point could be very low with sigma below...
        for isp in np.unique(self.sp['spec_id']):
            idx_sp = self.sp['spec_id'] == isp
            offset_sp = self.sp[idx_sp]['Flux'].max() * 5e-3  # 4
            self.sp['FluxErr'][idx_sp] = np.sqrt(self.sp['FluxErr'][idx_sp] ** 2 + offset_sp ** 2)

        if (np.isinf(self.sp['Flux']) ^ np.isinf(self.sp['FluxErr'])).sum() > 0:
            print('Inf in spectral flux set to zeros')
            idx_inf = np.where((np.isinf(self.sp['Flux']) ^ np.isinf(self.sp['FluxErr'])))[0]
            self.sp['Flux'][idx_inf] = 0.
            self.sp['FluxErr'][idx_inf] = 100.

        if (np.isnan(self.sp['Flux']) ^ np.isnan(self.sp['FluxErr'])).sum() > 0:
            print('NaN in spectral flux set to zeros')
            idx_nan = np.where((np.isnan(self.sp['Flux']) ^ np.isnan(self.sp['FluxErr'])))[0]
            self.sp['Flux'][idx_nan] = 0.
            self.sp['FluxErr'][idx_nan] = 100.
    
        self.sp = self.sp[self.sp['FluxErr'] != 100]
        self.lc['Flux'] = res[:len(self.lc)]  # lc_eval()
        
        self.make_photometric_sigma(self.data_generator.sigma_lc)
        self.lc['FluxErr'] = np.abs(self.sigma_lc) * np.abs(self.lc['Flux'])

        # Offset per LCs ... otherwise data point could be very low with sigma below...
        for ilc in np.unique(self.lc['lc_id']):
            idx_lc = self.lc['lc_id'] == ilc
            offset_lc = self.lc[idx_lc]['Flux'] * 5e-3
            self.lc['FluxErr'][idx_lc] = np.sqrt(self.lc['FluxErr'][idx_lc] ** 2 + offset_lc ** 2)
            
        if (np.isinf(self.lc['Flux']) ^ np.isinf(self.lc['FluxErr'])).sum() > 0:
            print('Inf in photo flux set to zeros')
            idx_inf = np.where((np.isinf(self.lc['Flux']) ^ np.isinf(self.lc['FluxErr'])))[0]
            self.lc['Flux'][idx_inf] = 0.
            self.lc['FluxErr'][idx_inf] = 100.

        if (np.isnan(self.sp['Flux']) ^ np.isnan(self.sp['FluxErr'])).sum() > 0:
            print('NaN in photo flux set to zeros')
            idx_nan = np.where((np.isnan(self.sp['Flux']) ^ np.isnan(self.sp['FluxErr'])))[0]
            self.lc['Flux'][idx_nan] = 0.
            self.lc['FluxErr'][idx_nan] = 100.
            
        self.lc = self.lc[self.lc['FluxErr'] != 100]

    def data_cuts(self):
        r"""
        Remove data out of the model definition. 
        If a date of observation is out of phase range, or wavelength out of wavelength range, 
        data point(s) is(are) removed.

        Returns
        -------
        idx_sp : numpy.array
            Spectral data index cuts.
        idx_lc : numpy.array
            Photometric data index cuts.
        """
        blue_cutoff, red_cutoff = self.model.wl_range
        early_cutoff, late_cutoff = self.model.phase_range

        # for JLA and K21 need cutoff to be less than model def;
        # in order to degrade tmax and fit
        early_cutoff += 5
        late_cutoff -= 5
        
        lc = self.lc
        sp = self.sp

        # lc
        bands = np.unique(lc['Filter'])
        lambda_range = np.linspace(1500, 11000, int(1e5))
        min_lambda = np.zeros(len(lc['Filter']))
        max_lambda = np.zeros(len(lc['Filter']))
        for bd in bands:
            idx = lc['Filter'] == bd
            ff = self.model.filter_db.transmission_db[bd.decode('UTF-8')].func(lambda_range)
            idxx = np.where(ff > ff.max()*0.01)
            mmin, mmax = lambda_range[idxx[0][0]], lambda_range[idxx[0][-1]]
            min_lambda[idx] = mmin/(1+lc['ZHelio'][idx])
            max_lambda[idx] = mmax/(1+lc['ZHelio'][idx])
        date_lc = (lc['Date'] - self.data_generator.snInfo['tmax'][lc['sn_id']]) / (1. + lc['ZHelio'])
        idx_ph_lc = (date_lc > early_cutoff) & (date_lc < late_cutoff)
        idx_wl_lc = (min_lambda > blue_cutoff) & (max_lambda < red_cutoff)
        idx_lc = idx_ph_lc & idx_wl_lc

        # sp
        wl_sp = sp['Wavelength'] / (1. + sp['ZHelio'])
        idx_wl_sp = (wl_sp > blue_cutoff) & (wl_sp < red_cutoff)
        date_sp = (sp['Date'] - self.data_generator.snInfo['tmax'][sp['sn_id']]) / (1. + sp['ZHelio'])
        idx_ph_sp = (date_sp > early_cutoff) & (date_sp < late_cutoff)
        
        idx_sp = idx_ph_sp & idx_wl_sp
        return idx_sp, idx_lc

    def init_from_data(self, filename):
        """
        Initiated light curve and spectra array from a stored file.

        Parameters
        ----------
        filename : str
            If simulation is already stored somewhere.
        """
        self.seed = 0
        dict_data = pickle.load(open(filename, "rb"))
        
        self.lc = dict_data['lc']
        self.sp = dict_data['spec']
        self.snInfo = dict_data['snInfo']
        self.filterpath = dict_data['filterpath']        
        if self.gamma_init != 0.:
            
            sig = dict_data['sig']
            self.lc['Flux'] -= sig[self.lc['i']]
            self.sp['Flux'] -= sig[self.sp['i']]
            flux = np.hstack((self.lc['Flux'], self.sp['Flux']))
            flux_err = np.hstack((self.lc['FluxErr'], self.sp['FluxErr']))
            
            val = flux_err ** 2 + (self.gamma_init * flux) ** 2
            if self.kappa_init != 0:
                print('kappa in generation')
                val += np.hstack((self.kappa_init * np.ones_like(self.lc['lc_id']),
                                  np.zeros_like(self.sp['i'])))**2
            sigma = np.sqrt(val)
            
            print("Adding New noise \n")
            if type(self.seed) == int:
                np.random.seed(self.seed)
            self.sig = np.random.normal(0, sigma)

            self.lc['Flux'] += self.sig[self.lc['i']]
            self.sp['Flux'] += self.sig[self.sp['i']]            
