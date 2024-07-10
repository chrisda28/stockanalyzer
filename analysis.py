import pandas as pd
import numpy as np
import seaborn as sb
import matplotlib.pyplot as plt
from sklearn import preprocessing, svm
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

boa_df = pd.read_csv("stock_data_BAC")
c_df = pd.read_csv("stock_data_C")
gs_df = pd.read_csv("stock_data_GS")
jpm_df = pd.read_csv("stock_data_JPM")

frames_dict = {
    "BOA": boa_df,
    "C": c_df,
    "GS": gs_df,
    "JPM": jpm_df,
}


def calc_daily_returns():
    """creates list of dataframes for each stock consisting of daily returns"""
    daily_returns = {}
    for key, value in frames_dict.items():
        frame = frames_dict[key].rename(columns={'Unnamed: 0': 'date'})  # Rename the unnamed column to 'date'
        frame['date'] = pd.to_datetime(frame['date'])  # Ensure the 'date' column is datetime

        frame['daily returns'] = frame['close'].pct_change()   # finding the daily returns and setting column name
        frame.set_index('date', inplace=True)  # setting the index of the entire frame before making a series
        series = frame['daily returns']        # creating series for each of stocks returns

        daily_returns[key] = series

    returns_df = pd.DataFrame.from_dict(daily_returns)
    returns_df.drop(index=returns_df.index[0], axis=0, inplace=True)  # removing the first row that has NaN values

    return returns_df


def calc_correlation(dataframe):
    correl_df = dataframe.corr(method="pearson", numeric_only=False)
    return correl_df


def calc_stdev(dataframe):
    stdev_df = dataframe.std(axis=0, skipna = True, ddof=1, numeric_only=False)
    return stdev_df


def prep_data_for_model(single_stock_dataframe):
    """modifies dataframe by finding moving average, daily returns, and previous day close price
     single stock to be used in linear regression model"""
    single_stock_dataframe.rename(columns={'Unnamed: 0': 'date'}, inplace=True)
    single_stock_dataframe['date'] = pd.to_datetime(single_stock_dataframe['date'])

    single_stock_dataframe.set_index('date', inplace=True)  # setting the index of the entire frame
    single_stock_dataframe.sort_index(inplace=True)

    single_stock_dataframe['daily returns'] = single_stock_dataframe['close'].pct_change()  # finding the daily returns
    # and setting column name

    single_stock_dataframe['20 day moving average'] = single_stock_dataframe['close'].rolling(window=20).mean()  # find
    # the 20-day moving average
    single_stock_dataframe['previous day close'] = single_stock_dataframe['close'].shift(periods=1)   # create column
    # for previous day close

    single_stock_dataframe.drop(index=single_stock_dataframe.index[:19], axis=0, inplace=True)
    prepped_frame = single_stock_dataframe.reset_index(drop=True)  # removing first 19 rows that have NaN values
    # because of the 20-day moving average calc column, need this for clean model data

    return prepped_frame


def train_linreg_model(dataframe):
    prepped_data = prep_data_for_model(dataframe)

    x = prepped_data[['20 day moving average', 'close']]
    y = prepped_data['daily returns']  # attempting to predict the daily returns

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25)  # Splitting the data into
    # training and testing data

    model = LinearRegression()

    model.fit(x_train, y_train)
    score = model.score(x_test, y_test)
    return model, score


def predict_returns(model, x):
    return model.predict(x)


def show_plot(column1, column2, prepped_data):
    return sb.lmplot(x=column1, y=column2, data=prepped_data, order=2, ci=None)


def correl_heatmap():
    stock_daily_returns = calc_daily_returns()
    correl_matrix = calc_correlation(stock_daily_returns)
    return sb.heatmap(correl_matrix)


















