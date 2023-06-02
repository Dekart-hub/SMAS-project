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


def get_prices(stock_tag):
    stock = yf.Ticker(stock_tag)
    dataframe = stock.history(period="365d")
    return {'cur': dataframe['Open'][-1],
            'week': (dataframe['Open'][-1] - dataframe['Open'][-7]) / dataframe['Open'][-7] * 100,
            'year': (dataframe['Open'][-1] - dataframe['Open'][-365]) / dataframe['Open'][-365] * 100}


def get_stock_data(stocks):
    stock_prices = {}
    for stock in stocks:
        stock_prices[stock.tag] = get_prices(stock.tag)
    return stock_prices


def filter_stocks(stocks, filter: dict):
    if filter['market']:
        stocks = stocks.filter(market_id=filter['market'])

    if filter['type']:
        stocks = stocks.filter(type_id=filter['type'])

    if filter['search_title']:
        stocks = stocks.filter(title__icontains=filter['search_title'])

    if filter['search_tag']:
        stocks = stocks.filter(tag__icontains=filter['search_tag'])
    return stocks


def filter_data(dates, y, filter: dict):
    new_dates = [[], []]
    for date_index in range(len(dates)):
        if (filter['start_date'] and filter['end_date']
                and filter['start_date'].date() <= dates[date_index] <= filter['end_date'].date()):
            new_dates[0].append(dates[date_index])
            new_dates[1].append(y[date_index])
        elif filter['start_date'] and filter['start_date'].date() <= dates[date_index] and not filter['end_date']:
            new_dates[0].append(dates[date_index])
            new_dates[1].append(y[date_index])
        elif filter['end_date'] and dates[date_index] <= filter['end_date'].date() and not filter['start_date']:
            new_dates[0].append(dates[date_index])
            new_dates[1].append(y[date_index])
        elif not filter['start_date'] and not filter['end_date']:
            new_dates[0].append(dates[date_index])
            new_dates[1].append(y[date_index])
    return new_dates[0], new_dates[1]


def take_date(date):
    date = date.timetuple()
    return time.mktime(date)


def lr_predict(x_test, name, model_tag):
    pkl_filename = MEDIA_ROOT + "models/" + f"{model_tag}_model_{name}.pkl"
    with open(pkl_filename, 'rb') as file:
        pickle_model = pickle.load(file)
    return pickle_model.predict(x_test.reshape(-1, 1))


def lr_train(x_train, y_train, name, model_tag):
    lr = linear_model.LinearRegression()
    lr.fit(x_train.reshape(-1, 1), y_train.reshape(-1, 1))
    pkl_filename = MEDIA_ROOT + "models/" + f"{model_tag}_model_{name}.pkl"
    with open(pkl_filename, 'wb') as file:
        pickle.dump(lr, file)


models = {'lr': (lr_train, lr_predict)}


def show(dates, x_test, y_test, name, model_tag):
    plt.plot(dates, y_test, 'b')
    if model_tag:
        plt.plot(dates, models[model_tag][1](x_test, name, model_tag), 'r')


def show_data(datasets):
    for dataset in datasets:
        plt.plot(dataset[0], dataset[1])


def take_data(company, filter):
    data_count = 100
    model_tag = filter['model']
    stock = yf.Ticker(company)
    dataframe = stock.history(period=f"{data_count}d")
    dates = dataframe.axes[0].date
    y = dataframe['Open'].values
    dates, y = filter_data(dates, y, filter)
    dates, y = np.array(dates), np.array(y)
    x = np.array(list(map(take_date, dates)))
    if model_tag:
        models[model_tag][0](x, y, company, model_tag)
    show(dates, x, y, company, model_tag)
