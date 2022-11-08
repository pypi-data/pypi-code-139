"""
    Two-step locally preserving projection (TS-LPP) and classification
    Original code by Ryo Tamura (NIMS)
    # ----------------------------------------------------------------------
    # Copyright Ryo Tamura (NIMS), Momo Matsuda (University of Tsukuba),
    # and Yasunori Futamura (University of Tsukuba)
    # This program is free software: you can redistribute it and/or modify
    # it under the terms of the MIT licence.
    # ----------------------------------------------------------------------
    Reference: arXiv:2107.14311v1
"""

import pandas as pd
import numpy as np
import os
import pickle

from tqdm.auto import tqdm
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import sklearn.metrics
from sklearn.cluster import KMeans
from sklearn.cluster import SpectralClustering

from AtomicAI.dim_reduction.lpp import compute_lpp, new_centering


def tslpp(features, reduced_dim):
    sigma_list=np.arange(5, 100, 10)
    sigma_list = np.append(sigma_list, np.arange(100, 600, 100))
    knn = 7
    data, outfile_labels = perform_ts_lpp(
        data_x = features,
        k_nearest_neighbors = knn,
        number_of_dimensions=reduced_dim,
        sigma_list=sigma_list,
        #k_nearest_neighbors=knn,
        #silent=True,
        #dimension_list=[5, 10, 20],
        #sigma_list=[20],
        )
    return data, outfile_labels


def plot_ts_lpp_labels(
        data, labels,
        figure_file: str = None,
        show_figure: bool = True,
        sigma='default', dm='default',
):
    """
        Plot of training result by true label
        Support 2-dimension and 3-dimension results
    :param sigma: sigma displayed in figure title
    :param dm: intermediate dimensionality displayed in figure title
    :param show_figure:
    :param figure_file:
    :param data:
    :param labels:
    :return:
    """

    number_of_clusters = len(set(labels))
    target_dimensionality = np.shape(data)[1]
    print(target_dimensionality)
    if target_dimensionality == 2:

        x_coordinate = [[] for j in range(number_of_clusters)]
        y_coordinate = [[] for j in range(number_of_clusters)]

        for line_number in range(len(data)):
            x_coordinate[int(labels[line_number])].append(data[line_number, 0])
            y_coordinate[int(labels[line_number])].append(data[line_number, 1])

        f, ax = plt.subplots(figsize=(6, 6))

        for line_number in range(number_of_clusters):
            ax.plot(x_coordinate[line_number], y_coordinate[line_number], '.', alpha=0.7)
        ax.set_title(fr'$\sigma$={sigma}, dm={dm}')
        ax.set_xlabel('Component 1')
        ax.set_ylabel('Component 2')

        if figure_file:
            plt.savefig(figure_file, dpi=150)

        if show_figure:
            plt.show()
        else:
            plt.close()

    # For 3
    if target_dimensionality == 3:

        x_coordinate = [[] for j in range(number_of_clusters)]
        y_coordinate = [[] for j in range(number_of_clusters)]
        z_coordinate = [[] for j in range(number_of_clusters)]

        for line_number in range(len(data)):
            x_coordinate[int(labels[line_number])].append(data[line_number, 0])
            y_coordinate[int(labels[line_number])].append(data[line_number, 1])
            z_coordinate[int(labels[line_number])].append(data[line_number, 2])

        fig = plt.figure(figsize=(6, 6))
        ax = Axes3D(fig)

        for line_number in range(number_of_clusters):
            ax.plot(x_coordinate[line_number], y_coordinate[line_number], z_coordinate[line_number], '.', alpha=0.7)

        ax.view_init(30, 60)
        ax.set_title(fr'$\sigma$={sigma}, dm={dm}')
        ax.set_xlabel('Component 1')
        ax.set_ylabel('Component 2')
        ax.set_zlabel('Component 3')

        if figure_file:
            plt.savefig(figure_file, dpi=150)
        if show_figure:
            plt.show()
        else:
            plt.close()


def save_results(data, labels, output_file='result_training_Kmeans.txt'):
    """
        Output of training result by K-means classification
    :param data:
    :param labels:
    :param output_file:
    :return:
    """

    f1 = open(output_file, 'w')

    line_buffer = []

    for data_index in range(len(data)):
        V_list = list(data[data_index])
        V_str_list = ["{0: >30.15f}".format(v) for v in V_list]
        line_buffer.append(str(int(labels[data_index])) + "".join(V_str_list) + '\n')

    f1.writelines(line_buffer)

    f1.close()


