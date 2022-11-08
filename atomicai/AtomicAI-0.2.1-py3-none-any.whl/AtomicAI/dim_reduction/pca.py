from sklearn.decomposition import PCA
from AtomicAI.data.descriptor_cutoff import descriptor_cutoff
from AtomicAI.io.write_data_in_py import write_data_in_py
import sys, os
import ase.io
import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

def pca():
    '''
    Principal Component Analysis:

    The features that are read from 'descriptors' directoy will be classify using PCA from sklearn.
    The classified data will be written as a python file called 'pca_projected_data.py' in 'pca' direcroy. 
    '''
    in_dir = './descriptors/'
    des_files = sorted([f for f in os.listdir(in_dir) if '.dat' in f])
    if len(des_files) > 0:
        print(f"Availabel files are \n {', '.join(des_files)}")
    else:
        print("No des_file.dat file is availabel HERE!!!")
        exit()
    out_directory = './dim_reduction/'
    if not os.path.isdir(out_directory):
        os.makedirs(out_directory)

    for des_file in des_files:
            for reduced_dim in [2]:
                outfile = out_directory+str(reduced_dim)+'D_PCA_'+des_file
                features = np.asarray(np.loadtxt(in_dir+des_file, skiprows=0))
                #features = pd.read_csv(in_dir+des_file, header=None).values
                loc_pca = PCA(n_components = reduced_dim)
                data = loc_pca.fit_transform(features).transpose()
                with open(outfile, mode='w') as nf:
                    lines = []
                    for i in range(len(data[0])):
                        #tmp_lst = [data[j][i] for j in range(len(data))]
                        V_str_list = ["{0: >30.16e}".format(v) for v in [data[0][i], data[1][i]]]#tmp_lst]
                        lines.append("".join(V_str_list) + '\n')
                    nf.writelines(lines)
                    nf.close()
    return
