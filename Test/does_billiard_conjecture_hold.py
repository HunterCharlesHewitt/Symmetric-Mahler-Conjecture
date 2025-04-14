import unittest
from unittest.mock import patch
from main import does_billiard_conjecture_hold, get_unit_cube

import numpy as np


def mock_get_untranslatable_points(T, m):
    if m == 1:
        return [[np.array([0, 0])]]
    theta = np.linspace(0, 2 * np.pi, m, endpoint=False)
    polygon = [np.array([np.cos(t), np.sin(t)]) for t in theta]
    return [polygon]


class TestDoesBilliardConjectureHold(unittest.TestCase):
    def test_does_billiard_conjecture_hold_for_unit_cube(self) -> None:
        # Setup
        dim = 2
        A, b = get_unit_cube(dim)
        K = A
        T = A
        with patch('main.get_untranslatable_points', side_effect=mock_get_untranslatable_points):
            result = does_billiard_conjecture_hold(K, T, dim)

        # Execute
        does_conjecture_hold = does_billiard_conjecture_hold(K, T, dim)

        # Assert
        self.assertEqual(does_conjecture_hold, True)


if __name__ == '__main__':
    unittest.main()
