# -*- coding: utf-8 -*-
#####################
# Load dependencies:
#####################

#Set proper environment for rpy2
#When install rpy2 before installation
#export LD_LIBRARY_PATH="/opt/R/3.5.2/lib64/R/lib:$LD_LIBRARY_PATH"
#Then set path in python environment
#os.environ['R_HOME'] = "/opt/R/3.5.2/lib64/R/" #"/usr/lib64/R/"

import logging
logging.getLogger('numexpr').setLevel(logging.WARNING)
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logging.info('Loading dependecies...')
import os

logging.info('Remember to set, os.environ["R_HOME"] to you R lib path else r2py will cause a error to be imported...')
import rpy2.robjects as ro
from rpy2.robjects import pandas2ri
from rpy2.robjects.conversion import localconverter

import anndata as ad
import numpy as np
import pandas as pd
import pandas
import leidenalg

import pkg_resources
import tensorflow as tf 

import keras
import scanpy as scanpy

import multiprocessing as mp
import itertools
import gc

import scipy
from scipy.io import mmread

import csv

from tensorflow.keras.layers import BatchNormalization
from tensorflow.keras.optimizers import Adam

from keras import regularizers, activations, initializers, constraints
from keras import backend as K

from keras.models import Model
from keras.models import load_model

from keras.layers import InputSpec
from keras.layers import LeakyReLU
from keras.layers import Dense, Dropout
from keras.layers import Layer

from keras.callbacks import EarlyStopping, ReduceLROnPlateau,ModelCheckpoint

from keras.constraints import UnitNorm
from keras.constraints import Constraint

from keras.wrappers.scikit_learn import KerasClassifier
from keras.wrappers.scikit_learn import KerasRegressor

from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_squared_error

from scipy import sparse

import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.pyplot import rc_context
import statistics
import glob
import re

logging.basicConfig(level=logging.INFO)


#####################
# Load data:'
#####################
def load_data(omic_1, omic_2, dataset1_path=None, dataset2_path=None, *args, **kwargs):
  if dataset1_path is None:
    dataset1_path = os.getcwd()
  if dataset2_path is None:
    dataset2_path = dataset1_path
  dataset1 = kwargs.get('dataset1', None)
  dataset2 = kwargs.get('dataset2', None)
  logging.info('Detecting file_forma from available AnnData(".h5ad"), sparse matrix(".mtx",".txt"), coma separated matrix(.csv), 10XGenomics(.mtx folder), 10XGenomics(.h5 file)...')
  #####################
  #Import dataset 1
  #####################
  if dataset1:
    if dataset1.endswith('.h5ad'):  #Dataframe
      logging.info('Detected file format from -Dataset 1- is "h5ad format"...') #Dataframe - cells in rows
      print (dataset1)
      logging.info('Reading "h5ad" files...')
      par = {'input_mod1': dataset1_path + '/' + dataset1, }
      ad_mod1 = ad.read_h5ad(par['input_mod1'])
      ad_mod1_x = ad_mod1.X.toarray()
      ad_mod1 = pd.DataFrame(data=ad_mod1_x, index=ad_mod1.obs_names, columns=ad_mod1.var_names)
      logging.info('Data stored in dictionary ...')
    elif dataset1.endswith(('.mtx','.txt')):  #Dataframe
      logging.info('Detected file format from -Dataset 1- is "sparse Matrix Market mtx format"...') #Dataframe - cells in rows
      print (dataset1)
      logging.info('Reading "sparse matrix" files...')
      par = {'input_mod1': dataset1_path + '/' + dataset1}
      ad_mod1 = mmread(par['input_mod1'])
      ad_mod1 = pd.DataFrame.sparse.from_spmatrix(ad_mod1)
      logging.info('Data stored in dictionary (remember adding barcode and gene names) ...')
    elif dataset1.endswith('.csv'):
      logging.info('Detected file format from -Dataset 1- is "csv matrix"...') #Dataframe - cells in rows
      print (dataset1)
      logging.info('Reading "csv matrix" files...')
      par = {'input_mod1': dataset1_path + '/' + dataset1}
      ad_mod1 = pd.read_csv(par['input_mod1'], index_col=0)
      logging.info('Data stored in dictionary ...')
    elif dataset1.endswith('.h5'):
      logging.info('Detected file format from -Dataset 1- is "10XGenomics .h5"...') #Dataframe - cells in rows
      print (dataset1)
      logging.info('Reading ".h5" files...')
      par = {'input_mod1': dataset1_path + '/' + dataset1}
      ad_mod1 = scanpy.read_10x_h5(par['input_mod1'])
      ad_mod1.var_names_make_unique()
      ad_mod1_x = ad_mod1.X.toarray()
      ad_mod1 = pd.DataFrame(data=ad_mod1_x, index=ad_mod1.obs_names, columns=ad_mod1.var_names)
      logging.info('Calling ".var_names_make_unique" ...')
      logging.info('Data stored in dictionary ...')
    else: 
      print("Dataset 1 is not from any of available input formats, import it manually.")
  elif dataset1 is None:
      logging.info('Detected file format from -Dataset 1- is "10X genomics (mtx)"...') #Dataframe - cells in rows
      logging.info('Reading "10X genomics" files...')
      ad_mod1 = scanpy.read_10x_mtx(dataset1_path, var_names='gene_symbols', cache=True)
      ad_mod1_x = ad_mod1.X.toarray()
      ad_mod1 = pd.DataFrame(data=ad_mod1_x, index=ad_mod1.obs_names, columns=ad_mod1.var_names)
      logging.info('Data stored in dictionary ...')   
  else: 
    print("Dataset 1 is not a -10X Genomics format-, import it manually.")   
  #####################
  #Import dataset 2
  #####################
  if dataset2:
    if dataset2.endswith('.h5ad'):
      logging.info('Detected file format from -Dataset 2- is "h5ad format"...')
      print (dataset2)
      logging.info('Reading "h5ad" files...')
      par = {'input_mod2': dataset2_path + '/' + dataset2, }
      ad_mod2 = ad.read_h5ad(par['input_mod2'])
      ad_mod2_x = ad_mod2.X.toarray()
      ad_mod2 = pd.DataFrame(data=ad_mod2_x, index=ad_mod2.obs_names, columns=ad_mod2.var_names)
      logging.info('Data stored in dictionary ...')
    elif dataset2.endswith(('.mtx','.txt')):
      logging.info('Detected file format from -Dataset 2- is "sparse Matrix Market mtx format"...')
      print (dataset2)
      logging.info('Reading "sparse matrix" files...')
      par = {'input_mod2': dataset2_path + '/' + dataset2}
      ad_mod2 = mmread(par['input_mod2'])
      ad_mod2 = pd.DataFrame.sparse.from_spmatrix(ad_mod2)
      logging.info('Data stored in dictionary (remember adding barcode and gene names) ...')
    elif dataset2.endswith('.csv'):
      logging.info('Detected file format from -Dataset 1- is "csv matrix"...')
      print (dataset2)
      logging.info('Reading "csv matrix" files...')
      par = {'input_mod2': dataset2_path + '/' + dataset2}
      ad_mod2 = pd.read_csv(par['input_mod2'], index_col=0)
      logging.info('Data stored in dictionary ...')
    elif dataset1.endswith('.h5'):
      logging.info('Detected file format from -Dataset 2- is "10XGenomics .h5"...')
      print (dataset1)
      logging.info('Reading ".h5" files...')
      par = {'input_mod2': dataset2_path + '/' + dataset2}
      ad_mod2 = scanpy.read_10x_h5(par['input_mod2'])
      ad_mod2.var_names_make_unique()
      ad_mod2_x = ad_mod2.X.toarray()
      ad_mod2 = pd.DataFrame(data=ad_mod2_x, index=ad_mod2.obs_names, columns=ad_mod2.var_names)
      logging.info('Calling ".var_names_make_unique" ...')
      logging.info('Data stored in dictionary ...')
    else: 
      print("Dataset 2 is not from any of available input formats, import it manually.")
  elif dataset2 is None:
      logging.info('Detected file format from -Dataset 2- is "10X genomics (mtx)"...')
      logging.info('Reading "10X genomics" files...')
      ad_mod2 = scanpy.read_10x_mtx(dataset2_path, var_names='gene_symbols', cache=True)
      ad_mod2_x = ad_mod2.X.toarray()
      ad_mod2 = pd.DataFrame(data=ad_mod2_x, index=ad_mod2.obs_names, columns=ad_mod2.var_names)
      logging.info('Data stored in dictionary ...')   
  else: 
    print("Dataset 2 is not a -10X Genomics format-, import it manually.") 
  imported_data = {omic_1: ad_mod1, omic_2: ad_mod2}
  return imported_data   

