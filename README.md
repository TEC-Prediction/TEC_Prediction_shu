# TEC_Prediction
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.10473190.svg)](https://doi.org/10.5281/zenodo.10473190)

## Usage

<!-- python3 main.py --config [config_file_path] --mode [mode train/test] --record [record_path] -->
```
python main.py [-h] [-c CONFIG] [-m MODE] [-r RECORD] [-k MODEL_CHECKPOINT]
               [-o OPTIMIZER_CHECKPOINT] [-t] [-s SHIFTING_CNT]

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config config file path
  -m MODE, --mode train or test mode
  -r RECORD, --record record folder path
  -k MODEL_CHECKPOINT, --model_checkpoint model checkpoint file path
  -o OPTIMIZER_CHECKPOINT, --optimizer_checkpoint optimizer file path
  -t, --retest_train_data, true if using 2018-2019 data as training data
  -s SHIFTING_CNT, --shifting_cnt shifting test for multiple output time steps
```
## File explanation

- data
  - place tec data [SWGIM_year](https://drive.google.com/drive/folders/1N1WxlP5DnnSkMMCD1XeHE9bYxL81PisT?usp=share_link) folder in "./data/raw_data" folder
- config.ini  
  - config file, containing all configurations  
- main.py  
  - main func: main loop, initialize all things and run epoches  
  - train_one func: train one epoch  
  - eval_one func: evaluate one epoch and record outputs  
- dataset
  - initialize dataloader
  - collate_fn.py  
    - initialize collate_fn to adjust batched data  
- models
  - initialize model
- output
  - output data to SWGIM format  

- preprocessing
  - initialize normalization

- training_tools
  - initialize optimizer, lr_scheduler and criterion
