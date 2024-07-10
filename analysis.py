import pandas as pd
import numpy as np
import seaborn as sb
import matplotlib.pyplot as plt
from sklearn import preprocessing, svm
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression


def calc_daily_returns(df):
    """find the daily returns for a single stock"""
    df['daily returns'] = df['close'].pct_change()  # calc the returns
    return df['daily returns'].dropna()  # removing Nan values (i.e. the first row I think)


def calc_correlation(dataframe_dict):
    """return correl matrix from multiple stocks"""
    returns_dict = {ticker: calc_daily_returns(df) for ticker, df in dataframe_dict.items()}  # creating dict with
    # ticker as the key and the calculated returns dataframe for each value
    returns_df = pd.DataFrame(returns_dict)  # turning the dict into a dataframe, so we can calc correl matrix
    correl_matrix = returns_df.corr(method="pearson")  # calc correl matrix
    return correl_matrix


def calc_stdev(dataframe_dict):  # works the same way as the calc_correlation function above
    """return stdev of multiple stocks based on their returns"""
    returns_dict = {ticker: calc_daily_returns(df) for ticker, df in dataframe_dict.items()}
    returns_df = pd.DataFrame(returns_dict)
    stdev_df = returns_df.std(axis=0, skipna=True, ddof=1, numeric_only=False)
    return stdev_df


def prep_data_for_model(df):
    """prepares data to be used in the linear regression model"""

    df['daily returns'] = df['close'].pct_change()  # finding the daily returns
    # and setting column name
    df['20 day moving average'] = df['close'].rolling(window=20).mean()  # find
    # the 20-day moving average
    df['previous day close'] = df['close'].shift(periods=1)   # create column
    # for previous day close
    prepped_frame = df.dropna().reset_index(drop=True)  # removing NaN values
    # because of the 20-day moving average calc column, need this for clean model data, setting drop to true disregards
    # the old index. then resetting index
    return prepped_frame


def train_linreg_model(dataframe):
    """trains linreg model"""
    prepped_data = prep_data_for_model(dataframe)
    # using 20 day moving average and close price for model
    x = prepped_data[['20 day moving average', 'close']]
    y = prepped_data['daily returns']  # attempting to predict the daily returns

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25)  # Splitting the data into
    # training and testing data with 75%-25% split. so 75% is for training and 25% is for testing

    model = LinearRegression()   # initialize model

    model.fit(x_train, y_train)  # train the model using the data
    score = model.score(x_test, y_test)  # evaluate model by giving the r squared
    # which tells how well the predictions match the actual data
    return model, score


def predict_returns(model, x):
    """predict returns using training model"""
    return model.predict(x)


def show_plot(column1, column2, prepped_data):
    return sb.lmplot(x=column1, y=column2, data=prepped_data, order=2, ci=None)


def correl_heatmap():
    stock_daily_returns = calc_daily_returns()
    correl_matrix = calc_correlation(stock_daily_returns)
    return sb.heatmap(correl_matrix)


















