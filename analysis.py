import pandas as pd

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



boo = calc_daily_returns()
print(boo)

















def calc_correlation(frame1, frame2):
    pass





def calc_stdev():
    pass


def calc_sharpe():
    pass




# def calc_daily_returns():
#     """creates list of dataframes for each stock consisting of daily returns"""
#     daily_returns = []
#     for frame in frames:
#         frame = frame.rename(columns={'Unnamed: 0': 'date'})  # Rename the date column
#         frame['date'] = pd.to_datetime(frame['date'])  # Ensure the 'date' column is datetime
#         frame['returns'] = frame['close'].pct_change()   # Calculate daily returns
#         columns_to_include = ['date', 'returns', "ticker"]
#         daily_returns_ = frame[columns_to_include].copy()  # Create a new DataFrame with date, ticker, and returns
#         daily_returns.append(daily_returns_)
#     daily_returns_df = pd.concat(daily_returns)    # use the axis=horizontal parameter to join them horizontally
#
#     return daily_returns_df
#
# daily_returns = calc_daily_returns()
# print(daily_returns)



# boo = boa_df.corr(method="pearson", numeric_only=False)
#
# print(boo)