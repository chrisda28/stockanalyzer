import os.path

import pandas as pd
from flask import Flask, render_template, url_for
from data import get_stock_df, get_multiple_stock_df
from analysis import (make_plot, calc_correlation, calc_stdev, calc_daily_returns, train_linreg_model, predict_returns,
                      prep_data_for_model, correl_heatmap)
import io
import base64

INTERESTED_STOCKS = ["JPM", "GS", "BAC", "C"]

app = Flask(__name__, static_folder='static')


@app.route("/")
def home():
    return render_template('home.html', title='Stock Analysis',
                           header='Analyzing Major Bank Stocks',
                           )


@app.route("/20daymovingavg")
def moving_average():
    """renders 20-day moving average plot images in flask"""
    img_folder = os.path.join(os.getcwd(), "static", "moving_avg_images")
    images = []
    for img in os.listdir(img_folder):
        if img.lower().endswith('.png'):
            img_path = 'moving_avg_images/' + img
            img_path = img_path.lstrip('/')
            images.append(img_path)

    return render_template('index.html', title='Stock Analysis',
                           header='Analyzing Major Bank Stocks',
                           images=images,
                           section_title='20-Day Moving Average Price',
                           content='Presenting 20-day moving average price of JPMorgan, Goldman Sachs,'
                                   ' Citigroup, and Bank of America. Time series data for the past 20 years is pulled'
                                   ' from AlphaVantage free API. From this data,'
                                   ' python scripts calculate the 20-day moving average price from 2000 - 2024.')


@app.route("/correlation")
def correlation():
    image = "correlation_heatmap.png"
    return render_template('index.html', title='Correlation',
                           header='Correlation Analysis',
                           section_title='',
                           content='', image=image)


@app.route("/stdev")
def standard_deviation():   ### UNFINISHED HIT API LIMIT
    stock_data_dict = get_multiple_stock_df(INTERESTED_STOCKS)
    standard_dev_table = calc_stdev(stock_data_dict)

    return render_template('index.html', title='Stock Analysis',
                           header='Analyzing Major Bank Stocks',
                           section_title='Analysis Notes',
                           table=standard_dev_table,
                           content='Presenting a basic analysis of JPMorgan, Goldman Sachs,'
                                   ' Citigroup, and Bank of America. Time series data for the past 20 years is pulled'
                                   ' from AlphaVantage free API. From this data, python scripts calculate daily returns,'
                                   ' correlation, standard deviation, and model a basic linear regression.'
                                   ' The model predicts daily returns with the 20-day moving average price.')


@app.route("/linreg")
def linear_regression():
    image = "linreg_plot.png"
    return render_template('index.html', title='Linear Regression Model and Graphic',
                           header='Linear Regression of JPMorgan',
                           section_title='',
                           content='', image=image)


if __name__ == "__main__":
    app.run(debug=True)




