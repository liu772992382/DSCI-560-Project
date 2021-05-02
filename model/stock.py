import os
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader,Dataset
import numpy as np
import pandas as pd
import ta
from sklearn.preprocessing import MinMaxScaler

# def minmaxscaler(data):
#     min = np.amin(data)
#     max = np.amax(data)
#     return (data - min)/(max-min)

class GpData(Dataset):
    def __init__(self, file_path,step_len):
        self.step_len = step_len
        temp_data = pd.read_csv('data/AAPL_long.csv')
        data = temp_data.iloc[:, 1:]
        all_data = ta.add_all_ta_features(data, open="Open", high="High", low="Low", close="Close", volume="Volume", fillna=True)
        scaler = MinMaxScaler()

        self.data = scaler.fit_transform(all_data.values).astype(np.float32)
        # self.data = np.zeros((len(all_data), 89), dtype=np.float32)
        # temp_y = []
        # for i, line in enumerate(all_data):
        #     line_data = line.strip().split(",")[1:-1]
        #     for j in range(len(line_data)):
        #         self.data[i][j] = float(line_data[j])
        # self.data = minmaxscaler(self.data)


    def __getitem__(self, item):
        x = self.data[item:item+self.step_len]
        # y = self.data[item+self.step_len]
        y = np.zeros((1),dtype=np.long)
        y[0] =  1 if self.data[item+self.step_len][3] > self.data[item+self.step_len-1][3] else 0
        t_x = torch.from_numpy(x)
        t_y = torch.from_numpy(y)
        # t_y = t_y.reshape(1,6)
        # t_y = t_y.reshape(2)
        t_y = t_y.type(torch.long)
        return t_x,t_y

    def __len__(self):
        return self.data.shape[0]-self.step_len


class PriceGpData(Dataset):
    def __init__(self, file_path,step_len):
        self.step_len = step_len
        temp_data = pd.read_csv('data/AAPL_long.csv')
        data = temp_data.iloc[:, 1:]
        # y_scaler = MinMaxScaler()
        # self.y = y_scaler.fit_transform(temp_data.iloc[:, 3].values.reshape(1, -1)).astype(np.float32)
        # self.y = temp_data.iloc[:, 3].values


        all_data = ta.add_all_ta_features(data, open="Open", high="High", low="Low", close="Close", volume="Volume", fillna=True)
        self.y = all_data.iloc[:, 3]
        self.x = all_data.drop(['Close'], axis=1)
        x_scaler = MinMaxScaler()
        self.scaler = x_scaler

        self.data = x_scaler.fit_transform(self.x.values).astype(np.float32)
        # self.data = self.x.values.astype(np.float32)


    def __getitem__(self, item):
        x = self.data[item:item+self.step_len]
        # y = self.data[item+self.step_len]
        y = np.zeros((1),dtype=np.float32)
        y[0] = self.y[item+self.step_len]
        t_x = torch.from_numpy(x)
        t_y = torch.from_numpy(y)
        # t_y = t_y.reshape(1,6)
        # t_y = t_y.reshape(2)
        # t_y = t_y.type(torch.long)
        return t_x,t_y

    def __len__(self):
        return self.data.shape[0]-self.step_len

class GpModel(nn.Module):
    def __init__(self, input_size,output_size,step_len):
        super(GpModel, self).__init__()
        self.step_len = step_len
        self.layer = nn.Sequential(
            nn.Linear(input_size,128),
            nn.ReLU(),
            nn.Linear(128, 16),
            nn.ReLU(),
            nn.Linear(16,1),
            nn.ReLU(),
        )
        self.out = nn.Linear(self.step_len,2)

    def forward(self, x):
        y = self.layer(x)
        y = y.reshape(y.shape[0],1,self.step_len)
        res = self.out(y)
        res = res.reshape(res.shape[0],2)
        # print(res.shape)
        # res = res.type(torch.long)
        return res


