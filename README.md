# amplitude-chimera-epilepsy
Code and variables for the paper Saptarshi Ghosh et al. "Amplitude entropy captures chimera-like behavior in epileptic seizure dynamics." [Currently under review]

## Overview
This repository contains code and data related to [briefly describe your project's purpose and significance].

## Installation
The installation requires Python>=3.x and conda (or py-venv) package. Users can then install the requirements inside a conda environment using 
```bash
conda env create -f environment.yml\
``` 

Once created the conda environment can be activated with ```conda activate ampEN``` and run the code in src_x folders.

## Folder Structure
- **data:** Contains raw data files.
- **scripts:** Holds code scripts for data processing and analysis.
- **figures:** Stores generated figures and visualizations.
- **docs:** Documentation and additional project materials.
- **results:** Result files and intermediate outputs.

## Files
### `data/`
- `data.csv`: Main dataset used for analysis.
- `metadata.json`: Metadata for the dataset.

### `scripts/`
- `data_preprocessing.py`: Data cleaning and preprocessing script.
- `analysis.ipynb`: Jupyter Notebook for data analysis.
- `plotting.py`: Functions for generating figures.

### `figures/`
- `figure1.png`: Example figure showing data distribution.
- `figure2.jpg`: Another figure illustrating variable correlation.

### `docs/`
- `README.md` (this file): Project overview, folder structure, and file descriptions.
- `CONTRIBUTING.md`: Guidelines for contributors.
- `LICENSE`: Project's license file.

### `results/`
- `analysis_results.csv`: Results of the analysis.
- `intermediate_output.txt`: Intermediate output or logs.

## Usage
Explain how to use the project, including instructions for running code and reproducing figures.

## Getting Started
Provide setup instructions, dependencies, and environment setup steps.

## Contributing
Explain how others can contribute, including guidelines for pull requests, issue reporting, and code style.

## License
Specify the project's license (e.g., MIT License).

## Acknowledgments
Acknowledge contributors, data sources, or sources of inspiration.

## Contact
Include contact information for questions or feedback.

## References
List any external sources or references relevant to your project.


## Instructions
This project uses [poetry](https://python-poetry.org/) to manage its dependencies. You can download it via
```bash
pip install --user poetry
```
then clone this repository, `cd` into it and run
```bash
poetry install
```
Place your data in the folder `data/` in the form of `I<interval>.mat`, e.g.:
```bash
SNN_HFO_iEEG/data/I1.mat
```
then run the code via
```bash
poetry run ./run.py <mode>
```
where `<mode>` is one of either `ieeg`, `ecog` or `scalp`.
If you run into problems, you can always run
```bash
poetry run ./run.py --help
``` 
And if you're still stuck, feel free to open an [issue](https://github.com/kburel/SNN_HFO_iEEG/issues/new) and we will help.

## Usage Examples
Show help:
```bash
poetry run ./run.py --help
```

When running, you need to specify how the data was obtained in order to run the right analyzers. We support the following modes:
- **ieeg**: Data was obtained via iEEG, the ripple bandwidth (80-250 Hz) and the fast ripple bandwidth (250-500 Hz) will be analyzed
- **ecog**: Data was obtained via eCoG, only the fast ripple bandwidth will be analyzed
- **scalp**: Data was obtained over the scalp via EEG, only the ripple bandwidth will be analyzed

Analyze all available data in iEEG mode:
```bash
poetry run ieeg ./run.py
```

Run in iEEG mode with custom data path:
```bash
poetry run ./run.py ieeg --data-path path/to/data
```

Analyze all available data in iEEG mode with an SNN with 100 hidden neurons:
```bash
poetry run ieeg ./run.py --hidden-neurons 100
```

 
Only analyze channels 2, 3 and 5 in eCoG mode:
```bash
# Since the channels are imported from matlab, they are 1 based
poetry run ecog ./run.py ecog --channels 2 3 5
```

Only analyze the first 100 seconds of the datasets in scalp mode:
```bash
poetry run scalp ./run.py scalp --duration 100
```

Only analyze the intervals 2, 3, 4, 6, 7 and 8 in iEEG mode:
```bash
poetry run ./run.py ieeg --intervals 2 3 4 6 7 
```

All options can be freely combined. For example, the following will construct an SNN with 256 neurons and
analyze the intervals 3 and 4 of in the channels 1 and 2
while only looking at the first 300 seconds in iEEG mode for data in ./ieeg-data:
```bash
poetry run ./run.py iieg --data-path ./ieeg-data --hidden-neurons 256 --intervals 3 4 --channels 1 2 --duration 300
```

## Plotting
The output can be plotting during the run in various ways by using `--plot`. The specified plots are created either after every channel
or after the entire patient. Note that multiple plots can be speficied.

### Per channel plots
- **raster**: Classic neuron ID to spike time raster plot. On gets drawn when an HFO was detected.
- **hfo_samples**: Shows interactive analytics for all detected HFO periods in the channel

### Per patient plots
- **mean_hfo_rate**: Plots the mean HFO rates of the channels along with their standard deviation



# Neuromorphic Oscillators for Pacemakers
Here we provide the code to the paper "Robust neuromorphic coupled oscillators for adaptive pacemakers".
This code allows you to implement a system of three coupled oscillators on the DYNAP-SE board and tune their frequency and phase shift.
It also shows you how to build and tune the parameters to provide an inhibitory input signal to adapt the oscillators' frequencies to implement an adaptive pacemaker.



## Installation
### Prerequisites
* contrexcontrol v4.0.2 (now samna, see: https://pypi.org/project/samna/)
* brian2 (https://brian2.readthedocs.io/en/stable/introduction/install.html)
* teili (https://teili.readthedocs.io/en/latest/)
* biosppy (https://biosppy.readthedocs.io/en/stable/)
```bash
pip install brian2
pip install teili
pip install biosppy
```

## Usage
To set up a system of 3 coupled oscillators and tune it as described in the paper, please use the scripts in this order:
* ***01_tune_three_coupled_oscillators.ipynb***
  Script to set up and tune the frequency and phase shift of a system of 3 coupled oscillators
* ***02_run_param_sweep_DCInput.ipynb***
Script to run parameter swipe over DC on each individual oscillator to later obtain explicit function to set oscillation frequency
* ***03_fit_fct_on_DCInput_to_frequency.ipynb***
Script to fit function on previously obtained data (run_param_swipe_constFreq.ipynb) to set oscillation frequency explicitly
* ***04_eval_fittedFct_on_DCInput_to_frequency.ipynb***
Script to evaluate how well the previously fitted function (to set oscillation frequency explicitly) works
* ***05_analysis_sECG_and_respiratorySignal.ipynb***
Script to look at recorded sECG and respiratory signal data. It also shows how the breathing coefficient is calculated and how the relation between the R-R interval and the average breathing coefficient is obtained.
* ***06_run_param_sweep_on_inhInputSpikeRate_for_RSA.ipynb***
Script to run swipe on each oscillator over a set of inhibitory input spike frequencies. This is later used to obtain an initial guess of how to set the inhibitory input strength to adapt the heart rate to the respiratory signal (RSA restoration).
* ***07_tune_three_coupled_oscillators_on_rsa_restoration.ipynb***
Script to tune a system of three coupled oscillators to adapt the oscillation frequency to model the RSA present in sECG recordings of dogs at rest.

## License
 [![CC BY 4.0][cc-by-shield]][cc-by]
The data collected in this work (recording_sECG_and_respiratorySignal.xlsx) is licensed under a [Creative Commons Attribution 4.0 International License][cc-by].
[![CC BY 4.0][cc-by-image]][cc-by]

[cc-by]: http://creativecommons.org/licenses/by/4.0/
[cc-by-image]: https://i.creativecommons.org/l/by/4.0/88x31.png
[cc-by-shield]: https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg

The provided code is licenced under the MIT license, see the LICENSE_MIT file.

