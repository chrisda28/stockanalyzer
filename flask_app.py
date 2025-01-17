from flask import Flask, render_template, url_for
from data import get_stock_df, get_multiple_stock_df
from analysis import (make_plot, train_linreg_model, predict_returns,
                      prep_data_for_model,)
import os
import os.path
import pandas as pd
import matplotlib
matplotlib.use('Agg')   # this allows matplotlib to use different backend
# that doesn't require GUI. Resolved threading issues

os.environ['OPENBLAS_NUM_THREADS'] = '1'   # numpy and scikit-lear use OpenBLAS for math operations,
# so limiting this to 1 thread will help it not interfere with flask


INTERESTED_STOCKS = ["JPM", "GS", "BAC", "C"]

app = Flask(__name__, static_folder='static')   # create an instance of flask application


@app.route("/")
def home():
    """render the home page"""
    return render_template(template_name_or_list='home.html', title='Stock Analysis',
                           header='',)


@app.route("/20daymovingavg")
def moving_average():
    """renders 20-day moving average plot images in flask"""
    img_folder = os.path.join(os.getcwd(), "static", "moving_avg_images")  # define path to img folder where plots are
    images = []
    for img in os.listdir(img_folder):  # appending img pathways to a list
        if img.lower().endswith('.png'):
            img_path = 'moving_avg_images/' + img  # construct relative file path to image (plot)
            img_path = img_path.lstrip('/')  # remove leading slash to ensure it's a relative file path
            images.append(img_path)

    return render_template(template_name_or_list='index.html', title='Stock Analysis',
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
    """render correlation heatmap and commentary"""
    image = "correlation_heatmap.png"
    sources = ['https://www.emarketer.com/content/citibank-shores-up-core-offerings-plan-shrink-mexico-footprint',
               'https://www.citigroup.com/global/news/perspective/2023/our-strategy-to-simplify-lessons-from-'
               'our-divestiture-journey-titi-cole']
    return render_template('index.html', title='Correlation',
                           header='Correlation Analysis',
                           section_title='Correlation',
                           sources=sources,
                           content="Citigroup's lower correlation to other three banks is caused by a shift in focus. "
                                   "Citigroup has shifted away from personal banking services "
                                   "in Mexico and is focusing "
                                   "more on U.S. personal banking services."
                                   " In 2021, Citi revealed intentions to exit 13"
                                   " markets across Asia and Europe - instead focusing on other higher-returning "
                                   "businesses. This shift from international markets may explain stark differences in"
                                   " Citigroup's correlation with the other three banks who maintain their "
                                   "international presence. View sources below.", image=image)


@app.route("/stdev")
def standard_deviation():
    """render barplot for standard deviation of daily returns for each stock"""
    image = "stdev_plot.png"
    sources = ['https://www.forbes.com/sites/johnbuckingham/2024/04/17/volatility-price-of-successful-equity-'
               'investing--liking-citigroup/', 'https://internationalbanker.com/banking/major-restructuring-seeks-to-'
                                               'restore-citigroups-competitiveness-among-us-banking-elite/']
    return render_template('index.html', title='Stock Analysis',
                           header='Analyzing Major Bank Stocks',
                           section_title='Standard Deviation of Daily Returns',
                           image=image,
                           sources=sources,
                           content="Citigroup's volatility is largely from restructuring efforts resulting in"
                                   " strategic shifts and cost-cutting measures. These efforts introduce short-term un"
                                   "certainty. Pair this with unfavorable"
                                   " past financial performance and this will explain"
                                   " the disparity between Citigroup and the other three banks' volatility. "
                                   "View news sources below.")


@app.route("/linreg")
def linear_regression():
    """render live linear regression model in flask"""
    ticker = "JPM"
    jpm_df = get_stock_df(ticker)   # get historical stock data (Daily Time Series data)
    prepped_jpm_df = prep_data_for_model(jpm_df)
    model, score = train_linreg_model(prepped_jpm_df)
    score = round(score, 4)   # formatting the r^2 value
    latest_data = prepped_jpm_df.iloc[-1]   # getting last row which is the most recent line
    x_vars = pd.DataFrame({   # getting hold of just the most recent data for interested columns
        '20 day moving average': [latest_data['20 day moving average']],
        'close': [latest_data['close']]
    })

    predicted_return = predict_returns(model, x_vars)[0]
    predicted_return = round(predicted_return, 4)  # Predict the daily return using the model and most recent data
# The model returns a numpy array, so we use [0] to extract the single predicted value
# This converts the prediction from an array to a simple number (scalar)

    plot_path = make_plot(columnx='20 day moving average', columny='daily returns',
                          prepped_data=prepped_jpm_df, title="{ticker} Linear Regression")
    # Generate a plot of the 20-day moving average vs daily returns
# The plot is saved as an image file, and the file path is returned

    latest_date = prepped_jpm_df.index[-1].strftime('%Y-%m-%d')  # getting hold of latest data to render in flask
    latest_close = latest_data['close']  # getting hold of latest data to render in flask
    latest_ma = latest_data['20 day moving average']  # getting hold of latest data to render in flask

    return render_template('index.html', title='Linear Regression Model and Graphic',
                           header='Linear Regression of JPMorgan',
                           section_title='Live Model Results',
                           score=score,
                           last_date=latest_date,
                           last_ma=latest_ma,
                           latest_close=latest_close,
                           predicted_return=predicted_return,
                           content=f"This model uses JPMorgan's historical calculated 20-day moving average price and"
                                   f" closing price to learn patterns and make predictions of daily returns."
                                   f" The predicted return is the model's estimate of the next day's price"
                                   f" change as a percentage. The R^2 value ranges from 0 to 1 and explains how"
                                   f" well the model explains the variability of the data. "
                                   f"While the R^2 of this model is low,"
                                   f" it provides a great platform for which to improve upon. ",
                           image=plot_path)


if __name__ == "__main__":
    app.run(debug=True)




