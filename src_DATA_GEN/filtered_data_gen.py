import numpy as np
import pandas as pd
import scipy.signal
import scipy.io
from scipy.signal import butter, sosfilt, hilbert
import os
import glob
import re
import multiprocessing as mp


#Global variables
sampling_rate=512;
bin_size=10;
total_patients=16;
no_of_workers_in_pool=mp.cpu_count();

#Modify the Path here acording to the download location
data_in_path="/home/sapta/Documents/"
data_save_path="../data/"

## FIltering, Hilbert Transformation and Amplitude Entropy Calculation
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


def filtered_data_AE_Worker(params):
        # Saving AE with time for all patients and seizures
        output_events={'fileID':[],'sez_len':[],'elec_no':[],'delta':[],'theta':[],'alpha':[],'beta':[],'lgamma':[],'hgamma':[]}

        patid, sz_id = params
        filename = os.path.join(data_in_path, "ID"+str(patid)+"/Sz"+str(sz_id)+".mat")
        mat=scipy.io.loadmat(filename)
        data=np.array(mat.get('EEG'))
        
        print("Processing patient ID"+str(patid)+" Seizure "+str(sz_id))

        #Sampling rate is 512Hz and each seizure preceded and succeeded by a 3 mins long segment
        sez_length=(np.shape(data)[0]/sampling_rate) - (2*3*60) #in seconds
        no_elec=np.shape(data)[1]
        
        output_events['fileID'].append("p"+str(patid)+"s"+str(sz_id))#Recorded in seconds
        output_events['sez_len'].append(sez_length)#Recorded in seconds
        output_events['elec_no'].append(no_elec)
        output_events['delta'].append(amp_en(data, 0.5,4)) #Delta Band
        output_events['theta'].append(amp_en(data, 4,8)) #Theta Band
        output_events['alpha'].append(amp_en(data, 8,12)) #Alpha Band
        output_events['beta'].append(amp_en(data, 12,35)) #Beta Band
        output_events['lgamma'].append(amp_en(data, 35,80)) #Low Gamma Band
        output_events['hgamma'].append(amp_en(data, 80,150)) #High Gamma Band   
        
        return pd.DataFrame.from_dict(output_events)  

#Creating all possible combinations of patients and seizures
all_comb=[(patid,i) for patid in range(1,total_patients+1) for i in range(1,len(glob.glob(os.path.join(data_in_path+"ID"+str(patid), '*.mat')))+1)]

# Running the worker function in parallel
pool = mp.Pool(mp.cpu_count())
all_res = [pool.apply_async(filtered_data_AE_Worker, (params,)) for params in all_comb]
# Close the pool and wait for the work to finish
pool.close()
pool.join()
#Taking the results from the workers and saving them
data=pd.DataFrame()
for dframes in all_res:
        r=dframes.get()
        if not r.empty:
            data=pd.concat([data,r], ignore_index=True)
        
data.to_json(os.path.join(data_save_path,"all_data_Swiss-Short.json"), orient='records')


# Mean patient AEs with time (which is averaged over seizures per patient)

def mean_std(arr):
    return np.mean(arr),np.std(arr)

def meanning(i,band):
    tmp=data.loc[i,band]
    no_datapoints = np.shape(tmp)[0]
    if data.loc[i,'sez_len'] == (no_datapoints/sampling_rate) - (2*3*60):
        rg=tmp[(3*60*sampling_rate) : (no_datapoints - (3*60*sampling_rate))] #Seizure Segment
        if (len(rg)/sampling_rate)== data.loc[i,'sez_len']:
            pre_mean,pre_std=mean_std(tmp[:(3*60*sampling_rate)]) #Pre-seizure Segment
            sez_mean,sez_std=mean_std(rg) #Seizure Segment
            post_mean,post_std=mean_std(tmp[no_datapoints - (3*60*sampling_rate):]) #Post-seizure Segment
            
    pattern = r'\d+'
    matches = re.findall(pattern, data.loc[i,'fileID'])
    pat_id,sez_id= [int(match) for match in matches]
    return data.loc[i,'fileID'],pat_id,sez_id,band,data.loc[i,'sez_len'],data.loc[i,'elec_no'],pre_mean,pre_std,sez_mean,sez_std,post_mean,post_std

# Create an empty DataFrame 
df = pd.DataFrame(columns=['file_ID','pat_id','sez_id','band','sez_length','no_of_elec','pre_mean','pre_sd',    'sez_mean','sez_sd','post_mean','post_sd'])

#Not worth time-wise to parallelize this
for i in data.index:
    for band in ['delta', 'theta', 'alpha', 'beta','lgamma', 'hgamma']:
        all=meanning(i,band)
        row={
            'file_ID' : all[0],
            'pat_id' : all[1],
            'sez_id' : all[2],
            'band' : all[3],
            'sez_length' : all[4],
            'no_of_elec' : all[5],
            'pre_mean' : all[6],
            'pre_sd' : all[7],
            'sez_mean' : all[8],
            'sez_sd' : all[9],
            'post_mean' : all[10],
            'post_sd' : all[11]
        }
        df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
        
df.to_json(os.path.join(data_save_path,"all_mean_Swiss-Short.json"), orient='records')