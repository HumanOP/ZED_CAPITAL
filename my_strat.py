# stock_trading_system.py

import yfinance as yf
import pandas as pd
import numpy as np
import datetime

def get_stock_data(tickers, start_date, end_date):
    """
    Retrieve historical stock data for the given tickers and date range.

    Parameters:
    - tickers (list): List of stock tickers.
    - start_date (str): Start date in the format 'YYYY-MM-DD'.
    - end_date (str): End date in the format 'YYYY-MM-DD'.

    Returns:
    - pandas.DataFrame: DataFrame with historical stock data.
    """
    data = yf.download(tickers, start=start_date, end=end_date)
    return data['Adj Close']  # We're using adjusted closing prices for simplicity



def portfolio_optimization(returns):
    """
    Perform portfolio optimization using the Markowitz model.

    Parameters:
    - returns (pandas.DataFrame): DataFrame with historical stock returns.

    Returns:
    - dict: Optimal allocation of funds to each stock.
    """
    cov_matrix = returns.cov()
    num_assets = len(returns.columns)

    weights = np.random.random(num_assets)
    weights /= np.sum(weights)

    expected_portfolio_return = np.sum(returns.mean() * weights) * 252  # 252 trading days in a year
    expected_portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix * 252, weights)))

    return {
        'weights': weights,
        'expected_return': expected_portfolio_return,
        'expected_volatility': expected_portfolio_volatility,
    }

def buy_stocks(strategy, portfolio_allocation, current_prices, short_window, long_window):
    """
    Execute the buying strategy to determine which stocks to buy and in what quantity.

    Parameters:
    - strategy (str): The buying strategy to use (e.g., 'moving_average').
    - portfolio_allocation (dict): Optimal allocation of funds to each stock.
    - current_prices (pandas.Series): Current stock prices.
    - short_window (int): Short moving average window size.
    - long_window (int): Long moving average window size.

    Returns:
    - dict: Buy decisions for each stock (stocks as keys and quantities as values).
    """
    if strategy == 'moving_average':
        # Simple moving average strategy (example)
        signals = pd.DataFrame(index=current_prices.index)
        signals['short_mavg'] = current_prices.rolling(window=short_window, min_periods=1, center=False).mean()
        signals['long_mavg'] = current_prices.rolling(window=long_window, min_periods=1, center=False).mean()

        # Create a new 'signal' column based on the moving average conditions
        signals['signal'] = np.where(signals['short_mavg'] > signals['long_mavg'], 1.0, 0.0)

        # Shift the 'signal' column to represent positions for the next day
        signals['positions'] = signals['signal'].shift(1)

        # Extract buy decision indices
        buy_decisions_indices = signals.index[signals['positions'] == 1].tolist()

        # Return a dictionary with stocks as keys and quantities as values
        stocks_to_buy = {stock: 1 for stock in buy_decisions_indices}
        return stocks_to_buy
    else:
        raise ValueError(f"Unknown strategy: {strategy}")


def sell_stocks(strategy, current_positions, current_prices):
    """
    Execute the selling strategy to determine when and which stocks to sell.

    Parameters:
    - strategy (str): The selling strategy to use (e.g., 'moving_average').
    - current_positions (dict): Current positions in the portfolio.
    - current_prices (pandas.Series): Current stock prices.

    Returns:
    - dict: Sell decisions for each stock.
    """
    if strategy == 'moving_average':
        # Simple moving average strategy (example)
        signals = pd.DataFrame(index=current_prices.index)
        short_window = 40
        long_window = 100

        signals['short_mavg'] = current_prices.rolling(window=short_window, min_periods=1, center=False).mean()
        signals['long_mavg'] = current_prices.rolling(window=long_window, min_periods=1, center=False).mean()

        # Make a copy of the DataFrame explicitly
        signals['signal'] = pd.Series(0, index=signals.index)
        signals.loc[signals.index[short_window:], 'signal'] = np.where(signals['short_mavg'].loc[signals.index[short_window:]] < signals['long_mavg'].loc[signals.index[short_window:]], -1.0, 0.0)
        signals['positions'] = signals['signal'].diff()

        sell_decisions = signals[signals['positions'] == -1].index
        return {'sell_decisions': sell_decisions}
    else:
        raise ValueError(f"Unknown strategy: {strategy}")




