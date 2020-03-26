import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
from mpl_finance import candlestick_ohlc
import matplotlib.dates as mdates
import pandas as pd
import os
import pandas_datareader.data as web
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

style.use('ggplot')
index = 'AAPL'

def read_into_csv(update=False):
	start = dt.datetime(2000,1,1)
	end = dt.datetime(2019,12,9)

	if (not os.path.exists(f'data/{index}.csv')) or update:
		df = web.DataReader(index, 'yahoo', start, end)
		df.to_csv(f'data/{index}.csv')
		print(f'Data written into data/{index}.csv')
	else:
		print(f'data/{index}.csv already exists')

def read_from_csv(filename):
	data = pd.read_csv(filename, parse_dates=True, index_col=0)
	return data

def display_moving_average_and_volume():
	df['100ma'] = df['Adj Close'].rolling(window=100, min_periods=0).mean()
	

	ax1.plot(df.index, df['Adj Close'])
	ax1.plot(df.index, df['100ma'])
	ax2.bar(df.index, df['Volume'])


if __name__ == '__main__':
	read_into_csv(update=False) # To read data into csv
	df = read_from_csv(f'data/{index}.csv')

	ax1 = plt.subplot2grid((18,1), (0,0), rowspan=14, colspan=1, title=f'{index} stock history')
	ax2 = plt.subplot2grid((18,1), (15,0), rowspan=3, colspan=1, sharex=ax1)
	ax1.xaxis_date()

	df_ohlc = df['Adj Close'].resample('10D').ohlc() # Vary this
	df_volume = df['Volume'].resample('10D').sum()

	df_ohlc.reset_index(inplace=True)

	df_ohlc['Date'] = df_ohlc['Date'].map(mdates.date2num)
	candlestick_ohlc(ax1, df_ohlc.values, width=2, colorup='g')
	ax2.fill_between(df_volume.index.map(mdates.date2num), df_volume.values, 0)


	plt.show()
	plt.close()







