"""
"""
import numpy as np
import logging
import pylab as pl
from . import instruments
logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    level=logging.INFO)


def stringify(nt):
    """
    Cast a record array so that byte fields become utf8 fields
    """
    dt = [(f, t.replace('S', 'U')) for f, t in nt.dtype.descr]
    return nt.astype(dt)


def load(filename):
    """
    default loader: load the simulated data 
    in the format G.A. has defined for his work.

    Parameters
    -------
    filename : str
        name of the simulation file

    Returns
    -------
    TrainingDataset
       A training dataset, with (1) LC and spectra, (2) an index of each spectrum and each light curve
    """
    logging.info('loading data from: {}'.format(filename))
    f = np.load(filename, allow_pickle=True)
    data = f['data']
    sne = f['snInfo']
    
    idx_spectral_data = data['Filter'] == b''
    lc_data = data[~idx_spectral_data]
    spectral_data = data[idx_spectral_data]

    lc_data = np.lib.recfunctions.rename_fields(lc_data, {'id': 'sn_id', 'obs_id': 'spec_id'})
    spectral_data = np.lib.recfunctions.rename_fields(spectral_data, {'id': 'sn_id', 'obs_id': 'spec_id'})
    lc_data['spec_id'] = -1
    lc_data, spectral_data = indexing(lc_data, spectral_data)
    return TrainingDataset(lc_data, spectral_data, sne)


def indexing(lc_data, spectral_data):
    """
    For photometric data create a band index, a light curve index and a data point index.
    For spectroscopic data create a band index (equal to -1), a light curve index (equal to -1)
    and a data point index (starting after last photometric data point index).

    Parameters
    -------
    lc_data : nacl.dataset.LcData
        Photometric data
    spectral_data : nacl.dataset.SpectrumData
        Spectral data

    Returns
    -------
    lc_data : numpy.rec.array (=nacl.dataset.LcData.data)
        Photometric data array.
    spectral_data : numpy.rec.array (=nacl.dataset.SpectrumData.data)
        Spectral data array.
    """
    n_lc, n_sp = len(lc_data), len(spectral_data)

    # band indexation                                                                                
    dict_bd = {}
    _, idx_bd = np.unique(lc_data['Filter'], return_index=True)
    for i_bd, bd in enumerate(lc_data['Filter'][np.sort(idx_bd)]):
        dict_bd[bd] = i_bd
    id_bd = np.array([dict_bd[bd] for bd in lc_data['Filter']])

    # light curve indexation                                                                         
    c = 0
    id_lc = np.ones(len(lc_data['sn_id'])).astype('<i8')
    
    for i in range(lc_data['sn_id'][-1]+1):
        idx_sn = lc_data['sn_id'] == i
        lcs = lc_data[idx_sn]
        _, idx = np.unique(lcs["Filter"], return_index=True)
        for bd_sn in lcs['Filter'][np.sort(idx)]:
            id_lc[(lc_data['sn_id'] == i) & (lc_data['Filter'] == bd_sn)] = c 
            c += 1
            
    id_lc = np.hstack(np.array(id_lc))

    lc_data = np.lib.recfunctions.rec_append_fields(lc_data,
                                                    names=['lc_id', 'band_id', 'i'],
                                                    data=[id_lc, id_bd, np.arange(n_lc)])
    i_sp = n_lc + np.arange(n_sp)
    sp_ones = np.ones_like(i_sp)
    spectral_data = np.lib.recfunctions.rec_append_fields(spectral_data,
                                                          names=['lc_id', 'band_id', 'i'],
                                                          data=[-1*sp_ones, -1*sp_ones,
                                                                n_lc + np.arange(n_sp)])
    return lc_data, spectral_data


