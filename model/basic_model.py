import os
import matplotlib.pyplot as plt
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import pandas as pd

from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from torch.utils.data import DataLoader,Dataset


DAYS_FOR_TRAIN = 6
# ORI_FEATURE_SIZE = 5
FEATURE_SIZE = 5
BATCH_SIZE = 512
TEST_SIZE = 0.3

def my_load_data(csv_file):
    ori_data = pd.read_csv(csv_file)
    
    train_data, test_data = train_test_split(ori_data, test_size=TEST_SIZE, shuffle=False)
    return train_data, test_data, ori_data


class StockDataset(Dataset):
    """stock market dataset"""
    
    def __init__(self, dataset, days_for_train=5, feature_size=5, scaled=True):
        self.days_for_train = days_for_train
        self.feature_size = feature_size
        self.ori_data = dataset

        self.data = self.ori_data.iloc[:, 1:1+self.feature_size].values.astype(np.float32)

        if scaled:
            scaler = MinMaxScaler()
            self.data = scaler.fit_transform(self.data).astype(np.float32)
        
        self.x = self.data
        self.y = self.data[:, 3]
        

    def __len__(self):
        return self.data.shape[0] - self.days_for_train

    
    def __getitem__(self, idx):
        x = self.x[idx:idx+self.days_for_train]
        y = np.zeros((1), dtype=np.float32)

        y[0] = self.y[idx+self.days_for_train]

        t_x = torch.from_numpy(x)
        t_y = torch.from_numpy(y)
        return t_x, t_y


class LSTM_Regression(nn.Module):
    """
        使用LSTM进行回归
        
        参数：
        - input_size: feature size
        - hidden_size: number of hidden units
        - output_size: number of output
        - num_layers: layers of LSTM to stack
    """
    def __init__(self, input_size, hidden_size, output_size=1, num_layers=2):
        super().__init__()

        self.lstm = nn.LSTM(input_size, hidden_size, num_layers)
        self.fc = nn.Linear(hidden_size, output_size)
        self.fc2 = nn.Linear(DAYS_FOR_TRAIN, output_size)

    def forward(self, _x):
#         print('_x', _x.shape)
        x, _ = self.lstm(_x)  # _x is input, size (seq_len, batch, input_size)
        s, b, h = x.shape  # x is output, size (seq_len, batch, hidden_size)
#         print('forward x: ', x.shape)
        x = x.view(s*b, h)
        out1 = self.fc(x)
        out1 = out1.view(s, b)  # 把形状改回来
        out1 = out1.transpose(0, 1)
#         print('out1', out1.shape)
        out2 = self.fc2(out1)
        # print(out2.shape)
        # out2 = out2.view(b, -1)
        return out2
    

def my_train(train_dataset):
#     print(train_dataset)
    data = StockDataset(train_dataset, DAYS_FOR_TRAIN, FEATURE_SIZE)
    D = DataLoader(dataset=data, batch_size=BATCH_SIZE)

    model = LSTM_Regression(FEATURE_SIZE, 8, output_size=1, num_layers=2)

    loss_function = nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.05)

    for epoch in range(200):       
        for i, (x, y) in enumerate(D):
#             print(x.shape, y.shape)
            x = x.transpose(0, 1)
#             x.transpose(1, 2)
            pred_y = model(x)
#             print('pred_y: ', pred_y.shape)
            loss = loss_function(pred_y, y)

            loss.backward()
            optimizer.step()
            optimizer.zero_grad()

        # out = model(train_x)
        # loss = loss_function(out, train_y)

        # loss.backward()
        # optimizer.step()
        # optimizer.zero_grad()

        if (epoch+1) % 5 == 0:
            print('Epoch: {}, Loss:{:.5f}'.format(epoch+1, loss.item()))
    
    return model

def my_test(model, test_dataset):
    model.eval()
    loss_function = nn.MSELoss()

    test_data = StockDataset(test_dataset, DAYS_FOR_TRAIN, FEATURE_SIZE)
    test_D = DataLoader(dataset=test_data, batch_size=1)

    all_loss = []
    preds = []
    targets = []

    for i, (test_x, test_y) in enumerate(test_D):
        test_x = test_x.transpose(0, 1)
        pred_y = model(test_x)
#         print(test_y)
#         print(type(pred_y), type(test_y))
        preds.extend(pred_y.detach().numpy())
        targets.extend(test_y.detach().numpy())

        test_loss = loss_function(pred_y, test_y)
        all_loss.append(test_loss)
#         print(test_loss)

    print('test loss: %.5f' % (sum(all_loss)))
    
    plt.plot(preds, 'r', label='prediction')
    plt.plot(targets, 'b', label='real')
    plt.savefig('result_img/result.png', format='png', dpi=200)
    plt.show()



train_dataset, test_dataset, ori_dataset = my_load_data('data/AAPL_long.csv')
trained_model = my_train(test_dataset)
my_test(trained_model, ori_dataset)