def perform_ts_lpp(
        input_file: str = 'data.csv',
        number_of_clusters: int = 4,
        number_of_dimensions: int = 3,
        k_nearest_neighbors: int = 7,
        sigma_num: int = 20,
        dimension_grid_size: int = 4,
        output_file: str = 'ts_lpp.dat',
        figure_file: str = None, show_figure: bool = True,
        silent: bool = True,
        save_model: str = r'./ts_lpp_model.pkl',
        save_y_matrix: str = r'./y_matrix.pkl',
        sigma_min: float = 10.0,
        sigma_list=None,
        dimension_list=None,
        data_x=None,
        clustering_method='k_means',
):
    """
        Double LPP + k mean clustering + plot results
    :param clustering_method:
    :param data_x: a dataset, if the user does not wish to use a file.
    :param sigma_list: overwrite sigma_min if present!
    :param dimension_list: overwrite dimension_grid_size if present!
    :param sigma_min:
    :param dimension_grid_size: Number of points on the grid for intermediate dimension hyperparameter
    :param sigma_num:
    :param save_y_matrix:
    :param save_model: where the model will be saved
    :param silent: display log
    :param show_figure:
    :param figure_file:
    :param output_file:
    :param input_file:
    :param number_of_clusters:
    :param number_of_dimensions:
    :param k_nearest_neighbors:
    :return: X_final, labels, Y_middle, Y_final
    """

    if not silent:
        print('Performing TS-LPP on data from ', input_file)
        print('The results shall be saved in', output_file)

    acceptable_clustering_methods = ['k_means', 'spectral']
    assert clustering_method in acceptable_clustering_methods, \
        f'{clustering_method} method for classification is unknown.'


    print('Shape of data set: ', np.shape(data_x))

    X = new_centering(data_x, data_x)

    # Number of lines and features
    number_of_lines, number_of_features = np.shape(data_x)

    if not silent:
        print('*************')
        print('Training data')
        print('Number of data =', len(X))
        print('Number of features =', number_of_features)
        print('Number of clusters =', number_of_clusters)
        print('Reduced dimension =', number_of_dimensions)
        print('*************')

    """
        Perform TS-LPP
    """

    # Determination of the grid search

    if sigma_list is None:
        sigma_list = []
        for sigma_index in range(sigma_num):
            sigma_list.append(5.0 * sigma_index + sigma_min)
    elif not isinstance(sigma_list, list):  # If a single value is entered
        sigma_list = [sigma_list]
        sigma_num = 1
    else:
        sigma_num = len(sigma_list)

    if dimension_list is None:
        dimension_list = []
        for dimension_index in range(dimension_grid_size):
            dimension_list.append(int(number_of_features / (dimension_grid_size + 1) * (dimension_index + 1)))
    elif not isinstance(dimension_list, list):  # If a single value is entered
        dimension_list = [dimension_list]
        dimension_grid_size = 1
    else:
        dimension_grid_size = len(dimension_list)

    PseudoF_max = 0.0

    if not silent:
        print('Searching optimized hyperparameters...')
        print('Dimension list is:', dimension_list)
        print('Sigma list is:', sigma_list)

    # Loop of hyperparameter dm: grid search for optimized hyperparameters

    for dimension_index, n_components_middle in tqdm(
            enumerate(dimension_list),
            desc=f'TS-LPP of custom data (dm grid optimization)',
            total=len(dimension_list),
    ):

        # n_components_middle = dimension_list[dimension_index]

        # Loop of hyperparameter sigma
        # initial values
        # sigma_max = None
        # dim_max = 0

        for sigma_index, sigma in enumerate(sigma_list):

            # if sigma_index == sigma_num:
            #    # If sigma_index exceed the sigma list, calculate ts-lpp for the optimized parameters
            #    sigma = best_sigma
            #    n_components_middle = best_intermediate_dimensionality
            # else:

            ############
            # LPP x 2
            ############

            X_middle, Y_middle = compute_lpp(X, k_nearest_neighbors, sigma, n_components_middle)
            X_final, Y_final = compute_lpp(X_middle, k_nearest_neighbors, sigma, number_of_dimensions)

            if clustering_method == 'k_means':

                # Clustering by K means
                clustering_model = KMeans(n_clusters=number_of_clusters, random_state=10).fit(X_final)

            elif clustering_method == 'spectral':

                clustering_model = SpectralClustering(n_clusters=number_of_clusters).fit(X_final)

            labels = clustering_model.labels_

            PseudoF = sklearn.metrics.calinski_harabasz_score(X_final, labels)
            if not silent:
                print(f'Intermediate dimension = {n_components_middle}, sigma = {sigma}, pseudo F = {PseudoF}')
                plot_ts_lpp_labels(data=X_final,
                                   labels=labels,
                                   figure_file=figure_file, show_figure=show_figure,
                                   sigma=sigma,
                                   dm=n_components_middle)
            if PseudoF > PseudoF_max:
                # Update best hyperparameters
                PseudoF_max = PseudoF
                best_sigma = sigma
                best_intermediate_dimensionality = n_components_middle

    # Calculate with optimal hyperparameters
    X_middle, Y_middle = compute_lpp(X, k_nearest_neighbors, best_sigma, best_intermediate_dimensionality)
    X_final, Y_final = compute_lpp(X_middle, k_nearest_neighbors, best_sigma, number_of_dimensions)

    if clustering_method == 'k_means':
        clustering_model = KMeans(n_clusters=number_of_clusters, random_state=10).fit(X_final)
    elif clustering_method == 'spectral':
        clustering_model = SpectralClustering(n_clusters=number_of_clusters).fit(X_final)

    labels = clustering_model.labels_

    print(
        f'Best results found for: dm = {best_intermediate_dimensionality}, '
        f'sigma = {best_sigma} with pseudo F score of {PseudoF_max}'
    )

    with open(save_model, "wb") as f:
        pickle.dump(clustering_model, f)

    with open(save_y_matrix, 'wb') as f:
        pickle.dump(Y_final, f)

    if not silent:
        print('')
        print('*************')
        print('Hyperparameter optimization...')
        print('Optimized sigma =', best_sigma)
        print('Optimized dm =', best_intermediate_dimensionality)
        print('*************')

    save_results(data=X_final, labels=labels, output_file=output_file)
    plot_ts_lpp_labels(data=X_final, labels=labels, figure_file=figure_file, show_figure=show_figure, sigma=sigma,
                       dm=n_components_middle)

    # Calculate cluster index
    PseudoF = sklearn.metrics.calinski_harabasz_score(X_final, labels)

    if not silent:
        print('*************')
        print('clustering results')
        print('Pseudo F =', PseudoF)
        print('*************')

    return X_final, labels, Y_middle, Y_final


