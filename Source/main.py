from datasets.pku import load_data
import argparse 
from models.BaselineModel import MyUNet
import torch
from utils.trainer import train
from torch import optim
from torch.optim import lr_scheduler

def main(args):
    data = load_data()
    train_loader, dev_loader, test_loader = data.get_baseline()

    if args.cuda:
        print('\nGPU is ON!')
        model = MyUNet(8, args).cuda()
    else:
        model = MyUNet(8, args)
    
    optimizer = optim.Adam(model.parameters(), lr=args.lr)
    exp_lr_scheduler = lr_scheduler.StepLR(optimizer, 
                                        step_size=max(args.epochs, 10) * len(train_loader) // 3, 
                                        gamma=0.1)

    train(model, optimizer, exp_lr_scheduler, train_loader, dev_loader, args)


# Training settings
parser = argparse.ArgumentParser(description='PKU')
parser.add_argument('--epochs', type=int, default=10, metavar='N',
                    help='number of epochs to train (default: 10)')
parser.add_argument('--lr', type=float, default=0.001, metavar='LR',
                    help='learning rate (default: 0.01)')
parser.add_argument('--reg', type=float, default=10e-5, metavar='R',
                    help='weight decay')
parser.add_argument('--no-cuda', action='store_true', default=False,
                    help='disables CUDA training')
parser.add_argument('--model-path', type=str, default='./save_models/{}.pth',
                    help='save train models')
parser.add_argument('--loss-path', type=str, default='./save_models/loss.csv',
                    help='save losses')
        
args = parser.parse_args()
args.cuda = not args.no_cuda and torch.cuda.is_available()

if __name__ == "__main__":
    main(args)