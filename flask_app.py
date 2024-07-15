import pandas as pd
from flask import Flask, render_template, url_for
from data import get_stock_df, get_multiple_stock_df
from analysis import (make_plot, calc_correlation, calc_stdev, calc_daily_returns, train_linreg_model, predict_returns,
                      prep_data_for_model, correl_heatmap)
import io
import base64

INTERESTED_STOCKS = ["JPM", "GS", "BAC", "C"]

app = Flask(__name__)


@app.route("/")
def home():
    return render_template('home.html', title='Stock Analysis',
                           header='Analyzing Major Bank Stocks',
                           )


@app.route("/dailyreturns")
def daily_returns():
    print("hi")
    # frame_dict = get_multiple_stock_df(tickers=INTERESTED_STOCKS)
    # for ticker, frame in frame_dict.items():
    #     stock_returns = calc_daily_returns(frame)
    #     make_plot(columnx=ticker, columny=stock_returns)


@app.route("/20daymovingavg")
def moving_average():

    return render_template('index.html', title='Stock Analysis',
                           header='Analyzing Major Bank Stocks',
                           section_title='Analysis Notes',
                           content='Presenting a basic analysis of JPMorgan, Goldman Sachs,'
                                   ' Citigroup, and Bank of America. Time series data for the past 20 years is pulled'
                                   ' from AlphaVantage free API. From this data, python scripts calculate daily returns,'
                                   ' correlation, standard deviation, and model a basic linear regression.'
                                   ' The model predicts daily returns with the 20-day moving average price.')


@app.route("/correlation")
def correlation():
    frame_dict = get_multiple_stock_df(INTERESTED_STOCKS)
    heatmap = correl_heatmap(frame_dict)
    print(len(heatmap))
    return render_template('index.html', title='Correlation',
                           header='Finance Stock Analysis',
                           section_title='correlation',
                           content='hiiiiiii', image=heatmap)


@app.route("/stdev")
def standard_deviation():
    return render_template('index.html', title='Stock Analysis',
                           header='Analyzing Major Bank Stocks',
                           section_title='Analysis Notes',
                           content='Presenting a basic analysis of JPMorgan, Goldman Sachs,'
                                   ' Citigroup, and Bank of America. Time series data for the past 20 years is pulled'
                                   ' from AlphaVantage free API. From this data, python scripts calculate daily returns,'
                                   ' correlation, standard deviation, and model a basic linear regression.'
                                   ' The model predicts daily returns with the 20-day moving average price.')


@app.route("/linreg")
def linear_regression():
    print("hi")


if __name__ == "__main__":
    app.run(debug=True)




