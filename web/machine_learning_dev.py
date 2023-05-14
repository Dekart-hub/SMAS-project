import time
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
import torch
from matplotlib import pyplot as plt
from torch import nn
from torch.utils.data import Dataset, DataLoader

import yfinance as yf


class DatasetForecast(Dataset):
    def __init__(self, data, sequence_length):
        self.data = data
        self.sequence_length = sequence_length

    def __len__(self):
        return int(torch.floor(torch.tensor(len(self.data) / self.sequence_length)))

    def __getitem__(self, index):
        data_sequence = self.data[index * self.sequence_length:(index + 1) * self.sequence_length - 1]
        next_value = self.data[(index + 1) * self.sequence_length - 1]
        return data_sequence, next_value


class RNN(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers):
        super(RNN, self).__init__()
        self.RNN = nn.RNN(
            input_size=input_size,
            hidden_size=hidden_size,
            num_layers=num_layers,
            nonlinearity='tanh',
            batch_first=True
        )
        self.linear1 = nn.Linear(hidden_size, 4)
        self.linear2 = nn.Linear(4, 1)

    def forward(self, x, h_state):
        x, h = self.RNN(x, h_state)
        y_pred = self.linear1(x[:, -1, :])
        y_pred = self.linear2(y_pred)
        return y_pred


# Перевод даты в тик
def take_date(date):
    date = (':'.join(date.split(':')[:-1]) + date.split(':')[-1])
    date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S%z').timetuple()
    return time.mktime(date)


# Выдача предсказаний
def model_predict(model_path, data, **kwargs):
    batch_size = kwargs['batch_size']
    sequence_length = kwargs['sequence_length']
    hidden_state = kwargs['hidden_state']
    model = torch.load(model_path)
    x = data.reshape(batch_size, sequence_length)[:, 1:]
    y_pred = model(x.reshape([batch_size, sequence_length - 1, 1]), hidden_state)
    return y_pred.detach().numpy()


def model_train(model, data, data_count, num_layers, hidden_size, epochs):
    sequence_length, batch_size, learning_rate = consts_to_rnn(data_count, data)
    forecast_train = data
    forecast_train_dataset = DatasetForecast(forecast_train, sequence_length)
    forecast_train_dataloader = DataLoader(forecast_train_dataset,
                                           batch_size=batch_size, shuffle=True)

    model = model(1, hidden_size, num_layers)
    loss_function = nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(),
                                 lr=learning_rate)

    model.train()
    loss_history = []
    for epoch in range(epochs):
        loss_total = 0
        print(epoch)
        for x_data, y_data in forecast_train_dataloader:
            hidden_state = torch.zeros([num_layers, batch_size, hidden_size])
            y_pred = model(x_data.reshape([batch_size, sequence_length - 1, 1]),
                           hidden_state)
            loss = loss_function(y_pred.view(-1), y_data)
            model.zero_grad()
            loss.backward()
            optimizer.step()
            loss_total += loss
        loss_history.append(loss_total.item())

    plt.plot(loss_history)
    plt.title('Функция потерь')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.show()

    model.eval()
    # for x_data, y_data in forecast_train_dataloader:
    #     y_pred = model(x_data.reshape([batch_size, sequence_length - 1, 1]),
    #                        hidden_state)
    #     plt.xlabel("Y")
    #     plt.ylabel("Predicted Y")
    #     y_data = y_data.detach().numpy()
    #     y_pred = y_pred.detach().numpy().reshape(y_data.size)
    #     x = np.linspace(1, y_data.size * 2, num=y_data.size * 2)
    #     # plt.scatter(y_data, y_pred, lw=1, color="b", label="test")
    #     plt.plot(x[len(x) // 2:], y_data)
    #     plt.plot(x[len(x) // 2:], y_pred)
    #     plt.legend()
    #     plt.show()

    torch.save(model, 'model1')

    # # Вывод реальных значений
    # x = np.linspace(1, data_count, num=data_count)
    # forecast_train = forecast_train.detach().numpy()
    # plt.plot(x, forecast_train, 'r')
    #
    # # Вывод предсказанных значений и предсказания на будущее
    # x = x.reshape(batch_size, sequence_length)[:, 1]
    # x = x.reshape(batch_size)[1:]
    # x = np.append(x, x[-1] + sequence_length)
    # y_pred = y_pred.detach().numpy().reshape(batch_size)
    # plt.plot(x, y_pred, 'b')
    # plt.show()


def show(x, y_data, y_pred, count):
    batch_size = y_pred.size
    sequence_length = y_data.size // batch_size

    # Вывод реальных значений
    plt.plot(x[-count:], y_data[-count:], 'r')

    # Вывод предсказанных значений и предсказания на будущее
    x = x.reshape(batch_size, sequence_length)[:, 1]
    x = x.reshape(batch_size)[1:]

    x = np.append(x, str(datetime.strptime(x[-1], '%Y-%m-%d') + timedelta(days=sequence_length)))
    # x = np.append(x, str(x[-1] + timedelta(days=sequence_length)))

    y_pred = y_pred.reshape(batch_size)
    plt.plot(x[-(count // sequence_length) - 1:], y_pred[-(count // sequence_length) - 1:], 'b')
    plt.show()


def consts_to_rnn(data_count, data):
    sequence_length = int(data_count * 0.01) if data_count > 200 else 2
    batch_size = int(data_count / sequence_length)
    learning_rate = 0.005
    return sequence_length, batch_size, learning_rate


MODELS = {'RNN': RNN}
model = MODELS['RNN']

data_count = 100
num_layers, hidden_size, epochs = 3, 15, 500

# company = 'IBM'
# stock = yf.Ticker(company)
# dataframe = stock.history(period=f"{data_count}d")
dataframe = pd.read_csv('test.csv', header=0).tail(data_count)

forecast_train = dataframe['Open'].values
forecast_train = torch.tensor(forecast_train, dtype=torch.float32)

# x = dataframe.axes[0].date
x = dataframe['Date'].to_numpy()



# Тренировка и сохранение модели
model_train(model=model,
            data=forecast_train,
            data_count=data_count,
            num_layers=num_layers,
            hidden_size=hidden_size,
            epochs=epochs)


sequence_length, batch_size, learning_rate = consts_to_rnn(data_count, forecast_train)
hidden_state = torch.zeros([num_layers, batch_size, hidden_size])
y_pred = model_predict('model1', forecast_train, batch_size=batch_size,
                       sequence_length=sequence_length, hidden_state=hidden_state)

show(x, forecast_train.detach().numpy(), y_pred, 100)
