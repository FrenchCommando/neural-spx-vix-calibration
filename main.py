import os
import torch
import src.checkpoint
import importlib

from data.expiry_selection import get_expiries
from src.data import load_dataset
from src.generator import GeneratorIto
from src.train_utils import train
from src.train_utils import wrap_loss_func
from src.train_utils import prepare_data
from src.train_utils import checkpoint_func
import datetime as dt


date = dt.date(2021, 10, 1)
# date = dt.date(2025, 12, 1)
model_file = ".".join(('src', "my_model"))


chosen_threshold = 21 * 6
maturities = {
    'spx': [dt.datetime.strftime(t, "%Y/%m/%d") for t in get_expiries(root="SPX", date=date, n_day_threshold=chosen_threshold + 30)],
    'vix': [dt.datetime.strftime(t, "%Y/%m/%d") for t in get_expiries(root="VIX", date=date, n_day_threshold=chosen_threshold)],
}

params = {
    "batch_size" : 150000,
    "dt" : 0.5,
    "w_fVIX" : 30,
    "w_CVIX" : 2,
    "w_SPX" : 3
}

my_model = importlib.import_module(model_file)

date_str = date.strftime("%Y/%m/%d")

data = load_dataset(date=date_str)
smiles, maturities, fSPX = prepare_data(data, date_str, maturities)

dt = torch.tensor(params["dt"] / 365)
GEN = GeneratorIto(dt, my_model.V_AND_MUY(my_model.MODEL), fSPX)

model, epoch = src.checkpoint.load_last_checkpoint(my_model.MODEL)
_, T0, loss_func = wrap_loss_func(date_str, params, smiles, maturities, GEN, dt, fSPX)
train(my_model.MODEL, epoch, loss_func, checkpoint_func, save_step=1)

