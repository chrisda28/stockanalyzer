import pandas as pd
from flask import Flask, render_template
from data import get_stock_df, get_multiple_stock_df
from analysis import (make_plot, calc_correlation, calc_stdev, calc_daily_returns, train_linreg_model, predict_returns,
                      prep_data_for_model, correl_heatmap)
import io
import base64

INTERESTED_STOCKS = ["JPM", "GS", "BAC", "C"]

app = Flask(__name__)


@app.route("/")
def home():
    return render_template('index.html', title='Home',
                           header='Finance Stock Analysis',
                           section_title='Section Title',
                           content='content here')

@app.route("/dailyreturns")
def function2():
    pass
    # frame_dict = get_multiple_stock_df(tickers=INTERESTED_STOCKS)
    # for ticker, frame in frame_dict.items():
    #     stock_returns = calc_daily_returns(frame)
    #     make_plot(columnx=ticker, columny=stock_returns)


@app.route("/correlation")
def get_correl_heatmap():
    frame_dict = get_multiple_stock_df(INTERESTED_STOCKS)
    heatmap = correl_heatmap(frame_dict)
    print(len(heatmap))
    return render_template('index.html', title='Correlation',
                           header='Finance Stock Analysis',
                           section_title='correlation',
                           content='content', base64_heatmap=heatmap)


@app.route("/stdev")
def function4():
    pass


if __name__ == "__main__":
    app.run(debug=True)