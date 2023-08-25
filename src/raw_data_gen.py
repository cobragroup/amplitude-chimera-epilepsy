# %%
import scipy.io
import glob
import numpy as np
import os
import json

# %%
#Global variables

sampling_rate=512;
bin_size=10;

# %%
from scipy.signal import butter, sosfreqz, sosfilt, hilbert
def feq_filter(signal, fstart, fstop, fs):
    # Create second-order sections (SOS) for the filter
    nyquist = 0.5 * fs
    low = fstart / nyquist
    high = fstop / nyquist
    sos = butter(4, [low, high], btype='band', output='sos')
    
    # Apply filter to the signal
    filtered_signal = sosfilt(sos, signal)
    
    # Hilbert Transformation
    complex_signal = hilbert(filtered_signal)
    amplitude_signal = np.abs(complex_signal)
    
    return amplitude_signal

def amp_en(alldata, start, stop, bin_size=bin_size):
    number_of_datapoints, number_of_channels = alldata.shape
    
    # Filtering all the channels
    filtered = np.empty((number_of_datapoints, number_of_channels))
    for i in range(number_of_channels):
        filtered[:, i] = feq_filter(alldata[:, i], start, stop, fs=sampling_rate)
    
    en = np.empty(number_of_datapoints)
    
    # Calculating Entropies across channels
    for t in range(number_of_datapoints):
        hist, bin_edges = np.histogram(filtered[t, :], bins=np.arange(min(filtered[t, :]), max(filtered[t, :]) + bin_size, bin_size))
        pmf = hist / np.sum(hist)
        pmf = pmf[pmf > 0]
        en[t] = -np.sum(pmf * np.log2(pmf))
    
    return en
# %%
output_events={'fileID':[],'sez_len':[],'elec_no':[],'delta':[],'theta':[],'alpha':[],'beta':[],'lgamma':[],'hgamma':[]}

#Modify the Path here acording to the download location
data_path="/home/sapta/Documents/"

for patid in range(1,17):
    mat_files = glob.glob(os.path.join(data_path+"ID"+str(patid), '*.mat'))
    no_of_seizures = len(mat_files)
    #print("No of seizures: ", no_of_seizures)
    #Slength=[];no_of_electrodes=[];

    for i in range(1,no_of_seizures+1):
        filename = os.path.join(data_path, "ID"+str(patid)+"/Sz"+str(i)+".mat")
        mat=scipy.io.loadmat(filename)
        data=np.array(mat.get('EEG'))

        #Sampling rate is 512Hz and each seizure preceded and succeeded by a 3 mins long segment
        sez_length=(np.shape(data)[0]/sampling_rate) - (2*3*60) #in seconds
        no_elec=np.shape(data)[1]
        
        # Slength.append(sez_length) #in seconds
        # no_of_electrodes.append(no_elec)
        
        
        output_events['fileID'].append("p"+str(patid)+"s"+str(i))#Recorded in seconds
        output_events['sez_len'].append(sez_length)#Recorded in seconds
        output_events['elec_no'].append(no_elec)
        output_events['delta'].append(amp_en(data, 0.5,4))
        output_events['theta'].append(amp_en(data, 4,8))
        output_events['alpha'].append(amp_en(data, 8,12))
        output_events['beta'].append(amp_en(data, 12,35))
        output_events['lgamma'].append(amp_en(data, 35,80))
        output_events['hgamma'].append(amp_en(data, 80,150))    
# %%
import pandas as pd
out=pd.DataFrame.from_dict(output_events)
result = out.to_json(orient="records")
parsed = json.loads(result)
with open("../../Code_3/all_data_Swiss-Short.json", "w") as write_file:
        json.dump(parsed, write_file, indent=4)