def update_positions(buy_decisions, sell_decisions, current_positions):
    """
    Update current positions based on buy and sell decisions.

    Parameters:
    - buy_decisions (dict): Buy decisions for each stock.
    - sell_decisions (dict): Sell decisions for each stock.
    - current_positions (dict): Current positions in the portfolio.

    Returns:
    - dict: Updated positions after executing buy and sell decisions.
    """
    updated_positions = current_positions.copy()

    # Execute buy decisions
    for stock, quantity in buy_decisions.items():
        updated_positions[stock] = updated_positions.get(stock, 0) + quantity

    # Execute sell decisions
    for stock, quantity in sell_decisions.items():
        if updated_positions.get(stock, 0) > 0:
              updated_positions[stock] = max(updated_positions[stock] - quantity, 0)

    return updated_positions

def apply_risk_management(current_positions, current_prices, risk_limit):
    """
    Apply risk management to the current positions based on the risk limit.

    Parameters:
    - current_positions (dict): Current positions in the portfolio.
    - current_prices (pandas.Series): Current stock prices.
    - risk_limit (float): Maximum allowed loss as a percentage of the portfolio value.

    Returns:
    - dict: Adjusted positions after applying risk management.
    """
    updated_positions = current_positions.copy()

    for stock, quantity in current_positions.items():
        if stock in current_prices.index:
            stock_price = current_prices[stock]
            current_value = quantity * stock_price

            # Check if the current value exceeds the risk limit
            if current_value > risk_limit:
                max_allowed_loss = current_value * (risk_limit / 100)
                quantity_to_sell = min(quantity, int(max_allowed_loss / stock_price))

                # Update the positions
                updated_positions[stock] = max(quantity - quantity_to_sell, 0)

    return updated_positions


def optimize_strategy_parameters(strategy, returns, population_size=10, generations=5):
    """
    Optimize trading strategy parameters using a genetic algorithm.

    Parameters:
    - strategy (str): The trading strategy to optimize.
    - returns (pandas.DataFrame): DataFrame with historical stock returns.
    - population_size (int): Number of individuals in the population.
    - generations (int): Number of generations in the genetic algorithm.

    Returns:
    - dict: Optimized strategy parameters.
    """
    # Define the parameter space for optimization
    if strategy == 'moving_average':
        param_space = {'short_window': range(10, 50), 'long_window': range(50, 200)}
    else:
        raise ValueError(f"Unknown strategy: {strategy}")

    # Generate an initial population
    population = [{'short_window': np.random.choice(param_space['short_window']),
                   'long_window': np.random.choice(param_space['long_window'])}
                  for _ in range(population_size)]

    for generation in range(generations):
        # Evaluate the fitness of each individual in the population
        fitness_scores = []
        for individual in population:
            # Apply the strategy with current parameters and calculate fitness
            # (e.g., total returns over the backtesting period)
            fitness = evaluate_strategy(individual, returns)
            fitness_scores.append((individual, fitness))

        # Select the top-performing individuals
        top_individuals = sorted(fitness_scores, key=lambda x: x[1], reverse=True)[:int(population_size / 2)]

        # Generate a new population through crossover and mutation
        new_population = []
        for _ in range(population_size):
            parent1, parent2 = np.random.choice(top_individuals, size=2, replace=False)
            crossover_point = np.random.choice(list(param_space.keys()))
            child = {param: parent1[0][param] if np.random.rand() < 0.5 else parent2[0][param]
                    for param in param_space.keys()}
            child[crossover_point] = np.random.choice(param_space[crossover_point])
            new_population.append(child)

        population = new_population

    # Return the parameters of the best-performing individual
    best_params = sorted(fitness_scores, key=lambda x: x[1], reverse=True)[0][0]
    return best_params