class TsLpp:
    """
        Class for TS-LPP model.
        Needed information to process new data:
        - Original data set (normalization - new_centering function <- From .csv file)
        - Y_middle and Y_final matrices (for dimensionality reduction <- stored?)
    """

    def __init__(self, clustering_type='k_means'):
        # DEV: accept k_means and spectral models for clustering
        self.clustering_type = clustering_type
        self.clustering_model = None
        self.x_data = None
        self.y_middle = None
        self.y_final = None
        self.data_training = None
        self.labels_training = None
        self.projections_training = None
        self.data_test = None
        self.labels_test = None
        self.projections_test = None

    def evaluate_data(self, data_file):
        test_data = pd.read_csv(data_file, header=None).values
        mq_data_normalized = new_centering(self.data_training, test_data)
        data_reduced_middle = np.dot(test_data, mq_data_normalized.T).T
        data_reduced_final = np.dot(data_reduced_middle, data_reduced_middle.T).T
        return data_reduced_final

    def fit(self,
            X_train,
            number_of_clusters: int = 4,
            number_of_dimensions: int = 2,
            k_nearest_neighbors: int = 7,
            sigma_list=None,
            dimension_list=None,
            silent: bool = True,
            ):
        """
            Train TS-LPP model using training data
        :param X_train: 
        :param number_of_clusters: 
        :param number_of_dimensions: 
        :param k_nearest_neighbors: 
        :param sigma_list: 
        :param dimension_list: 
        :param silent: 
        :return: 
        """

        if dimension_list is None:
            dimension_list = [5, 10, 15, 20, 30, 50, 100]
        if sigma_list is None:
            sigma_list = [5, 10, 15, 20, 30, 50]

        if not silent:
            print('Shape of data set: ', np.shape(X_train))
        self.data_training = X_train

        X = new_centering(X_train, X_train)

        # Number of lines and features
        number_of_lines, number_of_features = np.shape(X_train)

        if not silent:
            print('*************')
            print('Training data')
            print('Number of data =', len(X))
            print('Number of features =', number_of_features)
            print('Number of clusters =', number_of_clusters)
            print('Reduced dimension =', number_of_dimensions)
            print('*************')

        """
            Perform TS-LPP
        """

        PseudoF_max = 0.0
        lpp_projection_for_all_sigmas = []
        outfile_labels = []

        if not silent:
            print('Searching optimized hyperparameters...')
            print('Dimension list is:', dimension_list)
            print('Sigma list is:', sigma_list)

        # Loop of hyperparameter dm: grid search for optimized hyperparameters
        for dimension_index, n_components_middle in tqdm(
                enumerate(dimension_list),
                desc=f'TS-LPP (dm,sigma) grid optimization',
                total=len(dimension_list),
        ):

            for sigma_index, sigma in enumerate(sigma_list):

                # LPP x 2
                X_middle, y_middle = compute_lpp(X, k_nearest_neighbors, sigma, n_components_middle)
                X_final, y_final = compute_lpp(X_middle, k_nearest_neighbors, sigma, number_of_dimensions)

                xx, xy = np.transpose(X_final)
                lpp_projection_for_all_sigmas.append(xx)
                lpp_projection_for_all_sigmas.append(xy)
                outfile_labels.append(str(sigma)+'_D1')
                outfile_labels.append(str(sigma)+'_D2')

                # Clustering by K means
                if self.clustering_type == 'k_means':
                    clustering_model = KMeans(n_clusters=number_of_clusters, random_state=10).fit(X_final)
                else:
                    clustering_model = SpectralClustering(n_clusters=number_of_clusters).fit(X_final)
                labels = clustering_model.labels_
                PseudoF = sklearn.metrics.calinski_harabasz_score(X_final, labels)

                if not silent:
                    print(f'Intermediate dimension = {n_components_middle}, sigma = {sigma}, pseudo F = {PseudoF}')
                    plot_ts_lpp_labels(data=X_final,
                                       labels=labels,
                                       figure_file=None, show_figure=True,
                                       sigma=sigma,
                                       dm=n_components_middle)

                if PseudoF > PseudoF_max:
                    # Update best hyperparameters
                    PseudoF_max = PseudoF
                    best_sigma = sigma
                    best_intermediate_dimensionality = n_components_middle

        # Calculate with optimal hyperparameters
        X_middle, y_middle = compute_lpp(X, k_nearest_neighbors, best_sigma, best_intermediate_dimensionality)
        X_final, y_final = compute_lpp(X_middle, k_nearest_neighbors, best_sigma, number_of_dimensions)
        clustering_model = KMeans(n_clusters=number_of_clusters, random_state=10).fit(X_final)
        labels = clustering_model.labels_

        print(
            f'Best results found for: dm = {best_intermediate_dimensionality}, '
            f'sigma = {best_sigma} with pseudo F score of {PseudoF_max}'
        )

        if not silent:
            print('')
            print('*************')
            print('Hyperparameter optimization...')
            print('Optimized sigma =', best_sigma)
            print('Optimized dm =', best_intermediate_dimensionality)
            print('*************')

        PseudoF = sklearn.metrics.calinski_harabasz_score(X_final, labels)

        if not silent:
            print('*************')
            print('clustering results')
            print('Pseudo F =', PseudoF)
            print('*************')

        self.projections_training = X_final
        self.labels_training = labels
        self.y_middle = y_middle
        self.y_final = y_final
        self.clustering_model = clustering_model

        return np.array(lpp_projection_for_all_sigmas), outfile_labels #X_final, labels, y_middle, y_final

    def transform(self, data_test):
        """
            Use trained model to transform data into low-dimensional space
        :param data_test:
        :return:
        """
        self.data_test = data_test
        normalized_test_data = new_centering(self.data_training, data_test)
        projections_test = np.dot(np.dot(normalized_test_data, self.y_middle.T), self.y_final.T)
        self.projections_test = projections_test
        return projections_test

    def predict(self, data_test):
        """
           Placeholder: predict class of test data
        :param data_test:
        :return:
        """
        transformed_data = self.transform(data_test=data_test)
        k_mean_model = self.clustering_model
        prediction = k_mean_model.predict(data_test=transformed_data)
        return prediction

    def save_labels(self):
        pass

    def save_projections(self, output_file: str = 'ts_lpp.dat', ):
        save_results(data=self.X_final, labels=self.labels_training, output_file=output_file)

    def show_projections(self):
        pass