class LcData:
    r"""
    Light curve data class.
    We define one per Lc.

    Attributes
    ----------
    sn : int
        Index of sn.
    band : str
        Name of the Filter.
    slc : slc
        Index of the Light Curve data in the full photometric data.
    lc_data : numpy.rec.array
        Full photometric data.
    sne : numpy.rec.array
            Information of all SNe (:math:`(z, X_0, X_1, c, t_{max})`)
    sn_info : numpy.rec.array
        Information of the SN.

    """
    def __init__(self, sn, band, slc, lc_data, sne):
        """
        Constructor

        Parameters
        ----------
        sn : int
            Index of sn.
        band : str
            Name of the Filter.
        slc : slc
            Index of the Light Curve data in the full photometric data.
        lc_data : numpy.rec.array
            Photometric data.
        sne : numpy.rec.array
            Information of all SNe (:math:`(z, X_0, X_1, c, t_{max})`)
        """
        self.sn = sn
        self.band = band.astype(str)
        self.slc = slc
        self.lc_data = lc_data
        self.sne = sne
        self.sn_info = self.sne[self.sn]

    def __len__(self):
        """
        Return number of light curve data point.
        """
        return len(self.lc_data[self.slc])

    @property
    def data(self):
        """
        Return numpy.rec.array data file.
        """
        return self.lc_data[self.slc]

    @property
    def z(self):
        """
        return SNe redshift.
        """
        return self.sn_info['z']

    @property
    def sn_id(self):
        """
        Return SN index.
        """
        return self.sn

    def plot(self):
        """
        control plot
        """
        pl.figure()
        x, y, ey = self.data['Date'], self.data['Flux'], self.data['FluxErr']
        pl.errorbar(x, y, yerr=ey, ls='', color='k', marker='o')
        pl.xlabel('phase [days]')
        pl.ylabel('Flux')
        pl.title('SN#{} {} [$z={:5.3}]$'.format(self.sn_id, self.band, self.z))

        
class SpectrumData:
    r"""
    Spectrum data class.

    Attributes
    ----------
    sn : int
        Index of sn.
    spectrum : str
        Spectra index .
    slc : slc
        Index of the Light Curve data in the full photometric data.
    spec_data : numpy.rec.array
        Full spectral data.
    sne : numpy.rec.array
            Information of all SNe (:math:`(z, X_0, X_1, c, t_{max})`)
    sn_info : numpy.rec.array
        Information of the SN.
    """
    def __init__(self, sn, spectrum, slc, spec_data, sne):
        """
        Constructor

        Parameters
        ----------
        sn : int
            Index of sn.
        spectrum : str
            Spectra index .
        slc : slc
            Index of the Light Curve data in the full photometric data.
        spec_data : numpy.rec.array
            Full spectral data.
        sne : numpy.rec.array
            Information of all SNe (:math:`(z, X_0, X_1, c, t_{max})`)
        """
        self.sn = sn
        self.spectrum = spectrum
        self.slc = slc
        self.spec_data = spec_data
        self.sne = sne
        self.sn_info = self.sne[self.sn]
        
    def __len__(self):
        """
        Return number of spectral point.
        """
        return len(self.spec_data[self.slc])

    @property
    def data(self):
        """
        Return data numpy.rec.array
        """
        return self.spec_data[self.slc]

    @property
    def z(self):
        """
        Return redshift.
        """
        return self.sn_info['z']

    @property
    def sn_id(self):
        """
        Return SN index
        """
        return self.sn
                 
    def plot(self):
        """
        control plot
        """
        pl.figure()
        x, y, ey = self.data['Wavelength'], self.data['Flux'], self.data['FluxErr']
        pl.errorbar(x, y, yerr=ey, ls='', color='k')
        pl.xlabel(r'$\lambda [\AA]$')
        pl.ylabel('Flux')
        pl.title('SN#{} [$z={:5.3}$]'.format(self.sn_id, self.z))
        

