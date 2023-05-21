import time
import pickle
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
import torch
import matplotlib

from smas.settings import MEDIA_ROOT

matplotlib.use('Agg')
from matplotlib import pyplot as plt
from sklearn import linear_model
from torch import nn
from torch.utils.data import Dataset, DataLoader

import yfinance as yf


def take_date(date):
    date = date.timetuple()
    return time.mktime(date)


def linear_regression_predict(x_test, name):
    pkl_filename = MEDIA_ROOT + "models/" + f"lr_model_{name}.pkl"
    with open(pkl_filename, 'rb') as file:
        pickle_model = pickle.load(file)
    return pickle_model.predict(x_test.reshape(-1, 1))


def linear_regression_train(x_train, y_train, name):
    lr = linear_model.LinearRegression()
    lr.fit(x_train.reshape(-1, 1), y_train.reshape(-1, 1))
    pkl_filename = MEDIA_ROOT + "models/" + f"lr_model_{name}.pkl"
    with open(pkl_filename, 'wb') as file:
        pickle.dump(lr, file)


def linear_regression_show(dates, x_test, y_test, name):
    plt.plot(dates, y_test, 'r')
    plt.plot(dates, linear_regression_predict(x_test, name), 'b')


def take_data(company):
    data_count = 100
    stock = yf.Ticker(company)
    dataframe = stock.history(period=f"{data_count}d")
    dates = dataframe.axes[0].date
    y = dataframe['Open'].values
    x = np.array(list(map(take_date, dates)))
    linear_regression_train(x, y, company)
    linear_regression_show(dates, x, y, company)
