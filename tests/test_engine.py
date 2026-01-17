import unittest
import numpy as np
from engine import CellularAutomata

class TestCellularAutomata(unittest.TestCase):
    def test_wolfram_rule30(self):
        ca = CellularAutomata(width=5, states=2, radius=1, rule=30)
        ca.initialize(mode='pattern', pattern='00100')
        next_grid = ca.step(ca.grid)
        np.testing.assert_array_equal(next_grid, [0, 1, 1, 1, 0])

    def test_totalistic(self):
        rule = "0101010"
        ca = CellularAutomata(width=3, states=3, radius=1, rule=rule, totalistic=True)
        ca.grid = np.array([1, 1, 1])
        next_grid = ca.step(ca.grid)
        np.testing.assert_array_equal(next_grid, [1, 1, 1])

    def test_initialization(self):
        ca = CellularAutomata(width=10, states=3)
        ca.initialize(mode='center', pattern='121')
        expected = np.array([0, 0, 0, 1, 2, 1, 0, 0, 0, 0])
        np.testing.assert_array_equal(ca.grid, expected)

if __name__ == '__main__':
    unittest.main()
