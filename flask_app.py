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
                           header='',
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
                                   ' python scripts use the Pandas library '
                                   ' to calculate the 20-day moving average price from 2000 - 2024. Visualizations are'
                                   ' created with Seaborn and Matplotlib, then saved as images and rendered.')


@app.route("/correlation")
def correlation():
    """render correlation heatmap"""
    image = "correlation_heatmap.png"
    sources = ['https://www.emarketer.com/content/citibank-shores-up-core-offerings-plan-shrink-mexico-footprint',
               'https://www.citigroup.com/global/news/perspective/2023/our-strategy-to-simplify-lessons-from-'
               'our-divestiture-journey-titi-cole']
    return render_template('index.html', title='Correlation',
                           header='Correlation Analysis',
                           section_title='Correlation',
                           sources=sources,
                           content="Citigroup's lower correlation to other three banks is caused by a shift in focus. "
                                   "Citigroup has shifted away from personal banking services in Mexico and focusing "
                                   "more on U.S. personal banking services."
                                   " In 2021, Citi revealed intentions to exit 13"
                                   " markets across Asia and Europe - instead focusing on other higher-returning "
                                   "businesses. This shift from international markets may explain stark differences in"
                                   " Citigroup's correlation with the other three banks who maintain their "
                                   "international presence. View sources below.", image=image)


@app.route("/stdev")
def standard_deviation():
    """render barplot for stdev of daily returns for each stock"""
    image = "stdev_plot.png"
    sources = ['https://www.forbes.com/sites/johnbuckingham/2024/04/17/volatility-price-of-successful-equity-'
               'investing--liking-citigroup/', 'https://internationalbanker.com/banking/major-restructuring-seeks-to-'
                                               'restore-citigroups-competitiveness-among-us-banking-elite/' ]
    return render_template('index.html', title='Stock Analysis',
                           header='Analyzing Major Bank Stocks',
                           section_title='Standard Deviation of Daily Returns',
                           image=image,
                           sources=sources,
                           content="Insights\n Citigroup's volatility is largely from restructuring efforts resulting in"
                                   " strategic shifts and cost-cutting measures. These efforts introduce short-term un"
                                   "certainty. Pair this with unfavorable past financial performance and this will explain"
                                   " the disparity between Citigroup and the other three banks' volatility. "
                                   "View news sources below.")


@app.route("/linreg")
def linear_regression():
    image = "linreg_plot.png"
    return render_template('index.html', title='Linear Regression Model and Graphic',
                           header='Linear Regression of JPMorgan',
                           section_title='',
                           content='', image=image)


if __name__ == "__main__":
    app.run(debug=True)