#####################
# LIBRA model structure generator:
#####################
def createmodel(n_layers,n_nodes,alpha,dropout,batch_size,mid_layer,ncol_mod_1,ncol_mod_2):
  model = keras.Sequential()
  for i in range(0, n_layers):
    if i==0:
    #Input_layer
      model.add(Dense(n_nodes, input_dim=ncol_mod_1))
      model.add(LeakyReLU(alpha=alpha))
      model.add(Dropout(dropout))
    #intermediate_encoder_layers
    else:
      model.add(Dense(n_nodes/(2*i)))
      model.add(LeakyReLU(alpha=alpha))
      model.add(Dropout(dropout))
  #middle_layer
  model.add(Dense(mid_layer, name = 'Bottleneck'))
  model.add(LeakyReLU(alpha=alpha))
  model.add(Dropout(dropout))
    #intermediate_decoder_layers    
  for i in range(n_layers-1, -1, -1):
    if i!=0:
      model.add(Dense(n_nodes/(2*i)))
      model.add(LeakyReLU(alpha=alpha))
      model.add(Dropout(dropout))  
    else:
      model.add(Dense(n_nodes))
      model.add(LeakyReLU(alpha=alpha))
      #model.add(Dropout(dropout))          
  #Output_layer
  model.add(Dense(ncol_mod_2, activation='relu', name = 'Output'))
  return model

