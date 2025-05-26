import unittest
from ExamplePolytopes import *
from Project.Services.Calculation.CapacityService import *


class TestCapacityService(unittest.TestCase):
    bs = get_billiard_system_from_hiam_ostrover_counterexample()


    def test_get_capacity_gets_correct_for_hiam_ostrover(self):
        # Setup
        vol = self.bs.volume_k_metric
        expected_capacity = self.bs.capacity_k_of_t.length

        # Execute
        cap = get_capacity(T=self.bs.T, K=self.bs.K, volume_k_metric=vol)

        # Assert
        np.testing.assert_almost_equal(cap.length, expected_capacity)


if __name__ == '__main__':
    unittest.main()
