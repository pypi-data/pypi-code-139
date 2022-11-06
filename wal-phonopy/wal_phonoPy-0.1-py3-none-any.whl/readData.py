from scipy.io import wavfile
import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

path = r'D:\MailRu\Qawati\the-circor-digiscope-phonocardiogram-dataset-1.0.3\training_data'
list = os.listdir(path)
tr_data = pd.read_csv('training_data.csv')
print(tr_data.loc[(tr_data['Murmur'] == 'Absent') & (tr_data['Recording locations:'] == 'AV+PV+TV+MV')])

x = []
c = 0
for i in (tr_data['Recording locations:']):
    if len(i) == 11:
        # print(i, c+1)
        c += 1
        # print(tr_data[tr_data['Recording locations:'] == i])
        # x.append(tr_data[tr_data['Recording locations:'] == i])


list_wav = []
list_hea = []
list_tsv = []
list_txt = []


for i in list:
    if '.wav' in i:
        list_wav.append(i)
    if '.hea' in i:
        list_hea.append(i)
    if '.tsv' in i:
        list_tsv.append(i)
    if '.txt' in i:
        list_txt.append(i)

i = 100
samplerate, data = wavfile.read(os.path.join(path, list_wav[i]))

txt_data = pd.read_csv(os.path.join(path, list_txt[i]), delimiter=' ')

hea_data = pd.read_csv(os.path.join(path, list_hea[i]), delimiter=' ')

tsv_data = pd.read_csv(os.path.join(path, list_tsv[i]), delimiter='\t')

tsv_data = np.loadtxt(os.path.join(path, list_tsv[i]), delimiter='\t')



