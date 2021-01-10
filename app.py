from flask import Flask, render_template, request, redirect
import requests
#import json
import pandas as pd
import numpy as np
from bokeh.plotting import figure, show
from bokeh.embed import components
#import simplejson as json

app=Flask(__name__)

@app.route('/get_stocks',methods=['POST'])
def get_stock():

	ticker=request.form['ticker']
	month=request.form['month']
	year=request.form['year']

	key = 'W02IFYLEK6Y1T64F'

	#url and key work
	url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={}&apikey={}'.format(ticker,key)

	response = requests.get(url)

	json_ret=response.json()

	df=pd.DataFrame(json_ret["Time Series (Daily)"].values(),index=json_ret["Time Series (Daily)"].keys())

	match_str='{}-{}-'.format(year,month)

	dates=[date for date in df.index if (match_str in str(date))]

	days=[int(date.split('-')[2]) for date in dates]

	sub_df=df[df.index.isin(dates)]

	prices=[]
	for i in sub_df['5. adjusted close']:
		prices.append(float(i))

	#plot days vs prices
	x=days
	y=prices
	plot = figure(plot_width=400, plot_height=400, toolbar_location="below",
		title='{} adjusted closing prices for {}-{}'.format(ticker,year,month),x_axis_label='day',y_axis_label='price (USD)')
	plot.line(x,y)

	script, div = components(plot)
	kwargs = {'script': script, 'div': div}
	kwargs['title'] = 'bokeh-with-flask' 
	return render_template('plot.html', **kwargs)

@app.route('/')
def index_page():
	return render_template('query_page.html')

#remove debug mode later
if __name__ == '__main__':
    app.run(debug=False)
