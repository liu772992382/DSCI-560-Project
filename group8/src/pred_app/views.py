from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils.html import escapejs
# from pred_app.lstm_prediction import *
import json
import pandas as pd

# --------------- MAIN WEB PAGES -----------------------------
def redirect_root(request):
    return redirect('/new_page/aapl')

def index(request):
	return render(request, 'pred_app/index.html') 

def pred(request):
    return render(request, 'pred_app/prediction.html')

def contact(request):
	return render(request, 'pred_app/contact.html')

def new_data(request):
	
	stock_symbol = request.GET['stock_symbol']
	# stock_symbol = 'aapl'
	print(stock_symbol)
	# predicted_result_df = lstm_prediction(se, stock_symbol)
	stock_symbol = stock_symbol.lower()
	# print(stock_symbol)
	pred_df = pd.read_csv(f'data/{stock_symbol}_pred.csv').to_dict(orient='records')

	ori_df = pd.read_csv(f'data/{stock_symbol}_ori.csv').to_dict(orient='records')
	# print(predicted_result_df)
	# vis = predicted_result_df + ori_df
	res = []
	for i, item in enumerate(pred_df):
		tmp = item
		if i < len(ori_df):
			tmp['Close2'] = ori_df[i]['Close'] 
			tmp['Volume'] = ori_df[i]['Volume']
		res.append(tmp)

	len_pred_df = len(pred_df)
	pred = [(round(ori_df[-1]['Close'], 2), '-')]
	pred.extend([(round(pred_df[i]['Close'], 2), 'Up' if pred_df[i]['Close'] > ori_df[-1]['Close'] else 'Down') 
				for i in range(len_pred_df-3, len_pred_df)])

	full_res = {'chart': res, 'pred': pred}
	predicted_result_df = json.dumps(full_res)

	response = HttpResponse(predicted_result_df, content_type="plain/text")

	response.headers['Access-Control-Allow-Origin'] = '*'
	response.headers['Origin'] = '*'

	return response

def new_page(request, stock_symbol='aapl'):
	return render(request, f'pred_app/new_{stock_symbol}.html')

def search(request, se, stock_symbol):
	
	# predicted_result_df = lstm_prediction(se, stock_symbol)
	stock_symbol = stock_symbol.lower()
	# print(stock_symbol)
	pred_df = pd.read_csv(f'data/{stock_symbol}_pred.csv').to_dict(orient='records')

	ori_df = pd.read_csv(f'data/{stock_symbol}_ori.csv').to_dict(orient='records')
	# print(predicted_result_df)
	# vis = predicted_result_df + ori_df
	res = []
	for i, item in enumerate(pred_df):
		tmp = item
		tmp['Close2'] = ori_df[i]['Close']
		tmp['Volume'] = ori_df[i]['Volume']
		res.append(tmp)


	predicted_result_df = json.dumps(res)

	return render(request, 'pred_app/search.html', {"predicted_result_df": predicted_result_df})
# -----------------------------------------------------------