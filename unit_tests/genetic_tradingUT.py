import unittest
import numpy as np
from genetic_trading import GeneticTradingStrategy

class TestGeneticTradingStrategy(unittest.TestCase):
    """Test Suite for Genetic Algorithm Strategy Optimization"""

    def setUp(self):
        """Initialize a small test dataset."""
        # Generate mock close prices for realistic fitness
        self.data = np.linspace(100, 200, 102).reshape(-1, 1)  # 102 points → 101 strategy size
        self.strategy = GeneticTradingStrategy(self.data, pop_size=10, generations=5)

    def test_initial_population_size(self):
        """Test if initial population is correctly created."""
        self.assertEqual(len(self.strategy.population), 10)
        for chromo in self.strategy.population:
            self.assertEqual(len(chromo), self.strategy.strategy_size)

    def test_strategy_evolution(self):
        """Test that evolve returns a valid strategy of correct size."""
        evolved = self.strategy.evolve()
        self.assertEqual(len(evolved), self.strategy.strategy_size)
        self.assertTrue(all(gene in [0, 1] for gene in evolved))

    def test_mutation_changes_strategy(self):
        """Ensure mutation alters at least one gene when mutation_rate > 0."""
        self.strategy.mutation_rate = 1.0  # Force all bits to flip
        chromosome = [0] * self.strategy.strategy_size
        mutated = self.strategy._mutate(chromosome[:])
        self.assertNotEqual(chromosome, mutated)
        self.assertTrue(all(gene == 1 for gene in mutated))

    def test_fitness_evaluation_increases_with_trend(self):
        """Verify fitness rises with upward market trend and valid strategy."""
        chromo = [1 if i % 2 == 0 else 0 for i in range(self.strategy.strategy_size)]
        fitness = self.strategy._evaluate_fitness(chromo)
        self.assertGreater(fitness, 1000)  # Started capital baseline

if __name__ == "__main__":
    unittest.main()