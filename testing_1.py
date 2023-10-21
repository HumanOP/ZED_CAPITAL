import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf


def execute_strategy(ticker_symbol, time_period, initial_investment):
    ticker_symbol+='.NS'
    try:
        data = yf.download(ticker_symbol.upper(), period=f'{int(time_period*252)}d', interval='1d')
        if data.empty:
            raise ValueError('No data available for the given time period.')

    except Exception as e:
        # You can add a logger here or print the exception for debugging purposes.
        # print(str(e))
        if ticker_symbol.endswith('.NS'):
            ticker_symbol = ticker_symbol[:-3]
        raise ValueError(f"Error fetching data for ticker symbol {ticker_symbol}.\nEnsure it's a valid stock ticker symbol.")
    
    data['Highdiff'] = data['High'].diff()
    data['Lowdiff'] = data['Low'].diff()
    data['10WeekHigh'] = data['High'].rolling(window=50, min_periods=1).max()
    data['10WeekLow'] = data['Low'].rolling(window=50, min_periods=1).min()
    data['Volume_MA'] = data['Volume'].rolling(window=5).mean()
    stop_loss_percentage = 1.4
    brokerage = 0.5

    data['Buy_Signal'] = np.where(((data['Highdiff'] > 0) & (data['Highdiff'].shift() > 0) & (data['Lowdiff'] > 0) & (data['Lowdiff'].shift() > 0)), 1, 0)
    data['Sell_Signal'] = np.where((data['Lowdiff'] < 0) & (data['Lowdiff'].shift() < 0) & (data['Highdiff'] < 0) & (data['Highdiff'].shift() < 0) | (data['Close'] <= (1 - (stop_loss_percentage / 100)) * data['Close'].shift(1)), 1, 0)

    position = 'closed'
    data['Signal'] = 0

    #initial_investment = float(input('Enter the initial investment amount: '))
    
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

    data['Sell_Signal'] = data['Sell_Signal'].shift(-1)

    data.to_csv('trade_summary.csv', index=True)

    plt.figure(figsize=(12, 6))
    plt.plot(data.index, data['Close'], label='Close Price')
    plt.plot(data[data['Signal'] > 0].index, data['Close'][data['Signal'] > 0], '^', markersize=10, color='g', label='Buy Signal')
    plt.plot(data[data['Signal'] < 0].index, data['Close'][data['Signal'] < 0], 'v', markersize=10, color='r', label='Sell Signal')
    plt.title(ticker_symbol.upper() + ' Close Price with Buy/Sell Signals')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.savefig(r"C:\Users\bhush\Desktop\CP\zed_capital\test_images\Signals.png")
    # plt.show()


    final_portfolio_value = data['Total'].iloc[-1]
    return_percentage = (final_portfolio_value - initial_investment) / initial_investment * 100

    print("Final Portfolio Value: ₹", round(final_portfolio_value, 2))
    print("Strategy Return: ", round(return_percentage, 2), "%")

    unique_trades = data[data['Signal'] != 0]
    number_of_trades = len(unique_trades)
    print("Number of Trades Executed: ", number_of_trades//2)

    # strategy_returns = data['Strategy_Return']
    # buy_hold_returns = data['Buy_Hold_Return']

    # risk_free_rate = 0.0  

    # strategy_sharpe_ratio = (strategy_returns.mean() - risk_free_rate) / strategy_returns.std()
    # buy_hold_sharpe_ratio = (buy_hold_returns.mean() - risk_free_rate) / buy_hold_returns.std()

    # print('Strategy Sharpe Ratio:', strategy_sharpe_ratio)
    # print('Buy and Hold Sharpe Ratio:', buy_hold_sharpe_ratio)

    total_turnover = data['Shares'].diff().abs().sum()
    average_daily_turnover = total_turnover / len(data)

    # print('Average Daily Turnover:', average_daily_turnover)

    # Annualized Return
    total_trading_days = len(data)
    years = time_period
    annualized_return = ((final_portfolio_value / initial_investment) ** (1 / years) - 1) * 100
    print("Annualized Return: ", round(annualized_return, 2), "%")

    # Max Drawdown
    cumulative_returns = data['Total'] / initial_investment
    # print(cumulative_returns)
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
    
    # Calculate Daily Returns
    data['Daily Returns'] = data['Close'].pct_change()

    # 1. Value at Risk (VaR) at 95% confidence level
    alpha = 0.05
    var_95 = np.percentile(data['Daily Returns'].dropna(), 100 * alpha)
    print(f'Value at Risk (95% confidence): {-var_95:.2%}')

    # 2. Risk Return Ratio
    risk_return_ratio = data['Daily Returns'].std() / data['Daily Returns'].mean()
    print(f'Risk Return Ratio: {risk_return_ratio:.2f}')

    # 3. Average Profit Per Trade
    avg_profit_per_trade = 2*(final_portfolio_value-initial_investment)/number_of_trades
    print(f'Average Profit per Trade: {avg_profit_per_trade:.2f}')


    plt.figure(figsize=(12, 6))
    plt.plot(data['Buy_Hold_Return'], label='Buy and Hold')
    plt.plot(data['Total'] / initial_investment, label='STRATEGY')
    plt.title('Performance Comparison: Strategy vs Buy and Hold')
    plt.xlabel('Date')
    plt.ylabel('Returns')
    plt.legend()
    plt.grid(True)
    plt.savefig(r"C:\Users\bhush\Desktop\CP\zed_capital\test_images\Portfolio.png")
    # plt.show()

if __name__ == "__main__":
    execute_strategy("RELIANCE",3,200000)