#####################
# LIBRA parallel training structure:
#####################
def fast_tune(n_layers,n_nodes,alpha,dropout,batch_size,mid_layer,ncol_mod_1,ncol_mod_2,cell_names,ad_mod1_ndarray,ad_mod2_ndarray):
  ad_mod1_ndarray = ad_mod1_ndarray.todense()
  ad_mod2_ndarray = ad_mod2_ndarray.todense()
  #Set environment folders to store data
  cwd = os.getcwd()
  if not os.path.exists('LIBRA_outputs'):
    os.mkdir('LIBRA_outputs')
  path = cwd + "/LIBRA_outputs"
  if not os.path.exists('LIBRA_outputs/Models'):
    os.mkdir(path + '/Models')
  path = cwd + "/LIBRA_outputs" + "/Models" + "/model_"
  full_name = path + 'n_layers' + str(n_layers) + '_' + 'n_nodes' + str(n_nodes) + '_' + 'alpha' + str(alpha) + '_' + 'dropout' + str(dropout) + '_' + 'batch_size' + str(batch_size) + '_' + 'mid_layer' + str(mid_layer) + '.hdf5'
  #Create model
  model = createmodel(n_layers,n_nodes,alpha,dropout,batch_size,mid_layer,ncol_mod_1,ncol_mod_2)
  print(model.summary())
  #compile
  model.compile(optimizer = Adam(learning_rate=0.001), loss='mean_squared_error')
  #callbacks
  early_stop = EarlyStopping(monitor='loss', mode='min', verbose=1 ,patience=20)
  lr_plateau_callback = ReduceLROnPlateau(monitor="loss", factor=0.1, patience=15, min_lr=0.00001, verbose = 1)
  checkpoint = tf.keras.callbacks.ModelCheckpoint(
      filepath=full_name,
      save_weights_only=False,
      monitor='loss',
      mode='min',
      save_best_only=True,
      verbose=1)
  logging.info('Training model...')
  #fit
  trained_model= model.fit(ad_mod1_ndarray, ad_mod2_ndarray, epochs=1500, batch_size=7000, validation_split = 0, verbose = 0, shuffle = True, callbacks=[early_stop, lr_plateau_callback, checkpoint])    
  logging.info('LIBRA generating and storing model at {full_name}...'.format(full_name=full_name))    
  #Retrieve middle_layer from trained_model / integration - shared space
  layer_name = 'Bottleneck'
  intermediate_layer_model = Model(inputs=model.input,
                                   outputs=model.get_layer(layer_name).output)
  intermediate_output = intermediate_layer_model.predict(ad_mod1_ndarray)
  #Esport to csv the embedding "LIBRA_components"
  middle_layer =pd.DataFrame(intermediate_output)
  middle_layer.index = cell_names
  #Set environment folders to store data
  path = cwd + "/LIBRA_outputs"
  if not os.path.exists('LIBRA_outputs/Integration'):
    os.mkdir(path + '/Integration')
  path = cwd + "/LIBRA_outputs" + "/Integration" + "/test_"
  full_name = path + 'n_layers' + str(n_layers) + '_' + 'n_nodes' + str(n_nodes) + '_' + 'alpha' + str(alpha) + '_' + 'dropout' + str(dropout) + '_' + 'batch_size' + str(batch_size) + '_' + 'mid_layer' + str(mid_layer) + '.csv'
  logging.info('LIBRA generating and storing integration shared space at {full_name}...'.format(full_name=full_name)) 
  middle_layer.to_csv(path
  + 'n_layers' + str(n_layers) 
  + '_' + 'n_nodes' + str(n_nodes) 
  + '_' + 'alpha' + str(alpha) 
  + '_' + 'dropout' + str(dropout) 
  + '_' + 'batch_size' + str(batch_size) 
  + '_' + 'mid_layer' + str(mid_layer) 
  + '.csv', index=True) 
  del(model)
  del(trained_model)
  del(intermediate_layer_model)
  del(intermediate_output)
  del(middle_layer)
  tf.keras.backend.clear_session()
  gc.collect()

