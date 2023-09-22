
import numpy as np
import scipy.io
import matplotlib.pyplot as plt

import os
import glob

## Mention the Data Path here for the RAW iEEG data 
data_path="../../Documents/"
sampling_rate=512

#Creating folder for the SM9 figures
import os
if not os.path.exists('../images/figSM10_11'):
   os.makedirs('../images/figSM10_11')
   
   
# Mention the seizure ID here
sez_id=1; # Displating for first seizure for all patients

for patid in range(1,17): 
    filename = os.path.join(data_path, "ID"+str(patid)+"/Sz"+str(sez_id)+".mat")
    mat=scipy.io.loadmat(filename)
    data=np.array(mat.get('EEG'))

    no_of_electrodes=np.shape(data)[1]
    tme=np.arange(1,np.shape(data)[0]) / (sampling_rate*60) # time_window in Mins

    plt.clf()
    f, ax = plt.subplots(figsize=(20, 20))
    ax.set_title("Patient ID-" + str(patid) + " Seizure-" + str(sez_id),fontsize=40)


    for c in range(no_of_electrodes):
        ax.plot(tme[::int(sampling_rate/2)], data[1::int(sampling_rate/2), c] + (c*1000), color="black", lw=0.5)
        #showing datapoints and 1/2 of the sampling rate of 512
    ax.set_yticks(range(0, no_of_electrodes * 1000, 1000))
    ax.set_yticklabels(range(1, no_of_electrodes + 1),fontsize=40)

    ax.tick_params(axis='both', which='major', labelsize=20)
    ax.set_xlabel('Time (Mins)',fontsize=40)
    ax.set_ylabel('Channel Number',fontsize=40)
    ax.axvline(3, color='red', lw=5, linestyle='--')
    ax.axvline(((np.shape(data)[0]/(512*60)) - 3), color='green',lw=5, linestyle='--')
    ax.grid(True)  # Add a grid

    f.tight_layout()
    f.savefig("../images/figSM10_11/FigSM10_ID"+str(patid)+".png")
    plt.close(f)
    #plt.show()
