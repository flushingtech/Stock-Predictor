import requests
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression
import numpy as np
from sklearn.preprocessing import MinMaxScaler

# Replace 'YOUR_API_KEY' with your actual Alpha Vantage API key
API_KEY = 'BM7ED9BQP1D8AFP3'
symbol = input('Enter stock symbol: ')

# Endpoint for getting real-time stock quote
realtime_url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={API_KEY}'

# Send GET request to the real-time data API
realtime_response = requests.get(realtime_url)

# Parse real-time JSON response
realtime_data = realtime_response.json()

# Extract relevant real-time information
if 'Global Quote' in realtime_data:
    realtime_stock_data = realtime_data['Global Quote']
    realtime_symbol = realtime_stock_data['01. symbol']
    realtime_price = realtime_stock_data['05. price']
    realtime_change_percent = realtime_stock_data['10. change percent']
    
    print(f'Real-time Data:')
    print(f'Stock Symbol: {realtime_symbol}')
    print(f'Price: {realtime_price}')
    print(f'Change Percent: {realtime_change_percent}')
else:
    print('Error: Unable to fetch real-time stock data')

# Get date for 7 days ago
end_date = datetime.now().strftime('%Y-%m-%d')
start_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')

# Endpoint for getting historical stock data
historical_url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_KEY}'

# Send GET request to the historical data API
historical_response = requests.get(historical_url)

# Parse historical JSON response
historical_data = historical_response.json()

# Extract relevant historical information
if 'Time Series (Daily)' in historical_data:
    historical_stock_data = historical_data['Time Series (Daily)']
    print(f'\nHistorical Data (1 week):')
    dates = []
    prices = []
    for date in historical_stock_data.keys():
        if date >= start_date and date <= end_date:
            stock_info = historical_stock_data[date]
            dates.append(date)
            prices.append(float(stock_info["4. close"]))
            print(f'Date: {date}')
            print(f'Open: {stock_info["1. open"]}')
            print(f'High: {stock_info["2. high"]}')
            print(f'Low: {stock_info["3. low"]}')
            print(f'Close: {stock_info["4. close"]}')
            print(f'Volume: {stock_info["5. volume"]}')
            print()

    # Perform linear regression
    if len(prices) >= 2:
        X = np.arange(len(prices)).reshape(-1, 1)
        y = prices

        # Create and fit the model
        model = LinearRegression()
        model.fit(X, y)

        # Predict the next day's closing price
        next_day = np.array([[len(prices)]])
        predicted_price = model.predict(next_day.reshape(-1, 1))

        # Print the predicted price
        print(f'Predicted closing price for the next day: ${predicted_price[0]:.2f}')

    else:
        print("Error: Not enough historical data available to make predictions.")
else:
    print('Error: Unable to fetch historical stock data')