def evaluate_strategy(params, returns):
    """
    Evaluate the performance of a trading strategy with given parameters.

    Parameters:
    - params (dict): Strategy parameters.
    - returns (pandas.DataFrame): DataFrame with historical stock returns.

    Returns:
    - float: Fitness score representing the performance of the strategy.
    """
    if params['strategy'] == 'moving_average':
        signals = pd.Series(0, index=returns.index)
        signals['short_mavg'] = returns.rolling(window=params['short_window'], min_periods=1, center=False).mean()
        signals['long_mavg'] = returns.rolling(window=params['long_window'], min_periods=1, center=False).mean()
        signals['signal'] = 0.0
        signals['signal'] = pd.Series(signals['signal'])
        
        signals['signal'][params['short_window']:] = np.where(signals['short_mavg'][params['short_window']:] > signals['long_mavg'][params['short_window']:], 1.0, 0.0)
        signals['positions'] = signals['signal'].diff()

        # Calculate a fitness score based on the strategy's performance
        total_returns = (returns * signals['positions'].shift(1)).sum()
        return total_returns

    else:
        raise ValueError(f"Unknown strategy: {params['strategy']}")

def backtest_trading_system(strategy, params, returns, initial_capital=100000):
    """
    Backtest the trading system using historical returns.

    Parameters:
    - strategy (str): The trading strategy to backtest.
    - params (dict): Strategy parameters.
    - returns (pandas.DataFrame): DataFrame with historical stock returns.
    - initial_capital (float): Initial capital for the portfolio.

    Returns:
    - pandas.DataFrame: DataFrame with portfolio performance over time.
    """
    if strategy == 'moving_average':
        signals = pd.Series(0, index=returns.index)
        signals['short_mavg'] = returns.rolling(window=params['short_window'], min_periods=1, center=False).mean()
        signals['long_mavg'] = returns.rolling(window=params['long_window'], min_periods=1, center=False).mean()
        signals['signal'] = pd.Series(0, index=returns.index)


        # Add print statements
        print("Length of returns:", len(returns))
        print("Length of signals['signal']:", len(signals['signal']))
        print("Length of signals['short_mavg'][params['short_window']:] before assignment:", len(signals['short_mavg'][params['short_window']:]))

        # Update the 'signal' column using the mask
        condition_mask = signals['short_mavg'][params['short_window']:] > signals['long_mavg'][params['short_window']:]
        signals['signal'][params['short_window']:] = np.where(condition_mask.iloc[:, 0].values, 1.0, 0.0)

        # Add another print statement after assignment
        print("Length of signals['signal'][params['short_window']:] after assignment:", len(signals['signal'][params['short_window']:]))

        signals['positions'] = signals['signal'].diff()

        # Initialize portfolio with initial capital
        portfolio = pd.DataFrame(index=returns.index)
        portfolio['positions'] = signals['positions']
        portfolio['stock_holding'] = portfolio['positions'].diff().cumsum()
        portfolio['cash'] = initial_capital - (signals['positions'].diff() * returns.shift(-1)).cumsum().iloc[:, 0]

        # Calculate total portfolio value over time
        portfolio['total_value'] = portfolio['cash'] + (portfolio['stock_holding'] * returns)

        return portfolio

    else:
        raise ValueError(f"Unknown strategy: {strategy}")

# ... (rest of the code remains unchanged)



def calculate_performance_metrics(portfolio):
    """
    Calculate portfolio performance metrics.

    Parameters:
    - portfolio (pandas.DataFrame): DataFrame with portfolio performance over time.

    Returns:
    - dict: Performance metrics including total returns, annualized returns, and Sharpe ratio.
    """
    total_returns = (portfolio['total_value'][-1] / portfolio['total_value'][0]) - 1

    # Calculate annualized returns
    trading_days_per_year = 252
    years = len(portfolio) / trading_days_per_year
    annualized_returns = (1 + total_returns) ** (1 / years) - 1

    # Calculate daily returns
    daily_returns = portfolio['total_value'].pct_change()

    # Calculate Sharpe ratio
    sharpe_ratio = (daily_returns.mean() / daily_returns.std()) * np.sqrt(trading_days_per_year)

    return {
        'total_returns': total_returns,
        'annualized_returns': annualized_returns,
        'sharpe_ratio': sharpe_ratio,
    }


