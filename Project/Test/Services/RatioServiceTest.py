import unittest

from Project.Test.Services.ExamplePolytopes import *
from Project.Services.Calculation.RatioService import set_billiard_system_ratio
from Project.Models.BilliardSystem import BilliardSystem
from unittest.mock import patch


class RatioServiceTest(unittest.TestCase):

    @patch('Project.Services.Calculation.CapacityService.get_capacity')
    @patch('Project.Services.Calculation.VolumeService.get_volume_k_metric')
    def test_ratio_is_calculated_correctly_for_hiam_oslev(self, mock_get_volume_k_metric, mock_get_capacity):
        # Setup
        bs = get_billiard_system_from_hiam_ostrover_counterexample()
        billiard_system = BilliardSystem(K=bs.K, T=bs.T)
        expected_ratio = bs.ratio
        mock_get_volume_k_metric.return_value = bs.volume_k_metric
        mock_get_capacity.return_value = bs.capacity_k_of_t

        # Execute
        set_billiard_system_ratio(billiard_system)

        # Assert
        np.testing.assert_almost_equal(billiard_system.ratio, expected_ratio)


if __name__ == '__main__':
    unittest.main()