class LstmModel(nn.Module):
    def __init__(self, input_size,hidden_size=1, num_classes=2, output_size=2,step_len=50):
        super(LstmModel, self).__init__()
        self.step_len = step_len
        self.num_layers = 4
        self.hidden_size = hidden_size
        self.lstm = nn.LSTM(input_size, hidden_size)
        self.fc = nn.Linear(step_len, num_classes)

    def forward(self, x):
        x,_ = self.lstm(x)
        x = x.transpose(0,1)
        x = x.transpose(1,2)
        # print(x.shape)
        out = self.fc(x) 
        out = out.reshape(x.shape[0],2)
        return out

class PriceLstmModel(nn.Module):
    def __init__(self, input_size,hidden_size=64, num_classes=1, output_size=2,step_len=50):
        super(PriceLstmModel, self).__init__()
        self.step_len = step_len
        self.num_layers = 4
        self.hidden_size = hidden_size
        self.lstm = nn.LSTM(
            input_size=input_size,
            hidden_size=64,
            num_layers=1,
            batch_first=True,
        )
        self.fc = nn.Linear(40, 1)
        self.fc1 = nn.Linear(64, 1)

    def forward(self, x):
        x,_ = self.lstm(x)
        # print(x.shape)
        x = x.transpose(0,1)
        x = x.transpose(1,2)
        # print(x.shape)
        out = self.fc(x) 
        out = out.transpose(1, 2)
        out = self.fc1(out)
        # print(out.shape)
        # out = out
        # out = out.reshape(x.shape[0],2)
        return out



class LSTMNet(nn.Module):
 
    def __init__(self, input_size):
        super(LSTMNet, self).__init__()
        self.rnn = nn.LSTM(
            input_size=input_size,
            hidden_size=64,
            num_layers=1,
            batch_first=True,
        )
        self.out = nn.Sequential(
            nn.Linear(64, 1)
        )
 
    def forward(self, x):
        r_out, (h_n, h_c) = self.rnn(x, None)  # None 表示 hidden state 会用全0的 state
        # print(r_out.shape)
        out = self.out(r_out[:, :, 0])
        print(out.shape)
        return out

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
    def forward(self, _x):
        x, _ = self.lstm(_x)  # _x is input, size (seq_len, batch, input_size)
        s, b, h = x.shape  # x is output, size (seq_len, batch, hidden_size)
        x = x.view(s*b, h)
        x = self.fc(x)
        x = x.view(s, b, -1)  # 把形状改回来
        # print(x.shape)
        return x

class PriceModel(object):
    def train(self, file_path,step_len):
        data = PriceGpData(file_path,step_len)
        D = DataLoader(dataset=data,batch_size=64,shuffle=True)
        # model = GpModel(6,2,step_len)
        model = PriceLstmModel(88)
        criterion = nn.MSELoss()
        optimizer = torch.optim.Adam(model.parameters(), lr=1e-1)
        for ep in range(30):
            for i,(x,y) in enumerate(D):
                x = x.transpose(0,1)
                pre_y = model(x)
                y = y.reshape(y.shape[0])
                # print(pre_y.shape, y.shape)
                loss = criterion(pre_y,y)
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()
                if i%100 == 0:
                    print('Epoch: {}, Loss: {:.5f}'.format(ep + 1, loss))
        
        return model, step_len, data
            # self.test(model,file_path,step_len, data)


    def test(self, model,step_len, test_data):
        # model = model.eval() # 转换成测试模式
        # # 注意这里用的是全集 模型的输出长度会比原数据少DAYS_FOR_TRAIN 填充使长度相等再作图
        # dataset_x = test_data.x.values.reshape(-1, 1, 88).astype('float32')  # (seq_size, batch_size, feature_size)
        # dataset_x = torch.from_numpy(dataset_x)
        # pred_test = model(dataset_x) # 全量训练集的模型输出 (seq_size, batch_size, output_size)
        # pred_test = pred_test.view(-1).data.numpy()
        # pred_test = np.concatenate((np.zeros(88), pred_test))  # 填充0 使长度相同
        # print(pred_test)
        # return pred_test


        model.eval()
        scaler = MinMaxScaler()
        criterion = nn.MSELoss()
        # test_data = GpData(file_path, step_len)
        test_D = DataLoader(dataset=test_data, batch_size=64)
        softmax_func = nn.Softmax(dim=1)
        pred_res = []
        all_loss = []
        

        for i,(test_x,test_y) in enumerate(test_D):
            print(test_x.shape)
            test_x = test_x.transpose(0, 1)
            pre_test_y = model(test_x)
            print(pre_test_y.shape, test_y.shape)
            # pred_res.append([item.item() for item in pre_test_y])

            # test_loss = softmax_func(pre_test_y)
            test_loss = criterion(pre_test_y, test_y)
            # print(pre_test_y.shape, test_y[0])
            # print(len(test_loss))
            # print(test_loss)
            # for i in range(len(pre_test_y)):
            #     pred_res.append(torch.argmax(pre_test_y[i]).item() & test_y[i].item())
            # pred_res.extend([item for item in torch.argmax(pre_test_y).item() & test_y.item()])
            temp_d = pre_test_y.reshape(pre_test_y.shape[0])
            # print(temp_d.shape)
            pred_res.extend([item.item() for item in temp_d])
            all_loss.append(test_loss.item())
        # ori_pred = test_data.scaler.inverse_transform(pred_res)
        # print(ori_pred)
        

        def inverse_trans(val):
            # print(val)
            min_data = test_data.scaler.get_params()["feature_range"][0]
            max_data = test_data.scaler.get_params()["feature_range"][1]
            std_x = (val-min_data)/(max_data-min_data)
            real_x = std_x*(test_data.scaler.data_max_[3]-test_data.scaler.data_min_[3])+test_data.scaler.data_min_[3]
            return real_x
        
        # print(pred_res)
        real_pred = [inverse_trans(item) for item in pred_res]
        print(real_pred[0])
        print(len(pred_res), len(test_D))
        print('test_prec: {:.5f}'.format(sum(all_loss) / len(test_data)))
        return real_pred, pred_res, 


