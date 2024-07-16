import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import os


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


def make_stdev_plot(series):
    df = series.reset_index()
    df.columns = ["Ticker", "Standard Deviation of Daily Returns"]  # turning series to dataframe
    sb.barplot(data=df, orient="v", x='Ticker', y='Standard Deviation of Daily Returns')
    plt.tight_layout()  # Adjust the plot to ensure everything fits without overlapping

    static_dir = os.path.join(os.getcwd(), 'static')
    img_path = os.path.join(static_dir, 'stdev_plot.png')

    plt.tight_layout()
    plt.savefig(img_path, format='png', dpi=300)  # saving plot as an image to be used in flask app
    plt.close()  # closing matplotlib figure to free up memory

    print(f"Plot saved to {img_path}")
    return img_path



def prep_data_for_model(df):
    """prepares data to be used in the linear regression model"""
    df = df.copy()   # making copy to avoid messing with original
    df['daily returns'] = df['close'].pct_change()  # finding the daily returns
    # and setting column name
    df['20 day moving average'] = df['close'].rolling(window=20).mean()  # find
    # the 20-day moving average
    df['previous day close'] = df['close'].shift(periods=1)   # create column
    # for previous day close
    prepped_frame = df.dropna().reset_index()  # removing NaN values
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


def prepare_data_for_plotting(df):
    """Prepare data specifically for plotting without affecting original calculations"""
    plot_df = df.copy()  # making copy of df
    plot_df.index = pd.to_datetime(plot_df.index)  # make date column datetime
    plot_df.sort_index(inplace=True)   # sort by date
    plot_df['20 day moving average'] = plot_df['close'].rolling(window=20).mean()  # calc 20 day moving average
    return plot_df.dropna()


def make_20dayma_plot(prepped_data, title):
    """Generate plot and return it as an image"""
    fig, ax = plt.subplots(figsize=(15, 8))
    sb.lineplot(data=prepped_data, x=prepped_data.index, y=prepped_data['20 day moving average'], ax=ax)
    ax.set_title(title)
    ax.set_xlabel("Date")
    ax.set_ylabel("20-Day Moving Average")

    # Configure x-axis to show only years
    years = mdates.YearLocator(5)  # every 5 years there is a tick
    years_fmt = mdates.DateFormatter('%Y')
    ax.xaxis.set_major_locator(years)
    ax.xaxis.set_major_formatter(years_fmt)

    # Add minor ticks for each year
    ax.xaxis.set_minor_locator(mdates.YearLocator())

    # Rotate and align the tick labels so they look better
    fig.autofmt_xdate()

    # Adjust y-axis to start from 0
    ax.set_ylim(bottom=0)

    # Add grid for better readability
    ax.grid(True, linestyle='--', alpha=0.7)

    ax.set_xlim(prepped_data.index.min(), prepped_data.index.max())   # sets the x-axis
    # limits to follow date range of data

    static_dir = os.path.join(os.getcwd(), 'static')
    img_path = os.path.join(static_dir, 'goldmansachs20dayma.png')

    plt.tight_layout()
    plt.savefig(img_path, format='png', dpi=300)
    plt.close(fig)

    print(f"Plot saved to {img_path}")
    return img_path


def make_plot(columnx, columny, prepped_data, title):   ## NEED TO ADJUST THIS TO SAVE IMG IN STATIC FOLDER
    """generate plot and return it as an image"""
    sb.lmplot(x=columnx, y=columny, data=prepped_data, order=2, ci=None)   # generates scatter plot w regression line
    plt.title(title)   # setting title name of plot
    static_dir = os.path.join(os.getcwd(), 'static')
    img_path = os.path.join(static_dir, 'linreg_plot.png')

    plt.tight_layout()
    plt.savefig(img_path, format='png', dpi=300)  # saving plot as an image to be used in flask app
    plt.close()  # closing matplotlib figure to free up memory

    print(f"Plot saved to {img_path}")
    return img_path


def correl_heatmap(stock_data_dict):
    """makes correlation heatmap and returns it as an image"""
    correl_matrix = calc_correlation(stock_data_dict)
    heatmap = sb.heatmap(correl_matrix, annot=True, vmin=0, vmax=1, square=True, center=0, cmap='coolwarm')
    plt.title("Correlation Heatmap of Daily Returns", fontsize=16)  # setting title name of plot
    static_dir = os.path.join(os.getcwd(), 'static')
    img_path = os.path.join(static_dir, 'correlation_heatmap.png')

    plt.tight_layout()
    plt.savefig(img_path, format='png', dpi=300)   # saving plot as an image to be used in flask app
    plt.close(heatmap)  # closing matplotlib figure to free up memory

    print(f"Plot saved to {img_path}")
    return img_path


if __name__ == "__main__":
    from data import get_multiple_stock_df
    tickers = ['JPM', 'GS', 'BAC', 'C']
    stock_dict = get_multiple_stock_df(tickers)
    stdev = calc_stdev(stock_dict)
    make_stdev_plot(stdev)





# if __name__ == "__main__":
#     from data import get_stock_df
#
#     test_ticker = "JPM"
#     try:
#         stock_data = get_stock_df(test_ticker)
#         if stock_data is not None:
#             prep = prep_data_for_model(stock_data)
#             print(prep.head())  # Print the first few rows to check the structure
#             plot = make_plot('20 day moving average', 'daily returns', prep, f"{test_ticker} Linear Regression")
#             print(plot)
#         else:
#             print(f"No data received for {test_ticker}")
#     except Exception as e:
#         print(f"An error occurred: {e}")












