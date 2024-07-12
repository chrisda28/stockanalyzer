import pandas as pd
from flask import Flask

INTERESTED_STOCKS = ["JPM", "GS", "BAC", "C"]

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"







if __name__ == "__main__":
    app.run(debug=True)