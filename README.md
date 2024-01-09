# Global Total Electron Content Prediction
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.10473190.svg)](https://doi.org/10.5281/zenodo.10473190)

[link to paper]()

This is the implementation of paper **Forecasting of global ionosphere maps with multi-day1
lead time using transformer-based neural networks**

## Abstract
Ionospheric total electron content (TEC) is a key indicator of the space environment. Geophysical forcing from above and below drives its spatial and temporal variations. A full understanding of physical and chemical principles, available and well-representable driving inputs, and capable computational power are required for physical models to reproduce simulations that agree with observations, which may be challenging at times. Recently, data-driven approaches, such as deep learning, have therefore surged as means for TEC prediction. Owing to the fact that the geophysical world possesses a sequential nature in time and space, Transformer architectures are proposed and evaluated for sequence-to-sequence TEC predictions in this study. We discuss the impacts of time lengths of choice during the training process and analyze what the neural network has learned regarding the data sets. Our results suggest that 12-layer, 128-hidden-unit Transformer architectures sufficiently provide multi-step global TEC predictions for 48 hours with an overall RMSE of ~1.8 TECU. The hourly variation of RMSE increases from 0.6 TECU to about 2.0 TECU during the prediction time frame.

<img src="https://github.com/TEC-Prediction/TEC_Prediction_shu/assets/56257705/8f9ce146-870b-446d-913f-8e9313190e58" alt="image" style="width:400px">  

> All input & output data following SWGIM format  
> Supports multi-day GTEC input & output, three ways to permulate input sequences (time/latitude/longitude)  
> LSTM, Transformer, Transformer Encoder available  

## Basic Usage
1. Download dataset [SWGIM3.0_year](https://drive.google.com/drive/folders/16HBrvHgkfLXsu3R2JiyEqW5JSrPDlKPq?usp=drive_link) / [SWGIM1.0_year](https://drive.google.com/drive/folders/1N1WxlP5DnnSkMMCD1XeHE9bYxL81PisT?usp=drive_link) to "data/raw_data/" folder
2. **Training** ```python -m src.main -m train -c [path/to/config.ini/file] -r [path/to/record/folder] -tf [path/to/SWGIM_data/folder]```
3. **Testing** ```python -m src.main -m test -c [path/to/config.ini/file] -r [path/to/record/folder] -tf [path/to/SWGIM_data/folder]```
4. **Analyzing**  ```python -m src.analyze_tools.analyze -tf [path/to/SWGIM_data/folder] -f [path/to/prediction_file] -r [path/to/record/folder]```

```
python main.py [-h] [-c CONFIG] [-m MODE] [-tf TRUTH_PATH] [-r RECORD] [-ck CHECKPOINT] [-i RUN_ID] [-o OUTPUT]

optional arguments:
  -h, --help                   show this help message and exit
  -c CONFIG, --config          path to the configuration file (default: 'config.ini')
  -m MODE, --mode              mode of operation, either 'train' or 'test' (default: 'train')
  -tf TRUTH_PATH, --truth_path path to the truth data (default: './data/SWGIM3.0_year')
  -r RECORD, --record          path to the record folder (default: './')
  -ck CHECKPOINT, --checkpoint path to the checkpoint file for continuing training
  -i RUN_ID, --run_id          running ID of W&B for continuing training
  -o OUTPUT, --output          name of the output file (default: 'prediction_frame1.csv')

```
```
python analyze.py [-h] [-f FILE] [-m MODE] [-y YEAR YEAR] [-r RECORD] [-tf TRUTH_PATH] [-o OUTPUT_FILE]

optional arguments:
  -h, --help                    show this help message and exit
  -f FILE, --file               path to the prediction file (default: 'prediction.csv')
  -m MODE, --mode               mode of operation, either 'single' or 'global' (default: 'global')
  -y YEAR YEAR, --year          range of years as two integers (default: [2020, 2021])
  -r RECORD, --record           path to the record folder (default: './')
  -tf TRUTH_PATH, --truth_path  path to the truth data (default: './data/SWGIM3.0_year')
  -o OUTPUT_FILE, --output_file name of the output file, stored in the record path (default: 'record.json')

```
