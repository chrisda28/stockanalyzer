import pandas as pd
import seaborn as sb
import os
import matplotlib
matplotlib.use('Agg')  # this allows matplotlib to use different backend
# that doesn't require GUI. Resolved threading issues
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

os.environ['OPENBLAS_NUM_THREADS'] = '1'  # numpy and scikit-lear use OpenBLAS for math operations,
# so limiting this to 1 thread will help it not interfere with flask


def calc_daily_returns(df):
    """find the daily returns for a single stock"""
    df['daily returns'] = df['close'].pct_change()  # calculate the returns
    return df['daily returns'].dropna()  # removing Nan values (i.e. the first row I think)


def calc_correlation(dataframe_dict):
    """return correl matrix from multiple stocks"""
    returns_dict = {ticker: calc_daily_returns(df) for ticker, df in dataframe_dict.items()}  # creating dict with
    # ticker as the key and the calculated returns dataframe for each value
    returns_df = pd.DataFrame(returns_dict)  # turning the dict into a dataframe, so we can calc correl matrix
    correl_matrix = returns_df.corr(method="pearson")  # calc correl matrix
    return correl_matrix


def calc_stdev(dataframe_dict):  # works the same way as the calc_correlation function above
    """return standard deviation of multiple stocks based on their returns"""
    returns_dict = {ticker: calc_daily_returns(df) for ticker, df in dataframe_dict.items()}
    returns_df = pd.DataFrame(returns_dict)
    stdev_df = returns_df.std(axis=0, skipna=True, ddof=1, numeric_only=False)
    return stdev_df


def make_stdev_plot(series):
    """make barplot showing company standard deviations"""
    df = series.reset_index()  # converts series to a data frame
    df.columns = ["Ticker", "Standard Deviation of Daily Returns"]  # renaming columns
    sb.barplot(data=df, orient="v", x='Ticker', y='Standard Deviation of Daily Returns')  # create barplot
    plt.tight_layout()  # Adjust the plot to ensure everything fits without overlapping

    static_dir = os.path.join(os.getcwd(), 'static')
    img_path = os.path.join(static_dir, 'stdev_plot.png')  # get hold of image path so it can be saved

    plt.tight_layout()  # prevents layout from overlapping
    plt.savefig(img_path, format='png', dpi=300)  # saving plot as an image to be used in flask app
    plt.close()  # closing matplotlib figure to free up memory

    print(f"Plot saved to {img_path}")
    return img_path


def prep_data_for_model(df):
    """prepares data to be used in the linear regression model"""
    df = df.copy()   # making copy to avoid messing with original
    if not isinstance(df.index, pd.DatetimeIndex):  # check if df is in datetime format
        df.index = pd.to_datetime(df.index)  # convert to datetime if needed
    df['daily returns'] = df['close'].pct_change()  # finding the daily returns
    # and setting column name
    df['20 day moving average'] = df['close'].rolling(window=20).mean()  # find
    # the 20-day moving average
    df['previous day close'] = df['close'].shift(periods=1)   # create column
    # for previous day close
    return df.dropna()    # removing NaN values


def train_linreg_model(dataframe):
    """trains linreg model"""
    prepped_data = prep_data_for_model(dataframe)
    # using 20 day moving average and close price for model
    x = prepped_data[['20 day moving average', 'close']]  # declaring model x vars
    y = prepped_data['daily returns']  # attempting to predict the daily returns

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25)  # Splitting the data into
    # training and testing data with 75%-25% split.
    # So 75% is for training and 25% is for testing. AI recommended this split

    model = LinearRegression()   # initialize model

    model.fit(x_train, y_train)  # train the model using the data
    score = model.score(x_test, y_test)  # evaluate model by giving the r squared
    # which tells how well the predictions match the actual data
    return model, score


def predict_returns(model, x):
    """predict returns using training model"""
    return model.predict(x)  # predict next day daily returns (the price change as a percentage)


