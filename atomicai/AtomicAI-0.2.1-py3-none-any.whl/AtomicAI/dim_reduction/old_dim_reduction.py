import warnings
warnings.filterwarnings("ignore")
import sys, os
import numpy as np
from AtomicAI.dim_reduction.select_descriptors_and_manual_labels import select_descriptors_and_manual_labels
from AtomicAI.dim_reduction.lpp import lpp
from sklearn.decomposition import PCA

def dim_reduction():
    '''

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
            for reduced_dim in [2]:  # For more dimension, extand the list like [2, 3, 4, ...]
                if_label, descriptors, manual_labels = select_descriptors_and_manual_labels(in_dir+des_file)
                train_features = descriptors[0]
                color_labels = manual_labels[0]
                loc_pca = PCA(n_components = reduced_dim)
                pca_data = loc_pca.fit_transform(train_features).transpose()
                pca_data = np.vstack((pca_data, color_labels))
                lpp_data, lpp_outfile_labels = lpp(train_features, reduced_dim)
                lpp_data = np.vstack((lpp_data, color_labels))
                pca_outfile_labels = ['PC1', 'PC2', 'manual_labels']
                lpp_outfile_labels.append('manual_labels')
                outfiles_labels = [pca_outfile_labels, lpp_outfile_labels]
                models_data =  [pca_data, lpp_data]
                models = ['PCA', 'LPP']
                for outfile_labels, model, model_data in zip(outfiles_labels, models, models_data):
                    outfile = f'{out_directory}{str(reduced_dim)}D_{model}_{des_file}'
                    with open(outfile, mode='w') as nf:
                        lines, data_format = [], ["{0: >30.16e}" for dummy in range(0, len(model_data))]
                        labels_data_format = ["{0: >30.16s}" for dummy in range(0, len(model_data))]
                        labels_list = [labels_data_format[j].format(outfile_labels[j]) for j in range(0, len(model_data))]
                        lines.append("".join(labels_list)+'\n')
                        for i in range(len(color_labels)):
                            V_str_list = [data_format[j].format(model_data[j][i]) for j in range(0, len(model_data))]
                            lines.append("".join(V_str_list) + '\n')
                        nf.writelines(lines)
                        nf.close()
    return
