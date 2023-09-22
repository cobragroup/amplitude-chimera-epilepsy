# To Download

import wget
import zipfile
import os
import scipy.io
import glob
import numpy as np

# Open a file in read mode ('r')
file_path = 'shortterm-files.txt'
download_directory = '../data/'
os.makedirs(download_directory, exist_ok=True)
# Global variable
sampling_rate=512

## Downaloding the files
try:
    with open(file_path, 'r') as file:
        for line in file:
            # Process each line here
            print("Downloading...",line.strip())  # Strip removes trailing newline character
            url=line.strip()
            # Extract the filename from the URL
            filename = os.path.join(download_directory, os.path.basename(url))
            # Download the file
            wget.download(url, out=filename)
            # Unzip the file
            with zipfile.ZipFile(filename, 'r') as zip_ref:
                zip_ref.extractall(download_directory)
            
            # Remove the ZIP file (optional, if you want to keep it, remove this line)
            os.remove(filename)
except FileNotFoundError:
    print(f"The file '{file_path}' does not exist.")
except IOError:
    print(f"An error occurred while reading the file '{file_path}'.")


# Just Printing the Metadata
for patid in range(1,17):
    mat_files = glob.glob(os.path.join(download_directory+"ID"+str(patid), '*.mat'))
    no_of_seizures = len(mat_files)
    #print("No of seizures: ", no_of_seizures)
    Slength=[];no_of_electrodes=[];

    for i in range(1,no_of_seizures+1):
        filename = os.path.join(download_directory, "ID"+str(patid)+"/Sz"+str(i)+".mat")
        mat=scipy.io.loadmat(filename)
        data=np.array(mat.get('EEG'))

        #Sampling rate is 512Hz and each seizure preceded and succeeded by a 3 mins long segment
        sez_length=(np.shape(data)[0]/sampling_rate) - (2*3*60) #in seconds
        no_elec=np.shape(data)[1]
        
        Slength.append(sez_length) #in seconds
        no_of_electrodes.append(no_elec)
        
        
    print("PatID:",patid," Electrodes ",np.mean(no_of_electrodes),"/",np.std(no_of_electrodes)," Szs ",no_of_seizures," Max/Min ",np.max(Slength),"/",np.min(Slength))   
    