if __name__ == "__man__":
    tickers = ['AAPL', 'MSFT', 'GOOGL']
    start_date = '2022-01-01'
    end_date = '2023-01-01'

    stock_data = get_stock_data(tickers, start_date, end_date)
    print(stock_data.head())
    
    portfolio_returns = stock_data.pct_change().dropna()
    optimization_result = portfolio_optimization(portfolio_returns)
    print("Optimal Weights:", optimization_result['weights'])
    print("Expected Portfolio Return:", optimization_result['expected_return'])
    print("Expected Portfolio Volatility:", optimization_result['expected_volatility'])

    buying_strategy = 'moving_average'
    current_prices = stock_data.iloc[-1]  # Use the latest available prices
    buy_decisions = buy_stocks(buying_strategy, optimization_result, current_prices)
    print("Buy Decisions:", buy_decisions)

    buying_strategy = 'moving_average'
    selling_strategy = 'moving_average'
    current_prices = stock_data.iloc[-1]  # Use the latest available prices

    short_window = 20
    long_window = 50
    buy_decisions = buy_stocks(buying_strategy, optimization_result, current_prices, short_window, long_window)
    current_positions = update_positions(buy_decisions, {}, {})
    print("Buy Decisions:", buy_decisions)
    print("Updated Positions:", current_positions)

    sell_decisions = sell_stocks(selling_strategy, current_positions, current_prices)
    current_positions = update_positions({}, sell_decisions, current_positions)
    print("Sell Decisions:", sell_decisions)
    print("Updated Positions:", current_positions)

    risk_limit = 0.02
    adjusted_positions = apply_risk_management(current_positions, current_prices, risk_limit)
    print("Adjusted Positions with Risk Management:", adjusted_positions)

    optimization_strategy = 'moving_average'
    optimized_params = optimize_strategy_parameters(optimization_strategy, portfolio_returns)
    print("Optimized Strategy Parameters:", optimized_params)
    
    backtest_strategy = 'moving_average'
    backtest_params = {'short_window': 20, 'long_window': 50}  # Example parameters
    backtest_portfolio = backtest_trading_system(backtest_strategy, backtest_params, portfolio_returns)
    print(backtest_portfolio.tail())
    
    performance_metrics = calculate_performance_metrics(backtest_portfolio)
    print("Performance Metrics:", performance_metrics)


if __name__ == "__main__":
    tickers = ['AAPL', 'MSFT', 'GOOGL']
    start_date = '2022-01-01'
    end_date = '2023-01-01'

    # Step 1: Retrieve historical stock data
    stock_data = get_stock_data(tickers, start_date, end_date)

    # Step 2: Portfolio Optimization
    portfolio_returns = stock_data.pct_change().dropna()
    optimization_result = portfolio_optimization(portfolio_returns)

    # Step 3: Buying/Entering
    buying_strategy = 'moving_average'
    current_prices = stock_data.iloc[-1]
    short_window = 20
    long_window = 50
    buy_decisions = buy_stocks(buying_strategy, optimization_result, current_prices, short_window, long_window)
    # Step 4: Selling/Exiting
    selling_strategy = 'moving_average'
    current_positions = update_positions(buy_decisions, {}, {})
    sell_decisions = sell_stocks(selling_strategy, current_positions, current_prices)

    # Step 5: Risk Management
    risk_limit = 0.02
    current_positions = update_positions(buy_decisions, sell_decisions, current_positions)
    adjusted_positions = apply_risk_management(current_positions, current_prices, risk_limit)

    # Step 6: Backtesting
    backtest_strategy = 'moving_average'
    backtest_params = {'short_window': 20, 'long_window': 50}
    backtest_portfolio = backtest_trading_system(backtest_strategy, backtest_params, portfolio_returns)

    # Step 7: Performance Metrics
    performance_metrics = calculate_performance_metrics(backtest_portfolio)

    # Print results
    print("Optimal Weights:", optimization_result['weights'])
    print("Buy Decisions:", buy_decisions)
    print("Sell Decisions:", sell_decisions)
    print("Adjusted Positions with Risk Management:", adjusted_positions)
    print("Performance Metrics:", performance_metrics)