class RiseFallModel(object):

    def train(self, file_path,step_len):
        data = GpData(file_path,step_len)
        D = DataLoader(dataset=data,batch_size=64,shuffle=True)
        # model = GpModel(6,2,step_len)
        model = LstmModel(89)
        criterion = nn.CrossEntropyLoss()
        optimizer = torch.optim.Adam(model.parameters(), lr=1e-4)
        for ep in range(30):
            for i,(x,y) in enumerate(D):
                x = x.transpose(0,1)
                pre_y = model(x)
                y = y.reshape(y.shape[0])
                # print(pre_y.shape, y.shape)
                loss = criterion(pre_y,y)
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()
                if i%100 == 0:
                    print('Epoch: {}, Loss: {:.5f}'.format(ep + 1, loss))
            test(model,file_path,step_len, data)


    def test(self, model,file_path,step_len, test_data):
        model.eval()
        criterion = nn.CrossEntropyLoss()
        # test_data = GpData(file_path, step_len)
        test_D = DataLoader(dataset=test_data, batch_size=64)
        softmax_func = nn.Softmax(dim=1)
        pred_res = []

        for i,(test_x,test_y) in enumerate(test_D):
            test_x = test_x.transpose(0, 1)
            pre_test_y = model(test_x)

            test_loss = softmax_func(pre_test_y)
            # print(len(test_loss))
            # print(test_loss)
            for i in range(len(pre_test_y)):
                pred_res.append(torch.argmax(pre_test_y[i]).item() & test_y[i].item())
            # pred_res.extend([item for item in torch.argmax(pre_test_y).item() & test_y.item()])

            # all_loss.append(test_loss.item())

        print(len(pred_res), len(test_D))
        print('test_prec: {:.5f}'.format(sum(pred_res)/len(test_data)))

if __name__ == '__main__':
    cur_model = PriceModel()
    trained_model, step_len, data = cur_model.train(file_path="data\\AAPL_long.csv",step_len=40)
    torch.save(trained_model, 'model.pth')
    real_pred_y, scaled_pred_y = cur_model.test(trained_model, step_len, data)
    # print(real_pred_y)
    print(scaled_pred_y)
    print(data.y)

    import matplotlib.pyplot as plt

    plt.plot(data.y, 'r', label='prediction')
    plt.plot(scaled_pred_y, 'b', label='real')
    plt.show()





