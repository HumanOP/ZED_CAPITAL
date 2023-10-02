import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt

# Define stocks and time period
stocks = ['WIPRO.NS', 'TATAMOTORS.NS', 'HDFCBANK.NS', 'INFY.NS']
start_date = '2022-01-01'
end_date = '2023-01-01'

# Download historical stock prices
stock_data = yf.download(stocks, start=start_date, end=end_date)['Close']

# Calculate daily returns
returns = stock_data.pct_change()

# Initialize variables for portfolio optimization
num_portfolios = 10000
results = []

for _ in range(num_portfolios):
    weights = np.random.random(len(stocks))
    weights /= np.sum(weights)

    portfolio_return = np.sum(returns.mean() * weights) * 252
    portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(returns.cov() * 252, weights)))

    results.append([portfolio_return, portfolio_volatility] + weights.tolist())
    
# Convert results to DataFrame
columns = ['Return', 'Volatility'] + stocks
results_df = pd.DataFrame(results, columns=columns)

# Set the index explicitly
results_df.set_index(['Return', 'Volatility'], inplace=True)

# Calculate mean returns
mean_returns = returns.mean()

# Calculate portfolio return
results_df['Return'] = results_df.apply(lambda row: np.sum(row[stocks] * mean_returns) * 252, axis=1)

# Calculate portfolio volatility
results_df['Volatility'] = results_df.apply(lambda row: np.sqrt(np.dot(row[stocks].T, np.dot(returns.cov() * 252, row[stocks]))), axis=1)

# Calculate Sharpe Ratio
risk_free_rate = 0.0  # You can adjust this based on your risk-free rate
results_df['Sharpe Ratio'] = (results_df['Return'] - risk_free_rate) / results_df['Volatility']

# Find the portfolio with the highest Sharpe Ratio
optimal_portfolio = results_df.loc[results_df['Sharpe Ratio'].idxmax()]

# Display optimal portfolio
print("Optimal Portfolio:")
print(optimal_portfolio)

# Calculate individual stock allocations based on the optimal portfolio weights
stock_allocations = optimal_portfolio[stocks].values

# Allocate total funds equally to each stock
total_funds = 1000000  # You can adjust this based on your initial capital
allocated_funds_per_stock = total_funds * stock_allocations

# Initialize variables for trading strategy
buy_condition = (
    (stock_data[stocks].shift(1) < stock_data[stocks].shift(2)) &
    (stock_data[stocks].shift(2) < stock_data[stocks].shift(3)) &
    (stock_data[stocks].shift(4) < stock_data[stocks].shift(5)) &
    (stock_data[stocks].shift(3) < stock_data[stocks].shift(4)) &
    (stock_data[stocks].shift(5) < stock_data[stocks].shift(6)) &
    (stock_data[stocks] > stock_data[stocks].shift(1))
)

sell_condition = stock_data[stocks] < stock_data[stocks].shift(1)

# Initialize variables for tracking trades
trades = pd.DataFrame(index=stock_data.index, columns=stocks, data=0)

# Execute the trading strategy for each stock
for i, stock in enumerate(stocks):
    funds = allocated_funds_per_stock[i]
    position = 0  # 0 indicates no position, 1 indicates long, -1 indicates short

    for j in range(1, len(stock_data)):
        if buy_condition[stock].iloc[j] and position == 0:
            # Buy signal
            trades[stock].iloc[j] = funds / stock_data[stock].iloc[j]
            position = 1
        elif sell_condition[stock].iloc[j] and position == 1:
            # Sell signal
            trades[stock].iloc[j] = -funds
            position = 0


# Calculate the cumulative returns of the portfolio
portfolio_returns = np.sum(trades * returns[stocks], axis=1)
cumulative_returns = (1 + portfolio_returns).cumprod()

# Visualize the portfolio performance
plt.figure(figsize=(10, 6))
plt.plot(cumulative_returns, label='Portfolio')
plt.title('Portfolio Performance')
plt.xlabel('Date')
plt.ylabel('Cumulative Return')
plt.legend()
plt.show()
