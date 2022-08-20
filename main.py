# TODO
# tensorboardX: fix learning curve problem
# logger
import argparse
import configparser
from pathlib import Path
from utils import *
from preprocessing import initialize_processer
from dataset import initialize_dataset
from training_tools import initialize_criterion, initialize_optimizer, initialize_lr_scheduler
from models import initialize_model
import json

def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', type=str, default='config.ini')
    parser.add_argument('-m', '--mode', type=str, default='train')
    parser.add_argument('-r','--record', type=str) # record path
    
    return parser

def main():
    # argparser
    parser = get_parser()
    args = parser.parse_args()
    
    # configparser
    config = configparser.ConfigParser()
    config.read(args.config)
    
    # paths
    RECORDPATH = get_record_path(args)
    DATAPATH = './data/'
    # device
    if not torch.cuda.is_available():
        config['global']['device'] = 'cpu'
        
    rd_seed = config.getint('global', 'seed')
    setSeed(rd_seed)
    
    # read csv data
    df, truth_df = read_csv_data(config, args.mode, DATAPATH)
    
    print(truth_df.info())
    
    # print(df.head())
    print(df.info())
    
    # preprocessing
    processer = initialize_processer(config)
    
    df = processer.preprocess(df)
    if config['preprocess']['predict_norm'] == 'True':
        truth_df = processer.preprocess(truth_df)
        
    # print(df.head())
    # print(truth_df.head())
    
    # get dataloader
    if args.mode == 'train':
    
        train_indices, valid_indices = get_indices(config, df, rd_seed, 'train')
        train_loader = initialize_dataset(config, df, truth_df, train_indices, task="train")
        valid_loader = initialize_dataset(config, df, truth_df, valid_indices, task="eval")
        print(f'indices len: {len(train_indices)}, {len(valid_indices)}')
    elif args.mode == 'test':
        
        test_indices = get_indices(config, df, rd_seed, 'test')
        test_loader = initialize_dataset(config, df, truth_df, test_indices, task="eval")
        print(f'indices len: {len(test_indices)}')
    else:
        raise AttributeError(f'no mode name: {args.mode}')
    
    # for idx, data in enumerate(train_loader):
    #     if idx <= 0:
    #         print(f'{idx} {data}')
    
    # exit()
    
    criterion = initialize_criterion(config)
    model = initialize_model(config, args, criterion).to(device=config['global']['device'])
    
    if args.mode == 'train':
        optimizer = initialize_optimizer(config, model.parameters())
        scheduler = initialize_lr_scheduler(config, optimizer)
        
        # TODO: tensorboard recording
        tr_losses, vl_losses, lrs = [], [], []
        bestloss, bepoch = 100, 0
        # Running epoch
        for epoch in range(config.getint('train', 'epoch')):
            print(f'epoch: {epoch}')
            tr_loss = train_one(config, model, train_loader, optimizer, scheduler)
            vl_loss, _ = eval_one(config, model, valid_loader)
            lrs.append(get_lr(optimizer))
            scheduler.step(vl_loss)
            tr_losses.append(tr_loss)
            vl_losses.append(vl_loss)
            if vl_loss <= bestloss:
                bestloss = vl_loss
                bepoch = epoch
                torch.save(model.state_dict(), RECORDPATH / Path('best_model.pth'))

        print(f'best valid loss: {bestloss}, epoch: {bepoch}')
 
        # Plot train/valid loss, accuracy, learning rate
        plot_fg(tr_losses, 'losses', 'loss', RECORDPATH, vl_losses)
        plot_fg(lrs, 'lrs', 'lr', RECORDPATH)
        
    elif args.mode == 'test':
        loss, pred = eval_one(config, model, test_loader, 'Test')
        
        print(f'test unpostprocessed loss: {loss}')
        
        tmp = max(int(config['data']['reserved']), int(config['model']['input_time_step']) + int(config['model']['output_time_step'])-1)
        pred = np.concatenate([[None]*tmp, pred], axis=0)        
        
        # TODO: change model name
        pred_df = df.copy().rename(columns={'CODE':'LSTM'})
        pred_df[pred_df.columns[-1]] = pred
        
        # post processing
        if config['preprocess']['predict_norm'] == 'True':
            pred_df = processer.postprocess(pred_df) # Possible error: np.nan denormed
            
        pred_df.to_csv(RECORDPATH / Path('prediction.csv'))
        
def train_one(config, model, dataloader, optimizer, scheduler=None):
    model.train()
    totalloss = 0
    with tqdm(dataloader, unit='batch', desc='Train') as tqdm_loader:
        for idx, data in enumerate(tqdm_loader):
            for d in data:
                data[d] = data[d].to(device=config['global']['device'])
                
            output, loss = model(**data)
            
            optimizer.zero_grad()
            loss.backward()
                        
            optimizer.step()
            # scheduler.step()

            nowloss = loss.item()

            totalloss += nowloss
            tqdm_loader.set_postfix(loss=f'{nowloss:.7f}', avgloss=f'{totalloss/(idx+1):7f}')
    return totalloss/len(tqdm_loader)

def eval_one(config, model, dataloader, mode='Valid'):
    model.eval()
    output_list = []
    totalloss, bestloss = 0, 10
    with torch.no_grad():
        with tqdm(dataloader,unit='batch',desc=mode) as tqdm_loader:
            for idx, data in enumerate(tqdm_loader):
                for d in data:
                    data[d] = data[d].to(device=config['global']['device'])

                output, loss = model(**data) #output shape(batch, output_step or 1 , 1)
                
                # print(output.shape)
                output_list.append(output.detach().cpu().view(-1).numpy())
                
                nowloss = loss.item()
                totalloss += nowloss
                tqdm_loader.set_postfix(loss=f'{nowloss:.7f}', avgloss=f'{totalloss/(idx+1):.7f}')
    tec_pred_list = np.concatenate(output_list, axis=0)
        
    return totalloss/len(tqdm_loader), tec_pred_list

if __name__ == '__main__':
    main()