import numpy as np
import os
from .reindex import reindex
from ..dataset import TrainingDataset
from ..util import salt2


class Generator(object):
    r"""
    Data generator.
    Generate JLA simulation (Betoule et al. 2014)

    We start again from the objects composing each of these training batches~: we take their redshifts,
    their SALT2 parameters (:math:`X_0`, :math:`X_1`, :math:`c`, :math:`t_{max}`) as well as the
    photometric and spectroscopic observation dates.

    Attributes
    ----------
    filespath : str
        Path to the repository containing the light curve et spectra files.
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
    def __init__(self, filespath='../data/JLA_training_sample'):
        """
        Constructor - computes the arguments
        Args:
            filespath : string
               path to the repository containing the light curve et spectra files.
        """
        self.filespath = filespath

        self.Sne, self.snInfo, self.lc, self.sp = None, None, None, None
        self.sigma_sp, self.sigma_lc, self.trainingDataset, self.id_lc = None, None, None, None

        self.data_type = [('Date', '<f8'), ('Flux', '<f8'), ('FluxErr', '<f8'),
                          ('Filter', '|S20'), ('Wavelength', '<f8'), 
                          ('MagSys', '|S20'), ('ZHelio', '<f8'), ('sn_id', '<i4'), ('spec_id', '<i4')]
        self.snInfo_type = [('z', '<f8'), ('tmax', '<f8'), ('x1', '<f8'),
                            ('x0', '<f8'), ('c', '<f8')]
        self.make_data()

    def make_data(self):
        r"""
        Make training set from jla*.npy files, where all JLA data are gathered.
        Calculated ratio of error measured on measurements.
        
        Remove data out from definition ranges.
        """
        lc = np.load(self.filespath + os.sep + 'jla_lc.npy')
        lc_sum = np.load(self.filespath + os.sep + 'jla_lc_summary.npy', allow_pickle=True)
        sp = np.load(self.filespath + os.sep + 'jla_spectra.npy')
        sp_sum = np.load(self.filespath + os.sep + 'jla_spectra_summary.npy', allow_pickle=True)

        lc_sum = lc_sum[np.unique(lc['id'])]
        sp_sum = sp_sum[np.unique(sp['id'])]    
        self.Sne = lc_sum['SN'][np.unique(lc['id'])]
        lc['id'] = reindex(lc['id'])
        sp['id'] = reindex(sp['id'])

        lc_mean_wavelength = np.zeros_like(lc['id'])
        bands = [i.decode('UTF-8') for i in np.unique(lc['Filter'])]
        filterset = salt2.load_filters(bands)
        for bd in bands:
            idxmw = lc['Filter'] == bd.encode('UTF-8')
            lc_mean_wavelength[idxmw] = filterset.mean_wavelength([bd])

        # self.sne = lc_sum['SN']
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

        self.sigma_lc = np.abs(self.lc['FluxErr'])/np.abs(self.lc['Flux'])
        self.sigma_sp = np.abs(self.sp['FluxErr'])/np.abs(self.sp['Flux'])
        
        self.snInfo = np.rec.fromarrays((lc_sum['ZHelio'], lc_sum['DayMax'], lc_sum['X1'],
                                        lc_sum['X0'], lc_sum['Color']), dtype=self.snInfo_type)
        self.indexing()

        # 392 spectre sn z = 0.68, obs date = 53404. MJD
        # 392 spectre sn z = 0.64, obs date = 53445. MJD
        print(" removing spectra 392,398 index by this confing")            
        # print('LEN SP : ', len(self.sp))
        self.sp, self.sigma_sp = self.remove()  # [392,398])
        # print('LEN SP : ', len(self.sp))
        # print('LEN SigP : ', len(self.sigma_sp))

        self.lc, self.sigma_lc, self.sp, self.sigma_sp = self.remove_sn_low_c()
        
        self.trainingDataset = TrainingDataset(self.lc, self.sp, self.snInfo)

    def remove(self):
        """
        Removing 2 spectra at late date.

        Returns
        -------
        sp : numpy.rec.array
            Spectra array re-indexed without 2 spectra
        sp_err :
            Flux error array re-indexed without 2 spectra
        """
        sp = self.sp.copy()
        sp_err = self.sigma_sp.copy()
        spec_id = []
        for iz, idd in zip([0.68, 0.64], [53404., 53445.]):
            spec_id.append(np.unique(sp['spec_id'][(sp['ZHelio'] == iz) & (sp['Date'] == idd)])[0])
        print('removed id spec_id : ', spec_id)
        spec_id = np.array(spec_id)
        for si in spec_id:
            # print(sp[sp['spec_id'] == si]['Date'][0], sp[sp['spec_id'] == si]['ZHelio'][0])
            idx = sp['spec_id'] == si
            sp = np.delete(sp, idx)
            sp_err = np.delete(sp_err, idx)
            sp['spec_id'][sp['spec_id'] > si] -= 1
            sp['i'][sp['spec_id'] > si] -= idx.sum()
            spec_id -= 1
        return sp, sp_err

    def remove_sn_low_c(self):
        """
        Removing SN with :math:`c < -1`

        Returns
        -------
        lc : numpy.rec.array
            Light curves array re-indexed those SNe.
        lc_err :
             Light curves array re-indexed without those SNe.
        sp : numpy.rec.array
            Spectra array re-indexed without those SNe.
        sp_err :
            Flux error array re-indexed without those SNe.
        """
        sp = self.sp.copy()
        sp_err = self.sigma_sp.copy()
        spec_id = []

        lc = self.lc.copy()
        lc_err = self.sigma_lc.copy()
        lc_id = []

        c = self.snInfo['c'] 
        idxxc = np.where(c < -1)[0]
        for idd in idxxc:
            spid = np.unique(sp['spec_id'][sp['sn_id'] == idd])
            spec_id.append(spid)
            lcid = np.unique(lc['lc_id'][lc['sn_id'] == idd])
            lc_id.append(lcid)

            idx_lc = lc['sn_id'] == idd
            lc = np.delete(lc, idx_lc)
            lc_err = np.delete(lc_err, idx_lc)
            
            lc['lc_id'][lc['sn_id'] > idd] -= len(lcid)
            lc['i'][lc['sn_id'] > idd] -= idx_lc.sum()
            lc['sn_id'][lc['sn_id'] > idd] -= 1

            idx_sp = sp['sn_id'] == idd
            sp = np.delete(sp, idx_sp)
            sp_err = np.delete(sp_err, idx_sp)
            
            sp['spec_id'][sp['sn_id'] > idd] -= len(spid)
            sp['i'][sp['sn_id'] > idd] -= idx_sp.sum()
            sp['sn_id'][sp['sn_id'] > idd] -= 1

        self.snInfo = np.delete(self.snInfo, idxxc)
        self.Sne = np.delete(self.Sne, idxxc)
        return lc, lc_err, sp, sp_err

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

        self.id_lc = np.hstack(np.array(id_lc))
        self.lc = np.lib.recfunctions.rec_append_fields(self.lc,
                                                        names=['lc_id', 'band_id', 'i'],
                                                        data=[id_lc.astype(int), id_bd,
                                                              np.arange(n_lc)])
        i_sp = n_lc + np.arange(n_sp)
        sp_ones = np.ones_like(i_sp)
        
        self.sp = np.lib.recfunctions.rec_append_fields(self.sp,
                                                        names=['lc_id', 'band_id', 'i'],
                                                        data=[-1*sp_ones, -1*sp_ones,
                                                              n_lc + np.arange(n_sp)])
