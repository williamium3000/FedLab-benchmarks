import argparse
import os
from pathlib import Path
import logging
from math import sqrt

import torch
from torch import nn
import torch.nn.functional as F
import torchvision
import torchvision.transforms as transforms

torch.manual_seed(0)

import models
from config import cifar10_config, balance_iid_data_config
from client import FedDynSerialTrainer

import sys

sys.path.append("../../../FedLab/")

from fedlab.core.network import DistNetwork
from fedlab.utils.functional import save_dict, load_dict

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="FedDyn client demo in FedLab")
    parser.add_argument("--ip", type=str, default="127.0.0.1")
    parser.add_argument("--port", type=str, default="3003")
    parser.add_argument("--world_size", type=int)
    parser.add_argument("--rank", type=int)
    parser.add_argument("--client-num-per-rank", type=int, default=10)
    parser.add_argument("--ethernet", type=str, default=None)

    parser.add_argument("--partition", type=str, default='iid', help="Choose from ['iid', 'niid']")
    parser.add_argument("--data-dir", type=str, default='../../../datasets')
    parser.add_argument("--out-dir", type=str, default='./Output')
    args = parser.parse_args()

    Path(args.data_dir).mkdir(parents=True, exist_ok=True)
    Path(args.out_dir).mkdir(parents=True, exist_ok=True)

    # get basic model
    model = getattr(models, args.model_name)

    # get basic config
    if args.partition == 'iid':
        alg_config = cifar10_config
        data_config = balance_iid_data_config

    os.environ["CUDA_VISIBLE_DEVICES"] = "0,1,2,3"

    if args.partition == 'iid':
        data_indices = load_dict("cifar10_iid.pkl")
    else:
        data_indices = load_dict("cifar10_noniid.pkl")

    # Process rank x represent client id from (x-1) * client_num_per_rank - x * client_num_per_rank
    # e.g. rank 5 <--> client 40-50
    client_id_list = [
        i for i in
        range((args.rank - 1) * args.client_num_per_rank, args.rank * args.client_num_per_rank)
    ]

    # get corresponding data partition indices
    sub_data_indices = {
        idx: data_indices[cid]
        for idx, cid in enumerate(client_id_list)
    }

    trainset = torchvision.datasets.FashionMNIST(root=args.data_dir,
                                                 train=True,
                                                 download=False,
                                                 transform=transforms.ToTensor())

    # aggregator = Aggregators.fedavg_aggregate

    network = DistNetwork(address=(args.ip, args.port),
                          world_size=args.world_size,
                          rank=args.rank,
                          ethernet=args.ethernet)

    trainer = FedDynSerialTrainer(model=model,
                                  dataset=trainset,
                                  data_slices=sub_data_indices,
                                  aggregator=None,
                                  args=config)

    manager_ = ScaleClientPassiveManager(trainer=trainer, network=network)

    manager_.run()
