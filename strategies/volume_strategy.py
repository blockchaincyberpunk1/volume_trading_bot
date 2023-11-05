import pandas as pd
import numpy as np

def volume_based_strategy(data, symbol):
    # Calculate the average volume
    average_volume = data['5. volume'].mean()

    # Initialize trading variables
    position = 0  # 0 for no position, 1 for long position
    buy_price = 0
    holding_days = 0

    # List to store trading signals
    signals = []

    for index, row in data.iterrows():
        current_volume = row['5. volume']
        close_price = row['4. close']

        if current_volume > average_volume:
            if position == 0:
                # Buy signal
                position = 1
                buy_price = close_price
                signals.append((index, 'Buy', buy_price))
        else:
            if position == 1:
                # Sell signal after holding for 5 days (you can customize this)
                holding_days += 1
                if holding_days >= 5:
                    position = 0
                    sell_price = close_price
                    signals.append((index, 'Sell', sell_price))
                    holding_days = 0

    if position == 1:
        # Close any open position at the end of the data
        signals.append((data.index[-1], 'Sell', data['4. close'][-1]))

    return pd.DataFrame(signals, columns=['Date', 'Signal', 'Price'])

# Example usage of the strategy
if __name__ == "__main__":
    historical_data = pd.read_csv("data/historical_data.csv")  # Load your historical data
    signals_df = volume_based_strategy(historical_data, symbol='AAPL')  # Replace 'AAPL' with your desired symbol
    print(signals_df)
