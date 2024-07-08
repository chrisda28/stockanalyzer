import pandas as pd

boa_df = pd.read_csv("stock_data_BAC")
c_df = pd.read_csv("stock_data_C")
gs_df = pd.read_csv("stock_data_GS")
jpm_df = pd.read_csv("stock_data_JPM")

frames = [boa_df, c_df, gs_df, jpm_df]


def calc_daily_returns():
    """creates list of dataframes for each stock consisting of daily returns"""
    daily_return_list = []
    for frame in frames:
        frame = frame.rename(columns={'Unnamed: 0': 'date'})  # Rename the date column
        frame['date'] = pd.to_datetime(frame['date'])  # Ensure the 'date' column is datetime
        frame['returns'] = frame['close'].pct_change()   # Calculate daily returns
        columns_to_include = ['date', 'returns', "ticker"]  # Create a new DataFrame with date, ticker, and returns
        daily_returns = frame[columns_to_include].copy()
        daily_return_list.append(daily_returns)

    return daily_return_list




daily_returns = calc_daily_returns()
for df in daily_returns:
    # print(df.head())
    print(df)



def calc_correlation():
    pass
