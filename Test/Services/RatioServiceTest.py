import unittest

from Test.Services.ExamplePolytopes import *
from Services.RatioService import set_billiard_system_ratio
from Models.BilliardSystem import BilliardSystem
class RatioServiceTest(unittest.TestCase):
    def test_ratio_is_calculated_correctly_for_hiam_oslev_counterexample(self):
        # Setup
        K, T = get_K_T_from_hiam_ostrover_counterexample()
        billiard_system = BilliardSystem(K=K, T=T)
        expected_ratio = get_ratio_from_hiam_ostrover_counterexample()

        # Execute
        ratio = set_billiard_system_ratio(billiard_system)

        # Assert
        np.testing.assert_almost_equal(ratio, expected_ratio)


if __name__ == '__main__':
    unittest.main()