#####################
# LIBRA training:
#####################
def libra(input_dict, training_mode=None, n_top_genes=None, n_jobs=None, *args, **kwargs):
  #####################
  #Setting hyperparameters fom LIBRA model
  #####################
  if training_mode is None or training_mode == 'default':
    training_mode = 'default'
    #Default   
    n_layers = kwargs.get('n_layers', [2])
    n_nodes = kwargs.get('n_nodes', [512])
    alpha = kwargs.get('alpha', [0.3])
    dropout = kwargs.get('dropout', [0.2])
    batch_size = kwargs.get('batch_size', [7000])
    mid_layer = kwargs.get('mid_layer', [10])
    logging.info('Training model selected is "default". Hyperparameters are(all possible combinations): n_layers{n_layers}, n_nodes{n_nodes}, alpha={alpha}, dropout={dropout}, batch_size={batch_size}, mid_layer={mid_layer}'.format(n_layers=n_layers, n_nodes=n_nodes, alpha=alpha, dropout=dropout, batch_size=batch_size, mid_layer=mid_layer))
  elif training_mode == 'fine_tune_prediction':
    training_mode = 'fine_tune_prediction'
    #Prediction
    n_layers = kwargs.get('n_layers', [1,2])
    n_nodes = kwargs.get('n_nodes', [64,128,256,512])
    alpha = kwargs.get('alpha', [0.1,0.3,0.5])
    dropout = kwargs.get('dropout', [0.1,0.2])
    batch_size = kwargs.get('batch_size', [32,64,128,7000])
    mid_layer = kwargs.get('mid_layer', [10,30,50,70,100])  
    logging.info('Training model selected is "fine_tune_prediction". Hyperparameters are(all possible combinations): n_layers{n_layers}, n_nodes{n_nodes}, alpha={alpha}, dropout={dropout}, batch_size={batch_size}, mid_layer={mid_layer}'.format(n_layers=n_layers, n_nodes=n_nodes, alpha=alpha, dropout=dropout, batch_size=batch_size, mid_layer=mid_layer))
  elif training_mode == 'fine_tune_integration':
    training_mode = 'fine_tune_integration'
    #Integration
    n_layers = kwargs.get('n_layers', [1,2,3,4,5,6])
    n_nodes = kwargs.get('n_nodes', [256,512,1024,2048])
    alpha = kwargs.get('alpha', [0.1,0.3,0.5])
    dropout = kwargs.get('dropout', [0.1,0.2,0.3,0.4])
    batch_size = kwargs.get('batch_size', [7000])
    mid_layer = kwargs.get('mid_layer', [10,30,50,70])
    logging.info('Training model selected is "fine_tune_integration". Hyperparameters are(all possible combinations): n_layers{n_layers}, n_nodes{n_nodes}, alpha={alpha}, dropout={dropout}, batch_size={batch_size}, mid_layer={mid_layer}'.format(n_layers=n_layers, n_nodes=n_nodes, alpha=alpha, dropout=dropout, batch_size=batch_size, mid_layer=mid_layer))
  elif training_mode == 'custom':
    training_mode = 'custom'
    n_layers = kwargs.get('n_layers', None)
    n_nodes = kwargs.get('n_nodes', None)
    alpha = kwargs.get('alpha', None)
    dropout = kwargs.get('dropout', None)
    batch_size = kwargs.get('batch_size', None)
    mid_layer = kwargs.get('mid_layer', None)
    logging.info('Training model selected is "custom". Hyperparameters are(all possible combinations): n_layers{n_layers}, n_nodes{n_nodes}, alpha={alpha}, dropout={dropout}, batch_size={batch_size}, mid_layer={mid_layer}'.format(n_layers=n_layers, n_nodes=n_nodes, alpha=alpha, dropout=dropout, batch_size=batch_size, mid_layer=mid_layer))
    if n_layers is None or n_nodes is None or alpha is None or dropout is None or batch_size is None or mid_layer is None:
      logging.info('Grid parameters should by filled for -training_mode="custom"- (n_layers,n_nodes,alpha,dropout,batch_size and mid_layer should by specify)...')   
  else:
    logging.info('Training mode option is not valid, try with "None" or training_mode="default" or training_mode="fine_tune_prediction" or training_mode="fine_tune_integration" or training_mode="custom"...')
  #####################
  #Cheker for RNA features
  #####################
  if "RNA" in input_dict:
    if n_top_genes is None:
      n_top_genes = kwargs.get('n_top_genes', 2000)
    else:
      n_top_genes = kwargs.get('n_top_genes', n_top_genes)
    logging.info('Filtering RNA features to n_top_genes={n_top_genes} most HVG...'.format(n_top_genes=n_top_genes))
    #scanpy for MVG obtain
    adata = scanpy.AnnData(input_dict['RNA'])
    scanpy.pp.highly_variable_genes(adata, n_top_genes=n_top_genes) #round(len(adata.var_names)*0.4)
    adata = adata[:, adata.var.highly_variable]
    input_dict['RNA']= input_dict['RNA'][np.array(adata.var_names)]
  #numpy ndarray generation for model input/output
  ad_mod1_ndarray = input_dict[list(input_dict)[:2][0]].values[:,0:(input_dict[list(input_dict)[:2][0]].shape[1])]
  ad_mod2_ndarray = input_dict[list(input_dict)[:2][1]].values[:,0:(input_dict[list(input_dict)[:2][1]].shape[1])]
  cell_names = input_dict[list(input_dict)[:2][0]].index
  #ncol for datasets
  ncol_mod_1 = ad_mod1_ndarray.shape[1]
  ncol_mod_2 = ad_mod2_ndarray.shape[1]
  logging.info('Final shapes of omics: omic_1={omic_1} and omic_2={omic_2}'.format(omic_1=input_dict[list(input_dict)[:2][0]].shape, omic_2=input_dict[list(input_dict)[:2][1]].shape))
  #####################
  #model parallel train
  #####################
  #Generating all possible combinations from hyperparameters
  ncol_mod_1=list([ncol_mod_1])
  ncol_mod_2=list([ncol_mod_2])
  logging.info('Transforming omic_1 and omic_2 into sparse matrix for parallelize pool size limitations overcome...')
  ad_mod1_ndarray = sparse.csr_matrix(ad_mod1_ndarray)
  ad_mod2_ndarray = sparse.csr_matrix(ad_mod2_ndarray)
  a = [n_layers,n_nodes,alpha,dropout,batch_size,mid_layer,ncol_mod_1,ncol_mod_2,list([cell_names]),list([ad_mod1_ndarray]),list([ad_mod2_ndarray])]
  input = list(itertools.product(*a))
  #Set how many models should by trained at same time
  if n_jobs is None:
    n_jobs = 1
    logging.info('Models training 1 by 1. If desired multiple models parallel training then set attribute "n_jobs=value"...')
  else:
    n_jobs = n_jobs
    logging.info('Models training with parallel value of: n_jobs={n_jobs}. Ensure sufficient memory is available else reduce n_jobs value'.format(n_jobs=n_jobs))
  pool = mp.Pool(processes=n_jobs)
  pool.starmap(fast_tune, input) 
  pool.close()
  pool.terminate()
  del(pool)
  return [ad_mod1_ndarray,ad_mod2_ndarray]

#####################
# LIBRA prediction:
#####################
def libra_predict(model, input_data, to_predict, *args, **kwargs):
  if to_predict == 'modality_B':
    logging.info('Using input modality to predict "output modality" using trained model assigned...')
    layer_name = 'Output'
  elif to_predict == 'integrated_space':
    logging.info('Using input modality to predict "integrated shared space" using trained model assigned...')
    layer_name = 'Bottleneck'
  output_layer_model = Model(inputs=model.input, outputs=model.get_layer(layer_name).output)
  output_output = output_layer_model.predict(input_data)
  return output_output

