# Bank Stock Analysis

## Brief Description
Python scripts make API call to get historical time series data for JPMorgan, Bank of America, Goldman Sachs,
and Citigroup for the past 20 years. The data is formatted and analyzed with Pandas and used to make visualization with
Seaborn that are rendered in Flask. For JPMorgan specifically, using scikit-learn the program entails a basic linear
regression model to predict the daily return (price change as a percentage) for the next day. 

## Features
 - Calculate metrics such as correlation, standard deviation, 20-day moving average price,
and implement a linear regression model.
 - Show the calculated metrics with data visualizations in a Flask web application
 - Provide commentary in Flask app explaining visualization and news sources cited
 - Linear regression model predicts next day's daily return using most current data


## File Structure
- 'flask_app.py' : Sets up flask routes and implements functionality of 'analysis.py' , also renders html files
- 'analysis.py' : Makes calculations and plots based on formatted data from 'data.py'
- 'data.py' : makes API calls, and formats data for 'analysis.py' functions
- 'api_limit_checking.py' : tracks API calls and updates 'api_tracker.txt' accordingly. API documentation: https://www.alphavantage.co/documentation/
- Static folder: contains correlation heatmap image, standard deviation plot image, external css file (style.css), and
contains a static linear regression plot, although this is not used in Flask, since it's made live with most recent data 
unlike the other images.
The static folder also contains a folder containing 20 day moving average plots for each stock.
- Templates folder: Consists of 2 HTML files. The home.html is rendered for the homepage and contains design elements
from Bootstrap. The index.html is rendered for every other page and contains minimal Bootstrap design.
- 'key.env': Contains the AlphaVantage API key (not included in the repository for security reasons)
- 'api_tracker.txt': Keeps track of daily API calls to respect rate limits

## Installation and Configuration
1. Clone the repository:
git clone https://github.com/chrisda28/stockanalyzer.git
cd stockanalyzer
2. Create and Activate a Virtual Environment
3. Activate the virtual environment:
- On Windows:
  ```
  venv\Scripts\activate
  ```
- On macOS and Linux:
  ```
  source venv/bin/activate
  ```

4. Install the required dependencies listed below
5. Sign up for a free AlphaVantage API key at https://www.alphavantage.co/support/#api-key
6. Create a file named `key.env` in the project root directory
7. Add your API key to the `key.env` file:
apikey = YOUR_API_KEY_HERE
8. Ensure `key.env` is listed in your `.gitignore` file to avoid exposing your API key publicly



## How to run the program
1. Complete Installation/Configuration Steps
2. Make sure you are in project directory      (cd path/to/stockanalyzer)
3. Navigate to 'flask_app.py' in project and run the program
4. Open a web browser and go to the URL displayed in the terminal or click link if displayed in console (typically http://127.0.0.1:5000/)
5. Navigate through the different pages to view the analysis
6. When finished, stop the program by pressing CTRL+C in the terminal
7. Deactivate the virtual environment

## Dependencies

This project requires the following Python libraries:
- Flask
- pandas
- requests
- matplotlib
- seaborn
- scikit-learn
- python-dotenv

You can install these manually using pip:
## Technologies Used in Program
- Flask
- Pandas
- Scikit-learn
- AlphaVantage API
- Seaborn



## AI usage and helpful documentation
- Help me implement the linear regression model https://www.geeksforgeeks.org/python-linear-regression-using-sklearn/
- Save plots as images  https://www.geeksforgeeks.org/saving-a-plot-as-an-image-in-python/
- Claude helped implement the API check decorator and function that checks API daily limit
- Format the various plots and graphics
- AI help with external styling

## Future Improvements

1. Implement more advanced machine learning models for stock price prediction
2. Expand the analysis to include more stocks and sectors
3. Implement user authentication to allow personalized watchlists
4. Add more interactive features to the visualizations, such as date range selection

## Author
Christian Asimou