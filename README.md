# amplitude-chimera-epilepsy

Codes for Saptarshi Ghosh et al. "Amplitude entropy captures chimera-like behavior in epileptic seizure dynamics" (Currently under review). Preprint avaliable in [bioRxiv](https://doi.org/10.1101/2024.05.26.595969).

## Overview
This repository contains code and data required for reproducing the figures of the paper. The paper propose a novel method capturing the characteristic pronounced changes in the recorded EEG amplitude during seizures by estimating chimera-like states directly from the signals in a frequency-and time-resolved manner. The approach is tested on a publicly available intracranial EEG dataset of 16 patients with focal epilepsy. It is shown that the proposed measure, titled Amplitude Entropy, is sensitive to seizure onset dynamics, demonstrating its significant increases during seizure as compared to before and after seizure. This finding is robust across patients, their seizures, and different frequency bands.


## Installation
The installation requires Python>=3.x and conda (or py-venv) package. Users can then install the requirements inside a conda environment using 
```bash
conda env create -f environment.yml
``` 
Once created the conda environment can be activated with ```conda activate ampEN``` and run the codes in src_x folders. First, download the data using `src_DATA_GET`, then generate the amplitude entropy using `src_DATA_GEN` and finally plot the figures using `src_PLOT`. Modify the data paths, mentioned in the code to download and process the dataset.

## Folder Structure
- **data:** Contains raw data and generated intermediate data files.
- **images:** Stores generated figures and visualizations.
- **src_DATA_GET:** Codes for downloading and visualizing data from [SWEC-ETHZ iEEG Database](http://ieeg-swez.ethz.ch/).
- **src_DATA_GEN:** Codes to generate intermediate Amplitude Entropy from both filtered and unfiltered input signals across patients and seizures.
- **src_PLOT:** Codes to generate figures of the submitted manuscript.
- **notebooks:** Similar codes to src_DATA_GEN and src_PLOT is presented in jupyter notebook format.

## Files
### `src_DATA_GET`
- `Data_Download.py`: Main code to download and extract SWEC-ETH iEEG Dataset. Usage: `python Data_Download.py`. Note the download path. Merge `Xa` and `Xb` folders. (For Example: merge ID4a and ID4b as ID4).
- `Sez_plot.py`: For plotting the raw iEEG signals for any seizure for any patients. Usage: `python Sez_plot.py <pat_id> <sz_id>`, where pat_id can be 1...16 with corresponding seizures. Metadata for all seizures can also be printed from here. 
- `shortterm-files.txt`: Text file containing links of the files to be downloaded.

Ensure folders ID1-16 in `data_in/save path` folder before starting the AE generation code in next step.

### `src_DATA_GEN`
- `unfiltered_data_gen.py`: Script to produce `all unfiltered amplitude entropy`,`all unfiltered Mean AEs (which is averaged over seizures per patient)` and `all unfiltered electrode AA data (which is averaged over seizures and patients)` for `t1=2.5` and `t2=4 min`, as displayed in the paper (Fig 2). Usage: `python unfiltered_data_gen.py`
- `filtered_data_gen.py`: Script to produce similar files with filtering to different clinically relevant bands. Usage: `python filtered_data_gen.py`.

Multiprocessing is used to parallelize the code execution. 

### `src_PLOT/`
- `Fig_2-4.py`: Script to generate all figures of the manuscript. Usage: `python Fig_x.py`.
- `FigSM2-13.py`: Script to generate all figures of the supplementary materials. Usage: `python FigSMx.py`.

## Acknowledgments
We acknowledge SWEC-ETHZ iEEG Database as primary source of input data for this work. See the paper for further information on supporting funding agencies and academic institutes.

## Contact
Please contact the corresponding author for any questions on the investigation.

And if you're still stuck, feel free to open an [issue](https://github.com/cobragroup/amplitude-chimera-epilepsy/issues/new) and we will help.