#####################
# LIBRA model 2 structure generator:
#####################
def createmodel_2(n_layers,n_nodes,alpha,dropout,batch_size,mid_layer,ncol_mod_1,ncol_mod_2):
  model = keras.Sequential()
  for i in range(0, n_layers):
    if i==0:
    #Input_layer
      model.add(Dense(n_nodes, input_dim=ncol_mod_1))
      model.add(LeakyReLU(alpha=alpha))
      model.add(Dropout(dropout))
    #intermediate_encoder_layers
    else:
      model.add(Dense(n_nodes/(2*i)))
      model.add(LeakyReLU(alpha=alpha))
      model.add(Dropout(dropout))
  #middle_layer
  model.add(Dense(mid_layer, name = 'Bottleneck'))
  model.add(LeakyReLU(alpha=alpha))
  #model.add(Dropout(dropout))
    #intermediate_decoder_layers        
  #Output_layer
  model.add(Dense(ncol_mod_2, activation='relu', name = 'Output'))
  return model

#####################
# LIBRA parallel training structure 2:
#####################
def fast_tune_2(n_layers,n_nodes,alpha,dropout,batch_size,mid_layer,ncol_mod_1,ad_mod1_ndarray,ad_mod2_ndarray):
  ad_mod1_ndarray = ad_mod1_ndarray.todense()
  ad_mod2_ndarray = ad_mod2_ndarray.todense()
  #ncol for datasets
  ncol_mod_2 = ad_mod2_ndarray.shape[1]
  logging.info('Final shapes of omics: omic_1={omic_1} and omic_2={omic_2}'.format(omic_1=ad_mod1_ndarray.shape, omic_2=ad_mod2_ndarray.shape))
  #Set environment folders to store data
  cwd = os.getcwd()
  if not os.path.exists('LIBRA_outputs'):
    os.mkdir('LIBRA_outputs')
  path = cwd + "/LIBRA_outputs"
  if not os.path.exists('LIBRA_outputs/supp_Models'):
    os.mkdir(path + '/supp_Models')
  path = cwd + "/LIBRA_outputs" + "/supp_Models" + "/supp_model_"
  full_name = path + 'n_layers' + str(n_layers) + '_' + 'n_nodes' + str(n_nodes) + '_' + 'alpha' + str(alpha) + '_' + 'dropout' + str(dropout) + '_' + 'batch_size' + str(batch_size) + '_' + 'mid_layer' + str(mid_layer) + '.hdf5'
  #Create model
  model = createmodel_2(n_layers,n_nodes,alpha,dropout,batch_size,mid_layer,ncol_mod_1,ncol_mod_2)
  print(model.summary())
  #compile
  model.compile(optimizer = Adam(learning_rate=0.001), loss='mean_squared_error')
  #callbacks
  early_stop = EarlyStopping(monitor='loss', mode='min', verbose=1 ,patience=20)
  lr_plateau_callback = ReduceLROnPlateau(monitor="loss", factor=0.1, patience=15, min_lr=0.00001, verbose = 1)
  checkpoint = tf.keras.callbacks.ModelCheckpoint(
      filepath=full_name,
      save_weights_only=False,
      monitor='loss',
      mode='min',
      save_best_only=True,
      verbose=1)
  logging.info('Training model...')
  #fit
  trained_model= model.fit(ad_mod1_ndarray, ad_mod2_ndarray, epochs=1500, batch_size=7000, validation_split = 0, verbose = 0, shuffle = True, callbacks=[early_stop, lr_plateau_callback, checkpoint])    
  logging.info('LIBRA generating and storing model at {full_name}...'.format(full_name=full_name))    
  #Retrieve middle_layer from trained_model / integration - shared space
  layer_name = 'Output'
  output_layer_model = Model(inputs=model.input,
                                   outputs=model.get_layer(layer_name).output)
  output_output = output_layer_model.predict(ad_mod1_ndarray)
  #Esport to csv the embedding "LIBRA_components"
  middle_layer =pd.DataFrame(output_output)
  #Compute 'nn_consistency' metric 
  distance_vector = []
  for i in range(0, ad_mod2_ndarray.shape[0]):
    distance_vector.append(np.linalg.norm(ad_mod2_ndarray[i,]-output_output[i,]))
  #Export values
  logging.info('Exporting cell euclidean distance values...')
  full_name = path + 'n_layers' + str(n_layers) + '_' + 'n_nodes' + str(n_nodes) + '_' + 'alpha' + str(alpha) + '_' + 'dropout' + str(dropout) + '_' + 'batch_size' + str(batch_size) + '_' + 'mid_layer' + str(mid_layer) + '.csv'
  distance_matrix = pd.DataFrame({'Euclidean_distance':distance_vector})
  distance_matrix.to_csv(full_name)
  #Compute multi-modal distances
  #
  #From Python to R data.frame
  with localconverter(ro.default_converter + pandas2ri.converter):
    dataset1 = ro.conversion.py2rpy(distance_matrix)
  #
  #Apply the R code to data
  r = ro.r
  r['source'](os.path.join(os.path.dirname(__file__), "supp_functions_R.R"))
  #r['source']('/datos_2/phD_raw_data_2/OUTPUTS_2_ae_peaks_test_7_100pcent/q0/Summer_phase_1_data/final_final_phase/starter_kit-joint_embedding-r/output/datasets_phase2/joint_embedding/openproblems_bmmc_multiome_phase2/funcion_R.R')
  filter_function_r = ro.globalenv['biomodal_distances']
  df_result_r = filter_function_r(dataset1)
  #
  #From R to Python data.frame
  with localconverter(ro.default_converter + pandas2ri.converter):
    pd_from_r_df = ro.conversion.rpy2py(df_result_r)
  #
  pd_from_r_df.index = ['Mean', 'Median', 'Sd']
  #
  #Export bimodal-distances 
  logging.info('Exporting cell euclidean distance values...')
  full_name = path + 'n_layers' + str(n_layers) + '_' + 'n_nodes' + str(n_nodes) + '_' + 'alpha' + str(alpha) + '_' + 'dropout' + str(dropout) + '_' + 'batch_size' + str(batch_size) + '_' + 'mid_layer' + str(mid_layer) + '_biomodal_distances.csv'
  pd_from_r_df.to_csv(full_name)
  #
  #Export plot
  logging.info('Exporting cell euclidean distance plot...')
  full_name = path + 'n_layers' + str(n_layers) + '_' + 'n_nodes' + str(n_nodes) + '_' + 'alpha' + str(alpha) + '_' + 'dropout' + str(dropout) + '_' + 'batch_size' + str(batch_size) + '_' + 'mid_layer' + str(mid_layer) + '.pdf'
  g = sns.distplot(distance_vector, hist=False)
  g.set_xlabel("Euclidean distance between paired cells", fontsize = 10)
  g.set_ylabel("Number of cells", fontsize = 10)
  mean = statistics.mean(distance_vector)
  median = statistics.median(distance_vector)
  plt.axvline(mean, linestyle ="--", color ='red', label='Mean = ' + str(mean))
  plt.axvline(median, linestyle ="--", color ='blue', label='Median = ' + str(median))
  plt.legend(loc='upper right')
  plt.savefig(full_name)
  plt.close()
  #
  del(model)
  del(trained_model)
  del(middle_layer)
  tf.keras.backend.clear_session()
  gc.collect()
  return distance_vector

