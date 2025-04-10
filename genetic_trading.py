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
        token = os.getenv("OANDA_ACCESS_TOKEN")
        return oandapyV20.API(access_token=token) if token else None

    def _initialize_coinbase_client(self):
        key = os.getenv("COINBASE_API_KEY")
        secret = os.getenv("COINBASE_API_SECRET")
        passphrase = os.getenv("COINBASE_API_PASSPHRASE")
        return cbpro.AuthenticatedClient(key, secret, passphrase) if key and secret and passphrase else None

    def execute_trade(self, symbol, signal, platform, amount="100"):
        try:
            if platform == "oanda" and self.oanda_client:
                order_data = {
                    "order": {
                        "instrument": symbol,
                        "units": int(amount) if signal == 1 else -int(amount),
                        "type": "MARKET",
                        "positionFill": "DEFAULT"
                    }
                }
                account_id = os.getenv("OANDA_ACCOUNT_ID")
                self.oanda_client.request(orders.OrderCreate(account_id, data=order_data))
                logger.info(f"OANDA: Executed {'BUY' if signal == 1 else 'SELL'} on {symbol} for {amount} units.")

            elif platform == "coinbase" and self.coinbase_client:
                self.coinbase_client.place_market_order(
                    product_id=symbol,
                    side="buy" if signal == 1 else "sell",
                    funds=str(amount)
                )
                logger.info(f"Coinbase: Executed {'BUY' if signal == 1 else 'SELL'} on {symbol} with ${amount}.")

            else:
                raise ValueError("Invalid platform or missing API client.")

        except Exception as e:
            logger.error(f"Trade execution error: {e}")


class GeneticTradingStrategy:
    """Genetic Algorithm for evolving trading strategies."""

    def __init__(self, market_data, pop_size=100, generations=200, mutation_rate=0.02, crossover_rate=0.7):
        self.data = self._prepare_data(market_data)
        if len(self.data) < 2:
            raise ValueError("Market data must have at least two prices for strategy generation.")
        self.strategy_size = len(self.data) - 1
        self.pop_size = pop_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.population = self._initialize_population()

    def _prepare_data(self, data):
        arr = np.array(data)
        if len(arr.shape) > 1 and arr.shape[1] > 1:
            arr = arr[:, 1]  # use price column
        return arr.astype(float)

    def _initialize_population(self):
        return [np.random.randint(0, 2, size=self.strategy_size).tolist() for _ in range(self.pop_size)]

    def _evaluate_fitness(self, chromosome):
        capital = 1000.0
        position = 0.0
        for i in range(len(chromosome)):
            price_now = self.data[i]
            price_next = self.data[i + 1]

            if chromosome[i] == 1 and position == 0.0:
                position = price_now  # BUY
            elif chromosome[i] == 0 and position > 0.0:
                capital += price_next - position  # SELL
                position = 0.0

        # If still holding, liquidate at last known price
        if position > 0.0:
            capital += self.data[-1] - position

        return capital

    def _select_parents(self):
        fitness_scores = np.array([self._evaluate_fitness(chromo) for chromo in self.population])
        total_fitness = np.sum(fitness_scores)
        if total_fitness == 0:
            fitness_scores = np.ones_like(fitness_scores)
            total_fitness = np.sum(fitness_scores)
        probabilities = fitness_scores / total_fitness
        idx = np.random.choice(len(self.population), size=2, p=probabilities)
        return self.population[idx[0]], self.population[idx[1]]

    def _crossover(self, p1, p2):
        if random.random() < self.crossover_rate:
            point = random.randint(1, self.strategy_size - 1)
            return p1[:point] + p2[point:], p2[:point] + p1[point:]
        return p1, p2

    def _mutate(self, chromo):
        return [1 - gene if random.random() < self.mutation_rate else gene for gene in chromo]

    def evolve(self):
        for _ in range(self.generations):
            next_gen = []
            for _ in range(self.pop_size // 2):
                p1, p2 = self._select_parents()
                c1, c2 = self._crossover(p1, p2)
                next_gen.extend([self._mutate(c1), self._mutate(c2)])
            self.population = next_gen
        best = max(self.population, key=self._evaluate_fitness)
        logger.info(f"Evolved strategy fitness: {self._evaluate_fitness(best):.2f}")
        return best

    def backtest(self):
        best = self.evolve()
        return round(self._evaluate_fitness(best), 2)