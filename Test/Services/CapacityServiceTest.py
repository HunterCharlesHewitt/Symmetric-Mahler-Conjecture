import unittest
from ExamplePolytopes import *
from Services import CapacityService
from Services.CapacityService import *


class CapacityServiceTest(unittest.TestCase):
    K, T = get_K_T_from_hiam_ostrover_counterexample()


    def test_get_capacity_gets_correct_for_hiam_ostrover(self):
        # Setup
        vol = get_vol_from_hiam_ostrover_counterexample()
        expected_capacity = get_capacity_from_hiam_ostrover_counterexample()

        # Execute
        cap = get_capacity(self.T, self.K, vol)

        # Assert
        np.testing.assert_almost_equal(cap.length, expected_capacity)


if __name__ == '__main__':
    unittest.main()