#####################
# LIBRA metrics:
#####################
def libra_metrics(input_dict, metric, cluster_origin=None, n_neighbors=None, resolution=None, path_to_libra_outputs=None, libra_output=None, n_jobs=None, *args, **kwargs):    
  if metric == 'nn_consistency':
    #Integrated space to decoded-to-Integrated-space euclidean distances (NN-QC score): Subspaces - Euclidean distance
    #Load data
    if path_to_libra_outputs is None:
      cwd = os.getcwd()
      path_to_libra_outputs = cwd + "/LIBRA_outputs" + "/Integration"
      logging.info('Loading input data from: path_to_libra_outputs={path_to_libra_outputs}'.format(path_to_libra_outputs=path_to_libra_outputs))
    else:
      path_to_libra_outputs = path_to_libra_outputs
      logging.info('Loading input data from: path_to_libra_outputs={path_to_libra_outputs}'.format(path_to_libra_outputs=path_to_libra_outputs))
    if libra_output is None:
      mode = 'multiple'
      logging.info('Metric will be computed over all available LIBRA output_files in the folder...')
      libra_output_files = glob.glob(path_to_libra_outputs + '/' + 'test_n_*.csv')
      libra_output_list = []
      for file in libra_output_files:
        df = pd.read_csv(file, index_col=0)
        libra_output_list.append(df)
    else:
      mode = 'single'
      logging.info('Metric will be computed over LIBRA output selected...')
      path_to_libra_outputs = path_to_libra_outputs + '/'+ libra_output
      libra_output_list = [pd.read_csv(path_to_libra_outputs, index_col=0)]
    #input_files_list
    logging.info('Training embedding sub-network to Integrated subspace...')
    #numpy ndarray generation for model input/output
    ad_mod1_ndarray = input_dict[0]
    #ncol for datasets
    ncol_mod_1 = ad_mod1_ndarray.shape[1]  
    #####################
    #model parallel train
    #####################
    logging.info('Transforming omic_1 and omic_2 into sparse matrix for parallelize pool size limitations overcome...')
    ad_mod1_ndarray = sparse.csr_matrix(ad_mod1_ndarray) 
    libra_output_files = [x[-76:] for x in libra_output_files]
    hyper_params_list = []
    for element in libra_output_files:
      hyper_params_list.append(re.findall("\d*\.?\d+", element))
    hyper_params_list = [[(float(j)) for j in i] for i in hyper_params_list]
    for element in hyper_params_list:
      element[0]=int(element[0])
      element[1]=int(element[1])
      element[4]=int(element[4])
      element[5]=int(element[5])
    input = [tuple(x) for x in hyper_params_list]
    for n in range(len(input)):
      input[n] = input[n] + (ncol_mod_1,) + (ad_mod1_ndarray,) + (sparse.csr_matrix(libra_output_list[n]),)  
    #Set how many models should by trained at same time
    if n_jobs is None:
      n_jobs = 1
      logging.info('Models training 1 by 1. If desired multiple models parallel training then set attribute "n_jobs=value"...')
    else:
      n_jobs = n_jobs
      logging.info('Models training with parallel value of: n_jobs={n_jobs}. Ensure sufficient memory is available else reduce n_jobs value'.format(n_jobs=n_jobs))
    pool = mp.Pool(processes=n_jobs)
    pool.starmap(fast_tune_2, input) 
    pool.close()
    pool.terminate()
    del(pool) 
  if metric == 'nn_mse':
    #LIBRA MSE, prediction vs real output
    #Load data
    if path_to_libra_outputs is None:
      cwd = os.getcwd()
      path_to_libra_outputs = cwd + "/LIBRA_outputs" + "/Models"
      logging.info('Loading input data from: path_to_libra_outputs={path_to_libra_outputs}'.format(path_to_libra_outputs=path_to_libra_outputs))
    else:
      path_to_libra_outputs = path_to_libra_outputs
      logging.info('Loading input data from: path_to_libra_outputs={path_to_libra_outputs}'.format(path_to_libra_outputs=path_to_libra_outputs))
    if libra_output is None:
      mode = 'multiple'
      logging.info('Metric will be computed over all available LIBRA output_files in the folder...')
      libra_output_files = glob.glob(path_to_libra_outputs + '/' + 'model_n_*.hdf5')
      libra_output_mse_list = []
      ad_mod1_ndarray = input_dict[0].todense()
      ad_mod2_ndarray = input_dict[1].todense()
      layer_name = 'Output'
      for model in libra_output_files:
        model = load_model(model)
        output_layer_model = Model(inputs=model.input, outputs=model.get_layer(layer_name).output)
        output_output = output_layer_model.predict(ad_mod1_ndarray) 
        mse = mean_squared_error(ad_mod2_ndarray, output_output)
        libra_output_mse_list.append(mse)
      full_name = path_to_libra_outputs + '/' + 'MSE_table_.csv'
      libra_output_mse_matrix = pd.DataFrame({'MSE':libra_output_mse_list})
      libra_output_mse_matrix.index = [x[-78:] for x in libra_output_files]
      #Export mse matrix 
      logging.info('Exporting models MSE matrix...')
      libra_output_mse_matrix.to_csv(full_name)
    else:
      mode = 'single'
      layer_name = 'Output'
      ad_mod1_ndarray = input_dict[0].todense()
      ad_mod2_ndarray = input_dict[1].todense()
      logging.info('Metric will be computed over LIBRA output selected...')
      libra_output_mse_list = []
      path_to_libra_outputs = path_to_libra_outputs + '+' + libra_output
      model = load_model(path_to_libra_outputs)
      output_layer_model = Model(inputs=model.input, outputs=model.get_layer(layer_name).output)
      output_output = output_layer_model.predict(ad_mod1_ndarray) 
      mse = mean_squared_error(ad_mod2_ndarray, output_output)
      libra_output_mse_list.append(mse)  
      full_name = path_to_libra_outputs + '/' + 'MSE_table_.csv'
      libra_output_mse_matrix = pd.DataFrame({'MSE':libra_output_mse_list})
      libra_output_mse_matrix.index = [x[-78:] for x in libra_output_files]
      #Export mse matrix
      logging.info('Exporting models MSE matrix...')
      libra_output_mse_matrix.to_csv(full_name)  
  if metric == 'ppji':
    if n_neighbors is None:
      n_neighbors = 10
    if resolution is None:
      resolution = 1
    if cluster_origin is None:
      logging.info('Remember to add reference clustering input to: cluster_origin, input parameter else PPJI cant be computed.')
    else:
      #Preserver Pairwise Jacard Index
      #Load data
      if path_to_libra_outputs is None:
        cwd = os.getcwd()
        path_to_libra_outputs = cwd + "/LIBRA_outputs" + "/Integration"
        logging.info('Loading input data from: path_to_libra_outputs={path_to_libra_outputs}'.format(path_to_libra_outputs=path_to_libra_outputs))
      else:
        path_to_libra_outputs = path_to_libra_outputs
        logging.info('Loading input data from: path_to_libra_outputs={path_to_libra_outputs}'.format(path_to_libra_outputs=path_to_libra_outputs))
      if libra_output is None:
        mode = 'multiple'
        logging.info('Metric will be computed over all available LIBRA output_files in the folder...')
        libra_output_files = glob.glob(path_to_libra_outputs + '/' + 'test_n_*.csv')
        libra_output_list = []
        for file in libra_output_files:
          df = pd.read_csv(file, index_col=0)
          libra_output_list.append(df)
        count=0
        ppji_values_vector = []
        ppji_values_vector_names = []
        for output in libra_output_list:
          adata = scanpy.AnnData(output)
          adata.obsm['X_pca'] = adata.X
          logging.info('Computing, neighbors, umap and leiden clustering over LIBRA latent space...')
          scanpy.pp.neighbors(adata, n_neighbors=n_neighbors, n_pcs=adata.X.shape[1])
          scanpy.tl.umap(adata)
          scanpy.tl.leiden(adata, resolution=resolution)
          scanpy.settings.figdir = path_to_libra_outputs + '/'
          logging.info('Exporting UMAP plot...')
          with rc_context({'figure.figsize': (8, 8)}):
            scanpy.pl.umap(adata, color=['leiden'], save='_' + [x[-76:-4] for x in libra_output_files][count] +'.pdf')
          #cell to cluster matrix export  
          libra_clustering_output = adata.obs['leiden']
          logging.info('Exporting clustering matrix...')
          libra_clustering_output.to_csv(path_to_libra_outputs + '/' + 'clusters_' + [x[-76:-4] for x in libra_output_files][count] + '.csv') 
          #Computing PPJI
          logging.info('Computing PPJI metric and exporting results...') 
          latent_clustering_matrix = pd.to_numeric(adata.obs['leiden'])
          latent_clustering_matrix= latent_clustering_matrix.reset_index(drop=True).to_frame()
          latent_clustering_matrix = latent_clustering_matrix["leiden"]
          #
          #From Python to R data.frame
          with localconverter(ro.default_converter + pandas2ri.converter):
            dataset1 = ro.conversion.py2rpy(latent_clustering_matrix) 
          #
          if isinstance(cluster_origin, pandas.core.frame.DataFrame):
            logging.info('Transforming cluster_origin pandas_DataFrame to pandas_Series...')
            #
            cluster_origin_name = cluster_origin.columns.values[1]
            cluster_origin = cluster_origin[cluster_origin_name].squeeze()
            with localconverter(ro.default_converter + pandas2ri.converter):
              cluster_origin = ro.conversion.py2rpy(cluster_origin)       
          if isinstance(cluster_origin, pandas.core.series.Series):
            with localconverter(ro.default_converter + pandas2ri.converter):
              cluster_origin = ro.conversion.py2rpy(cluster_origin)   
          #
          #Apply the R code to data
          name = path_to_libra_outputs + '/' + 'clusters_' + [x[-76:-4] for x in libra_output_files][count]
          r = ro.r
          r['source'](os.path.join(os.path.dirname(__file__), "supp_functions_R.R"))
          #r['source']('/datos_2/phD_raw_data_2/base-folder/sc_libra/supp_functions_R.R')
          filter_function_r = ro.globalenv['ppji']
          df_result_r = filter_function_r(dataset1,cluster_origin,name)
          #
          #From R to Python data.frame
          with localconverter(ro.default_converter + pandas2ri.converter):
            pd_from_r_df = ro.conversion.rpy2py(df_result_r)
          #
          pd_from_r_df = float(pd_from_r_df[0])
          ppji_values_vector.append(pd_from_r_df)
          name = [x[-76:-4] for x in libra_output_files][count]
          ppji_values_vector_names.append(name) 
          count=count+1     
        pd_from_r_df = pd.DataFrame (ppji_values_vector, columns = ['PPJI'])
        pd_from_r_df.index = ppji_values_vector_names
        #
        #Export bimodal-distances 
        logging.info('Exporting ppji values into a summarized matrix...')
        full_name = path_to_libra_outputs + 'PPJI_values_summary_matrix.csv'
        pd_from_r_df.to_csv(full_name)
        #  
      else:
        mode = 'single'
        ppji_values_vector = []
        ppji_values_vector_names = []
        logging.info('Metric will be computed over LIBRA output selected...')
        path_to_libra_outputs = path_to_libra_outputs + '/' + libra_output
        libra_output_list = [pd.read_csv(path_to_libra_outputs, index_col=0)]
        path_to_libra_outputs = cwd + "/LIBRA_outputs" + "/Integration"
        #
        output = libra_output_list[0]
        adata = scanpy.AnnData(output)
        adata.obsm['X_pca'] = adata.X
        logging.info('Computing, neighbors, umap and leiden clustering over LIBRA latent space...')
        scanpy.pp.neighbors(adata, n_neighbors=10, n_pcs=adata.X.shape[1])
        scanpy.tl.umap(adata)
        scanpy.tl.leiden(adata)
        scanpy.settings.figdir = path_to_libra_outputs + '/'
        logging.info('Exporting UMAP plot...')
        with rc_context({'figure.figsize': (8, 8)}):
          scanpy.pl.umap(adata, color=['leiden'], save='_' + [x[-76:-4] for x in libra_output_files][count] +'.pdf')
        #cell to cluster matrix export  
        libra_clustering_output = adata.obs['leiden']
        logging.info('Exporting clustering matrix...')
        libra_clustering_output.to_csv(path_to_libra_outputs + '/' + 'clusters_' + [x[-76:-4] for x in libra_output_files][count] + '.csv') 
        #Computing PPJI
        logging.info('Computing PPJI metric and exporting results...') 
        latent_clustering_matrix = adata.obs['leiden']  
        #
        #From Python to R data.frame
        with localconverter(ro.default_converter + pandas2ri.converter):
          dataset1 = ro.conversion.py2rpy(latent_clustering_matrix)
        #
        if isinstance(cluster_origin, pandas.core.frame.DataFrame):
          logging.info('Transforming cluster_origin pandas_DataFrame to pandas_Series...')
          #
          cluster_origin_name = cluster_origin.columns.values[1]
          cluster_origin = cluster_origin[cluster_origin_name].squeeze()
          with localconverter(ro.default_converter + pandas2ri.converter):
            cluster_origin = ro.conversion.py2rpy(cluster_origin)       
        if isinstance(cluster_origin, pandas.core.series.Series):
          with localconverter(ro.default_converter + pandas2ri.converter):
            cluster_origin = ro.conversion.py2rpy(cluster_origin)   
        #
        #Apply the R code to data
        name = path_to_libra_outputs + '/' + 'clusters_' + [x[-76:-4] for x in libra_output_files][count]
        r = ro.r
        r['source'](os.path.join(os.path.dirname(__file__), "supp_functions_R.R"))
        #r['source']('/datos_2/phD_raw_data_2/OUTPUTS_2_ae_peaks_test_7_100pcent/q0/Summer_phase_1_data/final_final_phase/starter_kit-joint_embedding-r/output/datasets_phase2/joint_embedding/openproblems_bmmc_multiome_phase2/funcion_R.R')
        filter_function_r = ro.globalenv['ppji']
        df_result_r = filter_function_r(dataset1,cluster_origin,name)
        #
        #From R to Python data.frame
        with localconverter(ro.default_converter + pandas2ri.converter):
          pd_from_r_df = ro.conversion.rpy2py(df_result_r)
        #
        pd_from_r_df = float(pd_from_r_df[0])
        ppji_values_vector.append(pd_from_r_df)
        name = [x[-76:-4] for x in libra_output_files][count]
        ppji_values_vector_names.append(name) 
        #
        pd_from_r_df = pd.DataFrame (ppji_values_vector, columns = ['PPJI'])
        pd_from_r_df.index = ppji_values_vector_names
        #
        #Export bimodal-distances 
        logging.info('Exporting ppji values into a summarized matrix...')
        full_name = path_to_libra_outputs + 'PPJI_values_summary_matrix.csv'
        pd_from_r_df.to_csv(full_name)
  #
  return input_dict
    
         

    











    


 




