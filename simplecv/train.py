import argparse
import torch
import torch.nn as nn
import torch.distributed as dist
from simplecv.module.model_builder import make_model
from simplecv.data.data_loader import make_dataloader
from simplecv.opt.optimizer import make_optimizer
from simplecv.opt.learning_rate import make_learningrate
from simplecv.util import config
from simplecv.api import trainer
from simplecv.util import param_util

parser = argparse.ArgumentParser()
parser.add_argument("--local_rank", type=int)
parser.add_argument('--config_path', default=None, type=str,
                    help='path to config file')
parser.add_argument('--model_dir', default=None, type=str,
                    help='path to model directory')


def run(local_rank, config_path, model_dir):
    # 0. config
    cfg = config.import_config(config_path)

    if torch.cuda.is_available():
        torch.cuda.set_device(local_rank)
        dist.init_process_group(
            backend="nccl", init_method="env://"
        )
    # 1. data
    traindata_loader = make_dataloader(cfg['data']['train'])
    testdata_loader = make_dataloader(cfg['data']['test']) if 'test' in cfg['data'] else None
    # 2. model
    model = make_model(cfg['model'])
    if dist.is_available():
        model = nn.parallel.DistributedDataParallel(
            model, device_ids=[local_rank], output_device=local_rank,
        )
    # 3. optimizer
    optimizer = make_optimizer(cfg['optimizer'], params=param_util.trainable_parameters(model))
    lr_schedule = make_learningrate(cfg['learning_rate'])
    tl = trainer.Launcher(
        model_dir=model_dir,
        model=model,
        optimizer=optimizer,
        lr_schedule=lr_schedule,
        master=local_rank == 0)

    tl.train_by_config(traindata_loader, config=cfg['train'], test_data_loader=testdata_loader)


if __name__ == '__main__':
    args = parser.parse_args()
    assert args.config_path is not None, 'The config file is needed.'
    assert args.model_dir is not None, 'The model dir is needed.'
    run(local_rank=args.local_rank,
        config_path=args.config_path,
        model_dir=args.model_dir)
