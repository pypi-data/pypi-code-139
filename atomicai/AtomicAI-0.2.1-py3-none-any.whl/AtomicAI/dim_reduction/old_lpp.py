"""
    Module for analysis with LPP
    - Used by TS-LPP as well
"""
import warnings
warnings.filterwarnings("ignore")
import numpy as np
from tqdm.auto import tqdm

import sys, os, random, scipy, scipy.stats, sklearn
from scipy.spatial import distance
from sklearn.cluster import KMeans

def lpp():
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
            for reduced_dim in [2]:
                outfile = out_directory+str(reduced_dim)+'D_LPP_'+des_file
                features = np.asarray(np.loadtxt(in_dir+des_file, skiprows=0))
                #random_indices = random.choices(np.arange(0, len(features)), k=2000)
                #features = features[random_indices]

                #features = pd.read_csv(in_dir+des_file, header=None).values
                #loc_pca = PCA(n_components = reduced_dim)
                #data = loc_pca.fit_transform(features).transpose()

                number_of_eta = 50  # number of decay functions
                element_conversion = {'Si': 0}  # Only Si in this system
                species = ['Si']
                target_element = 0
                this_descriptor = 'ACSF_G2'  # 2-body descriptory. Can also be ACSF_G2G4
   
                number_of_clusters = 4
                knn = 7
   
                #my_tslpp = TsLpp(clustering_type='k_means')
                data, labels, Y_final = perform_lpp(
                    features,
                    graph_nearest_neighbors = knn,
                    number_of_clusters=number_of_clusters,
                    number_of_dimensions=reduced_dim,
                    #k_nearest_neighbors=knn,
                    #silent=True,
                    #dimension_list=[5, 10, 20],
                    #sigma_list=[20],
                    )
                with open(outfile,mode='w') as nf:
                    lines = []
                    print(np.shape(data), len(data[0]))
                    for i in range(len(data[0])):
                        #tmp_lst = [data[j][i] for j in range(len(data))]
                        V_str_list = ["{0: >30.16e}".format(data[0][i]), "{0: >30.16e}".format(data[1][i]), "{0: >10.4s}".format(str(labels[i]))]#data[1][i], labels[i]]]
                        lines.append("".join(V_str_list) + '\n')
                    #lines.append("".join(["{0: >10.4s}".format(str(l)) for l in labels]) + '\n')
                    nf.writelines(lines)
                    nf.close()
    return


def new_centering(reference_data, my_data):
    """
        Keep only columns that have some variance.
    :param reference_data:
    :param my_data:
    :return:
    """
    reference_std = np.std(reference_data, 0)
    reference_index = np.where(reference_std != 0)
    return (my_data[:, reference_index[0]] -
            np.mean(reference_data[:, reference_index[0]], 0)) / reference_std[reference_index[0]]


def compute_lpp(
        descriptor_data: np.float64,
        graph_nearest_neighbors: int,
        sigma: float,
        n_components_target: int,
):
    """
        Locally preserving projection.
    :param n_components_target:
    :param sigma:
    :param descriptor_data: 2D array (typically, numpy.array)
    :param graph_nearest_neighbors: number (knn)
    :return:
    """

    # Create distance matrix
    distance_matrix = distance.cdist(descriptor_data, descriptor_data, metric='euclidean')

    weighted_adjacency_matrix = np.exp(-np.power(distance_matrix, 2) / 2.0 / sigma / sigma)

    for data_number in range(len(descriptor_data)):
        weighted_adjacency_matrix[data_number, data_number] = 0.0

    # Create neighbor graph
    for data_number in range(len(descriptor_data)):
        del_list = np.argsort(weighted_adjacency_matrix[data_number])[::-1][graph_nearest_neighbors:]
        weighted_adjacency_matrix[data_number, del_list] = 0.0

    # Symmetrical of W
    weighted_adjacency_matrix = np.maximum(weighted_adjacency_matrix.T, weighted_adjacency_matrix)

    # Create D
    degree_matrix = np.diag(np.sum(weighted_adjacency_matrix, axis=1))

    # Create L
    graph_laplacian = degree_matrix - weighted_adjacency_matrix

    # SVD of X1
    delta = 1e-7
    U, Sig, VT = np.linalg.svd(descriptor_data, full_matrices=False)
    rk = np.sum(Sig / Sig[0] > delta)
    Sig = np.diag(Sig)
    U1 = U[:, 0:rk]
    VT1 = VT[0:rk, :]
    Sig1 = Sig[0:rk, 0:rk]

    # Positive definite for L
    Lp = np.dot(U1.T, np.dot(graph_laplacian, U1))
    Lp = (Lp + Lp.T) / 2

    # Positive definite for D
    Dp = np.dot(U1.T, np.dot(degree_matrix, U1))
    Dp = (Dp + Dp.T) / 2

    # Generalized eigenvalue problem
    eig_val, eig_vec = scipy.linalg.eigh(Lp, Dp)

    # Projection for low dimension
    tmp1 = np.dot(VT1.T, scipy.linalg.solve(Sig1, eig_vec))
    Trans_eig_vec = tmp1.T

    # Mapping matrix (Y)
    mapping_matrix_1 = Trans_eig_vec[0:n_components_target]

    x_transformed = np.dot(mapping_matrix_1, descriptor_data.T).T

    return x_transformed, mapping_matrix_1


def perform_lpp(
        descriptor_data,
        graph_nearest_neighbors=7,
        number_of_clusters=4,
        sigma_list=(5, 10, 20, 50, 100, 1000),
        number_of_dimensions=2,
):
    X = new_centering(descriptor_data, descriptor_data)
    # number_of_lines, number_of_features = np.shape(descriptor_data)
    # sigma_num = sigma_list[-1]

    PseudoF_max = 0.0

    for sigma in tqdm(sigma_list):
        # Scan sigma for best classification

        ############
        # LPP x 1
        ############

        X_final_lpp, Y_final_lpp = compute_lpp(X, graph_nearest_neighbors, sigma, number_of_dimensions)

        # Clustering by K means
        k_means_model = KMeans(n_clusters=number_of_clusters, random_state=10).fit(X_final_lpp)

        labels = k_means_model.labels_

        PseudoF = sklearn.metrics.calinski_harabasz_score(X_final_lpp, labels)

        if PseudoF > PseudoF_max:
            # Update best hyperparameters
            PseudoF_max = PseudoF
            sigma_max = sigma

    # Output the best result
    X_final_lpp, Y_final_lpp = compute_lpp(X, graph_nearest_neighbors, sigma_max, number_of_dimensions)
    k_means_model = KMeans(n_clusters=number_of_clusters, random_state=10).fit(X_final_lpp)
    labels = k_means_model.labels_
    PseudoF = sklearn.metrics.calinski_harabasz_score(X_final_lpp, labels)
    print(f'Best sigma is {sigma_max} with pseudoF score of {PseudoF}.')
    lpp_projection = np.transpose(X_final_lpp)

    return lpp_projection, labels, Y_final_lpp
