from iman import *
from scipy.io import savemat

def np2mat(param , fname):
   mdic = {"param": np.array(param)}
   savemat(fname, mdic)