def prepare_data_for_plotting(df):
    """Prepare data specifically for the 20-day moving average plot"""
    plot_df = df.copy()  # making copy of df
    plot_df.index = pd.to_datetime(plot_df.index)  # make date column datetime
    plot_df.sort_index(inplace=True)   # sort by date
    plot_df['20 day moving average'] = plot_df['close'].rolling(window=20).mean()  # calc 20 day moving average
    return plot_df.dropna()  # drop NaN values


def make_20dayma_plot(prepped_data, title):
    """Generate plot and return it as an image"""
    fig, ax = plt.subplots(figsize=(15, 8))  # create figure and axis, and set size
    sb.lineplot(data=prepped_data, x=prepped_data.index, y=prepped_data['20 day moving average'], ax=ax)  # make plot
    ax.set_title(title)
    ax.set_xlabel("Date")
    ax.set_ylabel("20-Day Moving Average")

    # Configure x-axis to show only years with help of AI
    years = mdates.YearLocator(5)  # every 5 years there is a tick
    years_fmt = mdates.DateFormatter('%Y')
    ax.xaxis.set_major_locator(years)
    ax.xaxis.set_major_formatter(years_fmt)
    ax.xaxis.set_minor_locator(mdates.YearLocator())   # Add minor ticks for each year

    fig.autofmt_xdate()   # Rotate and align the tick labels so they look better
    ax.set_ylim(bottom=0)  # Adjust y-axis to start from 0

    ax.grid(True, linestyle='--', alpha=0.7)  # Add grid for better readability

    ax.set_xlim(prepped_data.index.min(), prepped_data.index.max())   # sets the x-axis
    # limits to follow date range of data

    static_dir = os.path.join(os.getcwd(), 'static')
    img_path = os.path.join(static_dir, 'goldmansachs20dayma.png')   # define img path to enable saving it

    plt.tight_layout()   # prevent layout overlapping
    plt.savefig(img_path, format='png', dpi=300)
    plt.close(fig)   # to free memory

    print(f"Plot saved to {img_path}")
    return img_path


def make_plot(columnx, columny, prepped_data, title):
    """generate linreg plot and return it as an image"""
    fig, ax = plt.subplots()  # create figure and set of axes to plot
    sb.regplot(x=columnx, y=columny, data=prepped_data, order=2, ci=None, ax=ax)  # make scatter plot w regression line
    plt.title(title)   # setting title name of plot
    static_dir = os.path.join(os.getcwd(), 'static')
    img_filename = 'live_linreg_plot.png'
    img_path = os.path.join(static_dir, img_filename)  # getting img pathway so it can be saved

    plt.tight_layout()  # prevent layout overlapping
    plt.savefig(img_path, format='png', dpi=300)  # saving plot as an image to be used in flask app
    plt.close(fig)  # closing matplotlib figure to free up memory

    print(f"Plot saved to {img_path}")
    return img_filename


def correl_heatmap(stock_data_dict):
    """makes correlation heatmap and returns it as an image"""
    correl_matrix = calc_correlation(stock_data_dict)  # get correlation of each stock with each other
    heatmap = sb.heatmap(correl_matrix, annot=True, vmin=0, vmax=1, square=True, center=0, cmap='coolwarm')  # make
    # heatmap of correlations with range being 0 to 1
    plt.title("Correlation Heatmap of Daily Returns", fontsize=16)  # setting title name of plot
    static_dir = os.path.join(os.getcwd(), 'static')
    img_path = os.path.join(static_dir, 'correlation_heatmap.png')  # getting img pathway so it can be saved

    plt.tight_layout()  # prevent layout overlapping
    plt.savefig(img_path, format='png', dpi=300)   # saving plot as an image to be used in flask app
    plt.close(heatmap)  # closing matplotlib figure to free up memory

    print(f"Plot saved to {img_path}")
    return img_path


# if __name__ == "__main__":   # example usage
#     from data import get_multiple_stock_df
#     tickers = ['JPM', 'GS', 'BAC', 'C']
#     stock_dict = get_multiple_stock_df(tickers)
#     stdev = calc_stdev(stock_dict)
#     make_stdev_plot(stdev)









