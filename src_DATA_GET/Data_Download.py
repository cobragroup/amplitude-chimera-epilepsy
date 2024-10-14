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

print("Merge Xa and Xb folders. For Example: merge ID4a and ID4b as ID4.")
