import time
import pickle
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
import torch
from matplotlib import pyplot as plt
from sklearn import linear_model
from torch import nn
from torch.utils.data import Dataset, DataLoader

import yfinance as yf


def take_date(date):
    date = date.timetuple()
    return time.mktime(date)


def linear_regression_predict(x_test, name):
    pkl_filename = f"lr_model_{name}.pkl"
    with open(pkl_filename, 'rb') as file:
        pickle_model = pickle.load(file)
    return pickle_model.predict(x_test.reshape(-1, 1))


def linear_regression_train(x_train, y_train, name):
    lr = linear_model.LinearRegression()
    lr.fit(x_train.reshape(-1, 1), y_train.reshape(-1, 1))
    pkl_filename = f"lr_model_{name}.pkl"
    with open(pkl_filename, 'wb') as file:
        pickle.dump(lr, file)


def linear_regression_show(x_test, y_test, name):
    plt.plot(x_test, y_test, 'r')
    plt.plot(x_test, linear_regression_predict(x_test, name), 'b')
    plt.show()


data_count = 100
company = 'IBM'
stock = yf.Ticker(company)
dataframe = stock.history(period=f"{data_count}d")
dates = dataframe.axes[0].date
y = dataframe['Open'].values
x = np.array(list(map(take_date, dates)))
linear_regression_train(x, y, company)
linear_regression_show(x, y, company)
