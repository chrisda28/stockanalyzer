import pandas as pd

TRADING_DAYS_PER_YEAR = 252
RISK_FREE_RATE = .05


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
    return dataframe.corr(method="pearson", numeric_only=False)


def calc_stdev(dataframe):
    return dataframe.std(axis=0, skipna = True, ddof=1, numeric_only=False)

# boo = calc_daily_returns()
# boob = calc_stdev(boo)
# print(boob)


def prep_data_for_model(single_stock_dataframe):
    """returns a modified dataframe for single stock to be used in linear regression model"""
    single_stock_dataframe.rename(columns={'Unnamed: 0': 'date'}, inplace=True)
    single_stock_dataframe['date'] = pd.to_datetime(single_stock_dataframe['date'])

    single_stock_dataframe.set_index('date', inplace=True)  # setting the index of the entire frame
    single_stock_dataframe.sort_index(inplace=True)

    single_stock_dataframe['daily returns'] = single_stock_dataframe['close'].pct_change()  # finding the daily returns
    # and setting column name
    single_stock_dataframe.drop(index=single_stock_dataframe.index[0], axis=0, inplace=True)  # removing the first row
    # that has NaN values


#### check the recent message incladue
    prepped_dataframe = pass

    return prepped_dataframe








