import numpy as np
import random
import logging
import os
import oandapyV20
import oandapyV20.endpoints.orders as orders
import cbpro
from config import TRADING_CONFIG, get_logger

logger = get_logger()

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
                logger.info(f"OANDA: Executed {('BUY' if signal == 1 else 'SELL')} order for {symbol}")

            elif platform == "coinbase" and self.coinbase_client:
                self.coinbase_client.place_market_order(
                    product_id=symbol, 
                    side="buy" if signal == 1 else "sell", 
                    funds="100"
                )
                logger.info(f"Coinbase: Executed {('BUY' if signal == 1 else 'SELL')} order for {symbol}")

            else:
                raise ValueError("Invalid platform or missing API client.")

        except Exception as e:
            logger.error(f"Trade execution error: {str(e)}")

class GeneticTradingStrategy:
    """Implements a genetic algorithm for trading strategy optimization."""

    def __init__(self, market_data, pop_size=100, generations=200, mutation_rate=0.02, crossover_rate=0.7):
        self.data = np.array(market_data)
        self.strategy_size = len(self.data) - 1
        self.pop_size = pop_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.population = self._initialize_population()

    def _initialize_population(self):
        """Generate an initial population of trading strategies."""
        return [np.random.randint(2, size=self.strategy_size).tolist() for _ in range(self.pop_size)]

    def _select_parents(self):
        """Select parents for reproduction based on fitness ranking."""
        fitness_scores = np.array([np.random.random() for _ in self.population])  # Placeholder fitness scores
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
                chromosome[i] = 1 - chromosome[i]
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
        
        return max(self.population, key=lambda chromo: np.random.random())  # Placeholder for actual fitness function