class TrainingDataset:
    """
    A class to make sure that the format of the training dataset 
    is hidden from the model. We don't want to change the model 
    each time we change the format.

    Attributes
    ----------
    lc_data : numpy.rec.array
        Light curve data.
    spec_data : numpy.rec.array
        Spectral data.
    sne : numpy.rec.array
        Information of all SNe (:math:`(z, X_0, X_1, c, t_{max})`)
    filter_names : list
        Filters names used in the training dataset.
    transmissions : list
        Filters transmission.
    lcs : list[LcData]
        List of each LcData.
    spectra : list[SpectrumData]
        List of the SpectrumData.
    filterpath : str
        If filterpath should be explicit.
    """
    def __init__(self, lc_data, spec_data, sne, filterpath=None, spectra=None, lcs=None):
        """
        load the file, sort by data type (lc/spec) and SN

        Parameters
        ----------
        lc_data : numpy.rec.array
            Light curve data.
        spec_data : numpy.rec.array
            Spectral data.
        sne : numpy.rec.array
            Information of all SNe (:math:`(z, X_0, X_1, c, t_{max})`)
        lcs : list
            List of each LcData.
        spectra : list
            List of the spectral data.
        filterpath :str
            If filterpath should be explicit.
        """
        self.lc_data = lc_data
        self.spec_data = spec_data
        self.sne = sne

        if lcs is None:
            self.lcs = []
            self._index_lcs()
        else:
            self.lcs = lcs
        
        if spectra is None: 
            self.spectra = []
            self._index_spectra()            
        else:
            self.spectra = spectra
        self.filterpath = filterpath

    def _index_lcs(self):
        """
        Sort the light curve data, so that the light curve measurements
        are stored in continuous chunks and can be indexed easily.
        
        Build and index for each light curve (i.e. set of photometric
        points, for one sn, measured in one band). An index entry
        contains a slice object and links to the original data.
        """
        logging.info('indexing the light curves')

        self.lcs = []
        
        self.lc_data.sort(order=['sn_id', 'lc_id', 'Date'])
        self.lc_data['i'] = np.arange(len(self.lc_data)).astype(int)
        for i_lc in np.arange(self.lc_data['lc_id'][-1]+1):
            idx = (self.lc_data['lc_id'] == i_lc)
            band = self.lc_data['Filter'][idx][0]
            sn = self.lc_data['sn_id'][idx][0]
            i = np.where(idx)[0]
            slc = slice(i.min(), i.max()+1)
            self.lcs.append(LcData(sn, band, slc, self.lc_data, self.sne))

    def _index_spectra(self):
        """
        Sort the spectral data, so that the spectrum measurements are
        stored in contiguous chunks and can be indexed easily.

        Build and index for each spectrum. An index entry contains a
        slice object and links to the original data.
        """
        logging.info('indexing the spectra')
        self.spec_data.sort(order=['sn_id', 'spec_id', 'Wavelength'])
        
        nspin = self.spec_data['spec_id']-self.spec_data['spec_id'][0]
        nspin[np.where(nspin < 0)] += len(np.unique(self.spec_data['spec_id']))
        self.spec_data['spec_id'] = nspin
        
        self.spec_data['i'] = len(self.lc_data) + np.arange(len(self.spec_data)).astype(int)        
                    
    def nb_sne(self):
        """
        Return number of SNe.
        """
        return len(self.sne)

    def nb_lcs(self):
        """
        Return number of light curves.
        """
        return len(self.lcs)

    def nb_spectra(self):
        """
        Return number of spectra.
        """
        n = len(np.unique(self.spec_data['spec_id']))
        return n  # len(self.spectra)

    @property
    def sp_data(self):
        """
        Return numpy.rec.array spectra data.
        """
        return self.spec_data

    @property
    def lcs_data(self):
        """
        Return numpy.rec.array photometric data.
        """
        return self.lc_data

    def get_all_filter_names(self):
        """
        scan the dataset and return the list of all passbands used to take
        the data.

        Returns
        ----------
        list
            List of filter name.
        """
        if not hasattr(self, 'filter_names'):
            t = np.unique(self.lc_data['Filter'])
            self.filter_names = t.astype(t.dtype.str.replace('S', 'U'))
        return self.filter_names

    def get_all_transmissions(self):
        """
        Return transmission of all filters

        Returns
        ----------
        list
            List of filter transmission.

        """
        if hasattr(self, 'transmissions'):
            return self.transmissions
        self.transmissions = [instruments.load(fn,path=self.filterpath) for fn in self.get_all_filter_names()]
        return self.transmissions
    
    def __iter__(self):
        """
        """
        pass



    
