import os
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader,Dataset
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def minmaxscaler(data):
    min = np.amin(data)
    max = np.amax(data)
    return (data - min)/(max-min),min,max

class GpData(Dataset):
    def __init__(self, file_path,step_len):
        self.step_len = step_len
        f = open(file_path, 'r')
        temp_data = f.readlines()
        # all_data = temp_data[1:]

        # self.data = np.zeros((len(all_data) ), dtype=np.float32)
        all_data = pd.read_csv('data/AAPL_long.csv').iloc[:, 1:]
        self.data = all_data.values

        self.data,self.min,self.max = minmaxscaler(self.data)


    def __getitem__(self, item):
        x = self.data[item:item+self.step_len]
        # y = self.data[item+self.step_len]
        y = np.zeros((1),dtype=np.float32)
        y[0] = self.data[item+self.step_len]
        # if self.data[item+self.step_len][3] > self.data[item+self.step_len-1][3]:
        #     y[0] = 1
        # else:
        #     y[0] = 0
        # x = np.swapaxes(x,0,1)
        t_x = torch.from_numpy(x)
        t_y = torch.from_numpy(y)
        # t_y = t_y.type(torch.long)
        # t_y = t_y.reshape(1,6)
        # t_y = t_y.reshape(1,1)
        return t_x,t_y

    def __len__(self):
        return self.data.shape[0]-self.step_len


class GpModel(nn.Module):
    def __init__(self, input_size,output_size,step_len):
        super(GpModel, self).__init__()
        self.step_len = step_len
        self.layer = nn.Sequential(
            nn.Linear(input_size,128),
            nn.Sigmoid(),
            nn.Linear(128, 16),
            nn.Sigmoid(),
            nn.Linear(16,output_size),
            # nn.ReLU(),

        )
        # self.out = nn.Linear(self.step_len,output_size)
        self.out = nn.Linear(6, 1)

    def forward(self, x):
        y = self.layer(x)
        return y
        # y = y.reshape(y.shape[0],1,6)
        # res = self.out(y)
        # res = res.reshape((32,2))
        # return nn.functional.log_softmax(res)


def train(file_path,step_len):
    data = GpData(file_path,step_len)
    D = DataLoader(dataset=data,batch_size=32,shuffle=True)
    model = GpModel(40,4,step_len)
    criterion = nn.MSELoss()
    # criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-2)
    for ep in range(800):
        for i,(x,y) in enumerate(D):
            pre_y = model(x)
            loss = criterion(pre_y,y)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            if i%100 == 0:
                print('Epoch: {}, Loss: {:.5f}'.format(ep + 1, loss))
        if ep == 750:
            test(model,file_path,step_len)
def test(model,file_path,step_len):
    model.eval()
    test_data = GpData(file_path, step_len)
    criterion = nn.MSELoss()
    test_D = DataLoader(dataset=test_data, batch_size=1)
    all_loss = []

    def trans_data(x,test_data):
        return x*(test_data.max-test_data.min)+test_data.min

    y_1 = []
    y_2 = []
    for i,(test_x,test_y) in enumerate(test_D):
        pre_test_y = model(test_x)
        test_loss = criterion(pre_test_y,test_y)
        y_1.append(trans_data(pre_test_y.item(),test_data))
        y_2.append(trans_data(test_y.item(),test_data))
        print(trans_data(pre_test_y.item(),test_data),trans_data(test_y.item(),test_data))
        all_loss.append(test_loss.item())

    print('test_loss: {:.5f}'.format(sum(all_loss)/len(test_D)))

    x_1 = range(len(y_1))
    plt.plot(x_1, y_1, label="pre",color="red")
    plt.plot(x_1, y_2, label="true",color="green")
    plt.show()
    # for i,(test_x,test_y) in enumerate(test_D):
    #     pre_test_y = model(test_x)
    #     print(nn.Softmax(pre_test_y),test_y)

    # print('test_loss: {:.5f}'.format(sum(all_loss)/len(test_D)))

if __name__ == '__main__':
    train(file_path="data\\AAPL.csv",step_len=40)






