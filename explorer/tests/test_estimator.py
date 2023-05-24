from django.test import TestCase
from unittest.mock import patch
from explorer.services import estimator, mempool


class EstimatorTestCase(TestCase):

    @patch.object(mempool, 'get_mempools_transactions')
    def test_estimate(self, mock_get_mempools_transactions):
        mock_get_mempools_transactions.return_value = {
            'tx1': {
                'fees': {'modified': 0.20},
                'vsize': 999999,
                'weight': 1999999
            },
            'tx2': {
                'fees': {'modified': 0.18},
                'vsize': 999999,
                'weight': 1999999
            },
            'tx3': {
                'fees': {'modified': 0.16},
                'vsize': 999999,
                'weight': 1999999
            },
            'tx4': {
                'fees': {'modified': 0.14},
                'vsize': 999999,
                'weight': 1999999
            },
            'tx5': {
                'fees': {'modified': 0.12},
                'vsize': 999999,
                'weight': 1999999
            },
            'tx6': {
                'fees': {'modified': 0.10},
                'vsize': 999999,
                'weight': 1999999
            },

        }

        # Now test the estimate function
        result = estimator.estimate(15.8)
        self.assertEqual(result, 20)
