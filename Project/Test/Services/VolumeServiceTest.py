import unittest

from Project.Services.Calculation.VolumeService import *
from ExamplePolytopes import *


class VolumeServiceTest(unittest.TestCase):
    bs = get_billiard_system_from_hiam_ostrover_counterexample()

    def test_get_volume_k_metric_gets_correct_for_hiam_ostrover(self):
        # Setup
        expected_vol = self.bs.volume_k_metric

        # Execute
        vol = get_volume_k_metric(self.bs.K, self.bs.T)

        # Assert
        np.testing.assert_almost_equal(vol, expected_vol)

    def test_polar_dual_of_polar_dual_is_original_polytope(self):
        # Execute
        k_polar_dual = get_polar_dual(self.bs.K)
        k_polar_dual_polar_dual = get_polar_dual(k_polar_dual)

        # Assert
        self.assertEqual(k_polar_dual_polar_dual, self.bs.K)

    def test_K_is_not_equal_to_its_polar_dual(self):
        # Execute
        k_polar_dual = get_polar_dual(self.bs.K)

        # Assert
        self.assertNotEqual(k_polar_dual, self.bs.K)


if __name__ == '__main__':
    unittest.main()
