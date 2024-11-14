#!/usr/bin/env python
# coding: utf-8
"""
Submit experiments for QP
"""
import argparse
import itertools
import random
import time
import numpy as np
import pandas as pd
import torch
from torch import nn
from tqdm import tqdm
#import submitit

# random seed
random.seed(42)
np.random.seed(42)
torch.manual_seed(42)
torch.cuda.manual_seed(42)
torch.backends.cudnn.deterministic = True
torch.backends.cudnn.benchmark = False

# set parser
parser = argparse.ArgumentParser()
parser.add_argument("--size",
                    type=int,
                    default=1,
                    choices=[1, 10, 100, 1000, 10000],
                    help="problem type")
parser.add_argument("--samples",
                    type=int,
                    default=8000,
                    choices=[800, 8000, 80000],
                    help="problem type")
config = parser.parse_args()

# init problem
config.steepness = 50            # steepness factor
num_blocks = config.size         # number of blocks
train_size = config.samples      # number of train
test_size = 100                  # number of test size
val_size = 1000                  # number of validation size

# hyperparameters
hsize_dict = {1:4, 10:16, 100:64, 1000:256, 10000:1024, 10000:4096}
config.batch_size = 64                  # batch size
config.hlayers_sol = 5                  # number of hidden layers for solution mapping
config.hlayers_rnd = 4                  # number of hidden layers for solution mapping
config.hsize = hsize_dict[config.size]  # width of hidden layers for solution mapping
config.lr = 1e-3                        # learning rate
config.penalty = 100                    # penalty weight

# parameters as input data
p_low, p_high = 1.0, 8.0
a_low, a_high = 0.5, 4.5
p_train = np.random.uniform(p_low, p_high, (train_size, 1)).astype(np.float32)
p_test  = np.random.uniform(p_low, p_high, (test_size, 1)).astype(np.float32)
p_val   = np.random.uniform(p_low, p_high, (val_size, 1)).astype(np.float32)
a_train = np.random.uniform(a_low, a_high, (train_size, num_blocks)).astype(np.float32)
a_test  = np.random.uniform(a_low, a_high, (test_size, num_blocks)).astype(np.float32)
a_val   = np.random.uniform(a_low, a_high, (val_size, num_blocks)).astype(np.float32)
# nm datasets
from neuromancer.dataset import DictDataset
data_train = DictDataset({"p":p_train, "a":a_train}, name="train")
data_test = DictDataset({"p":p_test, "a":a_test}, name="test")
data_val = DictDataset({"p":p_val, "a":a_val}, name="dev")
# torch dataloaders
from torch.utils.data import DataLoader
batch_size = 64
loader_train = DataLoader(data_train, batch_size, num_workers=0, collate_fn=data_train.collate_fn, shuffle=True)
loader_test = DataLoader(data_test, batch_size, num_workers=0, collate_fn=data_test.collate_fn, shuffle=False)
loader_val = DataLoader(data_val, batch_size, num_workers=0, collate_fn=data_val.collate_fn, shuffle=True)

import run
print("Rosenbrock")
#run.rosenbrock.exact(loader_test, config)
#run.rosenbrock.relRnd(loader_test, config)
#run.rosenbrock.root(loader_test, config)
#run.rosenbrock.rndCls(loader_train, loader_test, loader_val, config)
#run.rosenbrock.rndThd(loader_train, loader_test, loader_val, config)
#run.rosenbrock.lrnRnd(loader_train, loader_test, loader_val, config)
run.rosenbrock.rndSte(loader_train, loader_test, loader_val, config)
