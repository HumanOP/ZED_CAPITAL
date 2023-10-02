import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
import pandas as pd

ticker_symbol = input('Enter the ticker symbol of the stock to implement the strategy on: ') + '.NS'
time_period = float(input('Enter the time period (in years) to be analyzed: '))

data = yf.download(ticker_symbol, period=f'{int(time_period*252)}d', interval='1d')

if data.empty:
    print('Error in Ticker Symbol')
    raise SystemExit(0)

data['EMA12'] = data['Close'].ewm(span=12).mean()
data['EMA26'] = data['Close'].ewm(span=26).mean()
data['EMA40'] = data['Close'].ewm(span=40).mean()
data['C'] = (data['Close'] + data['High'] + data['Low'])/3
data['Volume_MA'] = data['Volume'].rolling(window=5).mean()
data['Highdiff'] = data['High'].diff()
data['Lowdiff'] = data['Low'].diff()
data['10WeekHigh'] = data['High'].rolling(window=50, min_periods=1).max()
data['10WeekLow'] = data['Low'].rolling(window=50, min_periods=1).min()
stop_loss_percentage = 1.4
brokerage = 0.0

data['Sell_Signal'] = np.where((data['Close'] >= ((2 * data['C'].shift()) - data['Low'].shift())), 1, 0)
data['Buy_Signal'] = np.where(((data['Close'] > data['C'].shift()) & (data['Sell_Signal'] == 0)), 1, 0)


position = 'closed'
data['Signal'] = 0

initial_investment = float(input('Enter the initial investment amount: '))

data['Cash'] = initial_investment
data['Holdings'] = 0

num_stocks = 0 
data['Shares'] = 0

data['Buy_Hold_Return'] = data['Close'] / data['Close'].iloc[0]

for i in range(1, len(data)):
    if data['Buy_Signal'].iloc[i] != 1 and position == 'closed':
        data.loc[data.index[i], 'Cash'] = data['Cash'].iloc[i - 1]
    elif data['Buy_Signal'].iloc[i] == 1 and position == 'closed':
        data.loc[data.index[i], 'Cash'] = data['Cash'].iloc[i - 1]
        position = 'open'
        available_cash = data['Cash'].iloc[i]
        stock_price = data['Close'].iloc[i]
        num_stocks = int(available_cash / stock_price)
        if num_stocks > 0:
            data.loc[data.index[i], 'Signal'] = num_stocks
            invested_cash = num_stocks * stock_price
            data.loc[data.index[i], 'Holdings'] = invested_cash
            data.loc[data.index[i], 'Cash'] -= invested_cash
            data.loc[data.index[i], 'Shares'] = num_stocks  
    elif data['Sell_Signal'].iloc[i] == 1 and position == 'open':
        position = 'closed'
        data.loc[data.index[i], 'Signal'] = -num_stocks
        data.loc[data.index[i], 'Cash'] = (num_stocks * data['Close'].iloc[i-1])*(1-brokerage/100) + data['Cash'].iloc[i - 1]
        data.loc[data.index[i], 'Holdings'] = 0
        data.loc[data.index[i], 'Shares'] = 0 
        num_stocks = 0
    else:
        if position == 'open':
            data.loc[data.index[i], 'Holdings'] = num_stocks * data['Close'].iloc[i]
            data.loc[data.index[i], 'Cash'] = data['Cash'].iloc[i - 1]
            data.loc[data.index[i], 'Shares'] = num_stocks  
        
        data.loc[data.index[i], 'Buy_Hold_Return'] = data['Buy_Hold_Return'].iloc[i - 1] * (data['Close'].iloc[i] / data['Close'].iloc[i - 1])


data['Total'] = data['Cash'] + data['Holdings']

data['Strategy_Return'] = data['Total'].pct_change()
data['Strategy_Return'] = data['Strategy_Return'].fillna(0)

data.to_csv('trade_summary.csv', index=True)

plt.figure(figsize=(12, 6))
plt.plot(data.index, data['Close'], label='Close Price')
plt.plot(data[data['Signal'] > 0].index, data['Close'][data['Signal'] > 0], '^', markersize=10, color='g', label='Buy Signal')
plt.plot(data[data['Signal'] < 0].index, data['Close'][data['Signal'] < 0], 'v', markersize=10, color='r', label='Sell Signal')
plt.title(ticker_symbol.upper() + ' Close Price with Buy/Sell Signals')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()
plt.show()

final_portfolio_value = data['Total'].iloc[-1]
return_percentage = (final_portfolio_value - initial_investment) / initial_investment * 100

print("Final Portfolio Value: ₹", round(final_portfolio_value, 2))
print("Strategy Return: ", round(return_percentage, 2), "%")

unique_trades = data[data['Signal'] != 0]
number_of_trades = len(unique_trades)
print("Number of Trades Executed: ", number_of_trades//2)

strategy_returns = data['Strategy_Return']
buy_hold_returns = data['Buy_Hold_Return']

risk_free_rate = 0.0  

strategy_sharpe_ratio = (strategy_returns.mean() - risk_free_rate) / strategy_returns.std()
buy_hold_sharpe_ratio = (buy_hold_returns.mean() - risk_free_rate) / buy_hold_returns.std()

print('Strategy Sharpe Ratio:', strategy_sharpe_ratio)
print('Buy and Hold Sharpe Ratio:', buy_hold_sharpe_ratio)

total_turnover = data['Shares'].diff().abs().sum()
average_daily_turnover = total_turnover / len(data)

print('Average Daily Turnover:', average_daily_turnover)

# Annualized Return
total_trading_days = len(data)
years = time_period
annualized_return = ((final_portfolio_value / initial_investment) ** (1 / years) - 1) * 100
print("Annualized Return: ", round(annualized_return, 2), "%")

# Max Drawdown
cumulative_returns = data['Total'] / initial_investment
print(cumulative_returns)
peak = cumulative_returns.cummax()
drawdown = (cumulative_returns - peak) / peak
max_drawdown = drawdown.min() * 100
print("Max Drawdown: ", round(max_drawdown, 2), "%")

# Profit-making Trades
profit_trades = unique_trades[unique_trades['Total'] > unique_trades['Total'].shift()]
num_profit_trades = len(profit_trades)
print("Number of Profit-making Trades: ", num_profit_trades)

# Loss-making Trades
loss_trades = unique_trades[unique_trades['Total'] < unique_trades['Total'].shift()]
num_loss_trades = len(loss_trades)
print("Number of Loss-making Trades: ", num_loss_trades)

#print('WinLoss Ratio: ',round(profit_trades/loss_trades,2))

# Risk-Return Ratio
risk_return_ratio = (annualized_return) / max_drawdown
print("Risk-Return Ratio: ", round(risk_return_ratio, 2))

plt.figure(figsize=(12, 6))
plt.plot(data['Buy_Hold_Return'], label='Buy and Hold')
plt.plot(data['Total'] / initial_investment, label='STRATEGY')
plt.title('Performance Comparison: Strategy vs Buy and Hold')
plt.xlabel('Date')
plt.ylabel('Returns')
plt.legend()
plt.grid(True)
plt.show()