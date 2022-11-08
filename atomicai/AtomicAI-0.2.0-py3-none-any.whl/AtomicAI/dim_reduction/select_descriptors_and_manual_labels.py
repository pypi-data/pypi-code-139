import numpy as np
import os, sys, imp, random
def select_descriptors_and_manual_labels(descriptor_filename, count):
    data = np.asarray(np.loadtxt(descriptor_filename, skiprows=0))
    features = np.asarray(np.loadtxt(descriptor_filename, skiprows=0))
    row, column = np.shape(data)
    features = data[:, 0:column-1]   # Descreptors
    labels = data[:, column-1].reshape(row, 1) # Force
    
    # train, test, validation sets are about20%, 60% and 20%.
    train_indices = np.arange(0, int(20/100 * row))
    val_indices = np.arange(int(20/100 * row), int(40/100*row))
    test_indices = np.arange(int(40/100 * row), row)
    train_indices_file = './descriptors/train_indices.txt'
    val_indices_file = './descriptors/val_indices.txt'
    train_indices = np.arange(0, row)
    if len(train_indices) > 3000:
        try:
            print('Read from train_indecis_file')
            train_indices = np.asarray(np.loadtxt(train_indices_file, skiprows=0), dtype('int32'))
        except:
            train_indices = random.choices(train_indices, k=2000) 
            with open(train_indices_file, 'w') as ti:
                    line = [str(train_index) + '\n' for train_index in train_indices]
                    ti.writelines(line)
                    ti.close()

    val_indices = random.choices(val_indices, k=2000) 
    f_train, f_test, f_val = features[train_indices], features[test_indices], features[val_indices]
    l_train, l_test, l_val = labels[train_indices], labels[test_indices], labels[val_indices]
    return (f_train, f_test, f_val, l_train, l_test, l_val)

   #else:
   #    is_labels = False
   #
   #    # train, test, validation sets are about20%, 60% and 20%.
   #    train_indices = np.arange(0, int(20/100 * row))
   #    val_indices = np.arange(int(20/100 * row), int(40/100*row))
   #    test_indices = np.arange(int(40/100 * row), row)
   #    train_indices_file = './descriptors/train_indices.txt'
   #    val_indices_file = './descriptors/val_indices.txt'
   #    if len(train_indices) > 2000:
   #        try:
   #            train_indices = np.asarray(np.loadtxt(train_indices_file, skiprows=0), dtype='int32')
   #        except:
   #            if count > 1:
   #                print('Generating random train_indices file in descriptors directory \n is more than one time, Please stop.')
   #                exit()
   #            train_indices = random.choices(train_indices, k=5000)
   #            with open(train_indices_file, 'w') as ti:
   #                    line = [str(train_index) + '\n' for train_index in train_indices]
   #                    ti.writelines(line)
   #                    ti.close()
   #    val_indices = random.choices(val_indices, k=2000)
   #    f_train, f_test, f_val = features[train_indices], features[test_indices], features[val_indices]
   #    return is_labels, (f_train, f_test, f_val)

