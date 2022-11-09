import numpy as np
import nacl.instruments
import os 
from nacl.simulations.reindex import reindex
from nacl.dataset import TrainingDataset
import glob


class Generator(object):
    r"""
    Data generator.
    Generate K21 simulation (Kenworthy et al. 2021)

    We start again from the objects composing each of these training batches~: we take their redshifts,
    their SALT2 parameters (:math:`X_0`, :math:`X_1`, :math:`c`, :math:`t_{max}`) as well as the
    photometric and spectroscopic observation dates.


    Attributes
    ----------
    filespath : str
        Path to the repository containing the light curve et spectra files.
    filterpath : str
        Path to the filters files repository in nacl.dev/data/
    Sne ; numpy.array
        SNe names
    lc : numpy.rec.array
        Light curves data with data_type as type.
    sp : numpy.rec.array
        Spectral data, with data_type as type.
    snInfo : numpy.rec.array
        SNe information (:math:`z`, :math:`tmax`, :math:`x1`, :math:`x0`, :math:`c`)
    data_type : list
        NaCl data type.
    snInfo_type : list
        Type of information of SNe.

    sigma_lc : numpy.array
        Dispersion of photometric data
    sigma_sp : numpy.array
        Dispersion of spectral data.
    trainingDataset : nacl.dataset.TrainingDataset
        Data set of photometric and spectroscopic observations.
    """
    def __init__(self, filespath='../data/SALT3_training_sample/Data_reshape/',
                 filterpath='../data/SALT3_training_sample/filters'):
        """
        Constructor - computes the arguments

        Parameters
        ----------
        filespath : string
           path to the repository containing the light curve et spectra files.
        filterpath : string
           path to the filters files repository in nacl.dev/data/
        """
        self.filespath = filespath
        self.filterpath = filterpath

        self.Sne, self.snInfo, self.lc, self.sp = None, None, None, None
        self.sigma_lc, self.sigma_sp, self.trainingDataset = None, None, None

        self.data_type = [('Date', '<f8'), ('Flux', '<f8'), ('FluxErr', '<f8'),
                          ('Filter', '|S20'), ('Wavelength', '<f8'), 
                          ('MagSys', '|S20'), ('ZHelio', '<f8'), ('sn_id', '<i4'), ('spec_id', '<i4')]
        self.snInfo_type = [('z', '<f8'), ('tmax', '<f8'), ('x1', '<f8'),
                            ('x0', '<f8'), ('c', '<f8')]
        self.make_data()
        
    def merge_data_file(self):
        r"""
        Merge all the K21 survey training files of light curves and spectra.

        Returns
        -------
        lc_allsurveys : numpy.rec.array
             All surveys light curve file.
        lc_sum_allsurveys : numpy.rec.array
             All surveys light curve summary file.
        sp_allsurveys : numpy.rec.array
             All surveys spectra file.
        sp_sum_allsurveys : numpy.rec.array
             All surveys spectra summary file.
        """
        surveys = glob.glob(self.filespath + os.sep + '*_lc.npy')
        surveys = [i.split('/')[-1].split('_')[0] for i in surveys]
        lc_allsurveys, sp_allsurveys = [], []
        lc_sum_allsurveys, sp_sum_allsurveys = [], []
        
        for sur in surveys:
            lc = np.load(self.filespath + os.sep + f'{sur}_lc.npy')
            lc_sum = np.load(self.filespath + os.sep + f'{sur}_lc_summary.npy',
                             allow_pickle=True)
            try:
                sp = np.load(self.filespath + os.sep + f'{sur}_spectra.npy')
                sp_sum = np.load(self.filespath + os.sep + f'{sur}_spectra_summary.npy',
                                 allow_pickle=True)
            except FileNotFoundError:
                print('No spectra')
                sp = None
            try:
                lc_id_offset = lc_allsurveys[-1]['id']+1
                sp_id_offset = sp_allsurveys[-1]['id']+1
            except IndexError:
                lc_id_offset, sp_id_offset = 0, 0
   
            lc['id'] += lc_id_offset
            
            if sp is not None:
                sp['id'] += sp_id_offset
                
            if np.where(np.array(surveys) == sur)[0][0] == 0:
                lc_allsurveys = lc
                lc_sum_allsurveys = lc_sum
                if sp is not None:
                    sp_allsurveys = sp
                    sp_sum_allsurveys = sp_sum
                    
            else:
                lc_allsurveys = np.hstack((lc_allsurveys, lc))
                lc_sum_allsurveys = np.hstack((lc_sum_allsurveys, lc_sum))
                if sp is not None:
                    sp_allsurveys = np.hstack((sp_allsurveys, sp))
                    sp_sum_allsurveys = np.hstack((sp_sum_allsurveys, sp_sum))
                    
        return lc_allsurveys, lc_sum_allsurveys, sp_allsurveys, sp_sum_allsurveys

    @staticmethod
    def get_sn_parameter(lc_sum):
        r"""
        Get sn parameters from published files

        Parameters
        ----------
        lc_sum : array
            Light curve summary file.

        Returns
        -------
        x0 : list
            :math:`X_0` of K21 training sets
        x1 : list
            :math:`X_1` of K21 training sets
        color : list
            :math:`c` of K21 training sets
        """
        salt3 = np.recfromtxt('../data/SALT3_training_sample/SALT3TRAIN_K21_PUBLIC/SALT3_PARS_INIT.LIST')
        x0, x1, color = [], [], []
        for isn in lc_sum['SN']:
            idx = salt3['f0'] == isn[1:]       
            x0.append(salt3[idx]['f2'][0])
            x1.append(salt3[idx]['f3'][0])
            color.append(salt3[idx]['f4'][0])
        return x0, x1, color
    
    def make_data(self):
        r"""
        Make training set from jla*.npy files, where all JLA data are gathered.
        Calculated ratio of error measured on measurements.
        
        Remove data out from definition ranges.
        """

        lc, lc_sum, sp, sp_sum = self.merge_data_file()
        
        lc_sum = lc_sum[np.unique(lc['id'])]
        sp_sum = sp_sum[np.unique(sp['id'])]    
        self.Sne = lc_sum['SN'][np.unique(lc['id'])]    
        lc['id'] = reindex(lc['id'])
        sp['id'] = reindex(sp['id'])

        # self.sne = lc_sum['SN']

        lc_mean_wavelength = np.zeros_like(lc['id'])
        bands = [i.decode('UTF-8') for i in np.unique(lc['Filter'])]
        filterset = nacl.instruments.load_instrument(bands[0].split('::')[0],
                                                     path=self.filterpath)  # salt2.load_filters(bands)
        for bd in bands:
            idxmw = lc['Filter'] == bd.encode('UTF-8')
            band_k21 = bd.split('::')[1]
            lc_mean_wavelength[idxmw] = filterset.get_efficiency(band_k21).mean()

        self.lc = np.rec.fromarrays((lc['Date'], lc['Flux'], lc['FluxErr'],
                                     lc['Filter'], lc_mean_wavelength, 
                                     lc['MagSys'], lc_sum['ZHelio'][lc['id']], lc['id'],
                                     # len(np.unique(sp['id'])) + np.arange(len(lc['id']))
                                     -1 * np.ones_like(lc['Flux'])),
                                    dtype=self.data_type)
        sp_none = np.array([b''] * len(sp))
        sp_id = np.array([np.where(lc_sum['SN'] == i)[0][0] for i in sp_sum['SN']])[sp['id']]
                
        self.sp = np.rec.fromarrays((sp_sum['Date'][sp['id']], sp['Flux'],
                                     sp['FluxErr'], sp_none, sp['Wavelength'],
                                     sp_none, lc_sum['ZHelio'][sp_id], sp_id, sp['id']),
                                    dtype=self.data_type)

        self.sigma_lc = np.abs(self.lc['FluxErr']/self.lc['Flux'])
        self.sigma_sp = np.abs(self.sp['FluxErr']/self.sp['Flux'])
        x0, x1, color = self.get_sn_parameter(lc_sum)
        self.snInfo = np.rec.fromarrays((lc_sum['ZHelio'], lc_sum['DayMax'], x1, x0, color),
                                        dtype=self.snInfo_type)
        self.indexing()
        self.trainingDataset = TrainingDataset(self.lc, self.sp, self.snInfo,
                                               filterpath=self.filterpath)

    def indexing(self):
        """
        Reindex spectral ('spec_id', 'sn_id') and photometric data ('band_id', 'lc_id', 'sn_id'),
        when data have been removed.
        """
        n_lc, n_sp = len(self.lc), len(self.sp)
        # band indexation 
        dict_bd = {}
        _, idx_bd = np.unique(self.lc['Filter'], return_index=True)
        for i_bd, bd in enumerate(self.lc['Filter'][np.sort(idx_bd)]):
            dict_bd[bd] = i_bd
        id_bd = np.array([dict_bd[bd] for bd in self.lc['Filter']])

        # light curve indexation
        c = 0
        id_lc = np.ones(len(self.lc['Flux']))  # .astype(int)
        
        for i in range(self.lc['sn_id'][-1]+1):
            idx_sn = self.lc['sn_id'] == i
            lcs = self.lc[idx_sn]
            _, idx = np.unique(lcs["Filter"], return_index=True)
            for bd_sn in lcs['Filter'][np.sort(idx)]:
                id_lc[(self.lc['sn_id'] == i) & (self.lc['Filter'] == bd_sn)] = c  # [c]*len(lc[lc]))
                c += 1

        id_lc = np.hstack(np.array(id_lc))
        self.lc = np.lib.recfunctions.rec_append_fields(self.lc,
                                                        names=['lc_id', 'band_id', 'i'],
                                                        data=[id_lc.astype(int), id_bd, np.arange(n_lc)])
        i_sp = n_lc + np.arange(n_sp)
        sp_ones = np.ones_like(i_sp)
        
        self.sp = np.lib.recfunctions.rec_append_fields(self.sp,
                                                        names=['lc_id', 'band_id', 'i'],
                                                        data=[-1*sp_ones, -1*sp_ones,
                                                              n_lc + np.arange(n_sp)])
