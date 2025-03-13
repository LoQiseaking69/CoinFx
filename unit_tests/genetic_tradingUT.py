import unittest
import numpy as np
from unittest.mock import patch
from genetic_trading import GeneticTradingStrategy

class TestGeneticTradingStrategy(unittest.TestCase):
    """Test Suite for Genetic Algorithm Strategy Optimization"""

    def setUp(self):
        """Initialize a small test dataset."""
        self.data = np.random.rand(100, 5)  # Simulated market data
        self.strategy = GeneticTradingStrategy(self.data, pop_size=10, generations=5)

    def test_initial_population_size(self):
        """Test if initial population is correctly created."""
        self.assertEqual(len(self.strategy.population), 10)

    def test_strategy_evolution(self):
        """Test evolution of trading strategies."""
        best_strategy_before = max(self.strategy.population, key=lambda chromo: np.random.random())
        evolved_strategy = self.strategy.evolve()
        self.assertEqual(len(evolved_strategy), len(best_strategy_before))

    def test_mutation_changes_strategy(self):
        """Ensure mutation modifies the strategy."""
        chromosome = [0] * self.strategy.strategy_size
        mutated = self.strategy._mutate(chromosome[:])
        self.assertNotEqual(chromosome, mutated)

if __name__ == "__main__":
    unittest.main()