import numpy as np
import random
import logging
import os
import oandapyV20
import oandapyV20.endpoints.orders as orders
import cbpro

# Configure Logging
logging.basicConfig(
    filename="trading.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class APIManager:
    """Handles API authentication and trade execution for OANDA and Coinbase."""
    
    def __init__(self):
        self.oanda_client = self._initialize_oanda_client()
        self.coinbase_client = self._initialize_coinbase_client()

    def _initialize_oanda_client(self):
        """Initialize OANDA API Client if credentials exist."""
        access_token = os.getenv("OANDA_ACCESS_TOKEN")
        return oandapyV20.API(access_token=access_token) if access_token else None

    def _initialize_coinbase_client(self):
        """Initialize Coinbase API Client if credentials exist."""
        api_key = os.getenv("COINBASE_API_KEY")
        api_secret = os.getenv("COINBASE_API_SECRET")
        api_passphrase = os.getenv("COINBASE_API_PASSPHRASE")
        return cbpro.AuthenticatedClient(api_key, api_secret, api_passphrase) if api_key and api_secret and api_passphrase else None

    def execute_trade(self, symbol, signal, platform):
        """Executes trade on the chosen platform based on evolved strategy."""
        try:
            if platform == "oanda" and self.oanda_client:
                order_data = {
                    "order": {
                        "instrument": symbol,
                        "units": 100 if signal == 1 else -100,
                        "type": "MARKET"
                    }
                }
                self.oanda_client.request(orders.OrderCreate(os.getenv("OANDA_ACCOUNT_ID"), data=order_data))
                logging.info(f"OANDA: Executed {('BUY' if signal == 1 else 'SELL')} order for {symbol}")

            elif platform == "coinbase" and self.coinbase_client:
                self.coinbase_client.place_market_order(
                    product_id=symbol, 
                    side="buy" if signal == 1 else "sell", 
                    funds="100"
                )
                logging.info(f"Coinbase: Executed {('BUY' if signal == 1 else 'SELL')} order for {symbol}")

            else:
                raise ValueError("Invalid platform or missing API client.")

        except Exception as e:
            logging.error(f"Trade execution error: {str(e)}")


class TradeSimulator:
    """Handles backtesting and performance evaluation of trading strategies."""
    
    def __init__(self, market_data, initial_capital=10000, transaction_cost=0.001, slippage=0.0005, risk_free_rate=0.0):
        self.data = np.array(market_data)
        self.initial_capital = initial_capital
        self.transaction_cost = transaction_cost
        self.slippage = slippage
        self.risk_free_rate = risk_free_rate

    def backtest(self, chromosome):
        """Simulates trading and calculates performance metrics."""
        capital = self.initial_capital
        position = 0
        returns = []
        peak_capital = capital
        max_drawdown = 0

        for i, signal in enumerate(chromosome):
            try:
                execution_price = self.data[i] * (1 - self.slippage) if signal == 1 else self.data[i] * (1 + self.slippage)

                if signal == 1:  # Buy
                    position = (capital * (1 - self.transaction_cost)) / execution_price
                    capital -= capital * self.transaction_cost
                elif signal == 0 and position > 0:  # Sell
                    capital = position * execution_price * (1 - self.transaction_cost)
                    position = 0
                    returns.append((capital - self.initial_capital) / self.initial_capital)

                peak_capital = max(peak_capital, capital)
                drawdown = (peak_capital - capital) / peak_capital
                max_drawdown = max(max_drawdown, drawdown)
            except Exception as e:
                logging.error(f"Error during backtesting: {str(e)}")

        sharpe_ratio = (np.mean(returns) - self.risk_free_rate) / (np.std(returns) + 1e-6) if returns else 0
        profit_factor = sum(r for r in returns if r > 0) / abs(sum(r for r in returns if r < 0) + 1e-6) if returns else 1
        
        return capital, sharpe_ratio, max_drawdown, profit_factor


class GeneticTradingStrategy:
    """Implements a genetic algorithm for trading strategy optimization."""
    
    def __init__(self, market_data, pop_size=100, generations=200, mutation_rate=0.02, crossover_rate=0.7):
        self.data = np.array(market_data)
        self.strategy_size = len(self.data) - 1
        self.pop_size = pop_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.simulator = TradeSimulator(market_data)

        self.strategy_type = self._detect_optimal_strategy()
        self.population = self._initialize_population()

    def _detect_optimal_strategy(self):
        """Determine the best strategy type based on market volatility."""
        price_changes = np.diff(self.data)
        volatility = np.std(price_changes)
        
        if volatility > np.median(price_changes):  
            return "multi-class"
        elif np.mean(price_changes) > 0:
            return "continuous"
        else:
            return "binary"

    def _initialize_population(self):
        """Generate an initial population of trading strategies."""
        if self.strategy_type == "binary":
            return [np.random.randint(2, size=self.strategy_size).tolist() for _ in range(self.pop_size)]
        elif self.strategy_type == "continuous":
            return [np.random.uniform(-1, 1, self.strategy_size).tolist() for _ in range(self.pop_size)]
        elif self.strategy_type == "multi-class":
            return [np.random.randint(3, size=self.strategy_size).tolist() for _ in range(self.pop_size)]
        else:
            raise ValueError("Unsupported strategy type.")

    def _select_parents(self):
        """Select parents for reproduction based on fitness ranking."""
        fitness_scores = np.array([self.simulator.backtest(chromosome)[1] for chromosome in self.population])
        probabilities = fitness_scores / np.sum(fitness_scores)
        return list(np.random.choice(self.population, size=2, p=probabilities))

    def _crossover(self, parent1, parent2):
        """Apply crossover between two parents to generate offspring."""
        if random.random() < self.crossover_rate:
            point = random.randint(1, self.strategy_size - 1)
            return parent1[:point] + parent2[point:], parent2[:point] + parent1[point:]
        return parent1, parent2

    def _mutate(self, chromosome):
        """Apply mutation to a trading strategy."""
        for i in range(len(chromosome)):
            if random.random() < self.mutation_rate:
                chromosome[i] = random.choice([-1, 0, 1]) if self.strategy_type == "multi-class" else random.randint(0, 1)
        return chromosome

    def evolve(self):
        """Run the genetic algorithm to optimize the trading strategy."""
        for _ in range(self.generations):
            new_population = []
            for _ in range(self.pop_size // 2):
                parent1, parent2 = self._select_parents()
                offspring1, offspring2 = self._crossover(parent1, parent2)
                new_population.extend([self._mutate(offspring1), self._mutate(offspring2)])
            self.population = new_population
        
        return max(self.population, key=lambda chromo: self.simulator.backtest(chromo)[1])

# Usage Example
# market_data = [...]  # Load real market data
# strategy = GeneticTradingStrategy(market_data)
# best_strategy = strategy.evolve()
# api_manager = APIManager()
# signal = best_strategy[-1]
# api_manager.execute_trade("BTC-USD", signal, "coinbase")