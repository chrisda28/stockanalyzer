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
    """render live lin reg model in flask"""
    ticker = "JPM"
    jpm_df = get_stock_df(ticker)
    prepped_jpm_df = prep_data_for_model(jpm_df)
    model, score = train_linreg_model(prepped_jpm_df)

    latest_data = prepped_jpm_df.iloc[-1]   # getting last row which is the most recent line
    x_vars = [[latest_data['20 day moving average'], latest_data['close']]]

    predicted_return = predict_returns(model, x_vars)[0]  # Predict the daily return using the model and most recent data
# The model returns a numpy array, so we use [0] to extract the single predicted value
# This converts the prediction from an array to a simple number (scalar)

    plot_path = make_plot('20 day moving average', 'daily returns', prepped_jpm_df, f"{ticker} Linear Regression")
    # Generate a plot of the 20-day moving average vs daily returns
# The plot is saved as an image file, and the file path is returned

    latest_date = prepped_jpm_df.index[-1].strftime('%Y-%m-%d')  # getting hold of latest data
    latest_close = latest_data['close']
    latest_ma = latest_data['20 day moving average']

    return render_template('index.html', title='Linear Regression Model and Graphic',
                           header='Linear Regression of JPMorgan',
                           section_title='Live Model Results',
                           content=f"This model uses daily time series data of JPMorgan's stock. "
                                   f"Using the calculated 20-day moving average price and closing price, "
                                   f"the model predicts the stock's daily returns.\n\n"
                                   f"Model has R^2 value of: {round(score, 4)}"
                                   f"Latest data as of {latest_date}:\n"
                                   f" Closing price: ${latest_close:.2f}\n"
                                   f" 20-day moving average: ${latest_ma:.2f}\n"
                                   f"Predicted daily return: {predicted_return:.4f}",
                           image=plot_path)


if __name__ == "__main__":
    app.run(debug=True)




