from django.test import TestCase
from unittest.mock import patch
from explorer.services.mempool import Mempool, get_mempools, make_request, get_mempools_transactions


class MempoolTestCase(TestCase):

    def setUp(self):
        self.mempool = Mempool('testname', 'testendpoint', 'testauth')

    @patch('explorer.services.mempool.request.json_rpc')
    def test_make_request(self, mock_json_rpc):
        mock_json_rpc.return_value = {
            'a1234': {
                'transaction': {
                    'txid': 'a1234',
                    'size': 100,
                    'weight': 200,
                    'fee': 1000,
                },
            },
            'a1235': {
                'transaction': {
                    'txid': 'a1235',
                    'size': 200,
                    'weight': 400,
                    'fee': 2000,
                }
            }
        }

        result = make_request(self.mempool)
        assert isinstance(result, dict), 'Result should be a dict with tx_hash as key and tx_info (' \
                                         'dict) as value'

    @patch('explorer.services.mempool.make_request')
    def test_get_mempools_transactions(self, mock_make_request):
        mock_make_request.return_value = {
            'a1234': {
                'transaction': {
                    'txid': 'a1234',
                    'size': 100,
                    'weight': 200,
                    'fee': 1000,
                },
            },
            'a1235': {
                'transaction': {
                    'txid': 'a1235',
                    'size': 200,
                    'weight': 400,
                    'fee': 2000,
                }
            }
        }

        combined_transactions = get_mempools_transactions()
        assert isinstance(combined_transactions, dict), 'Result should be a dict with tx_hash as key and tx_info (' \
                                                        'dict) as value'

    def test_get_mempools(self):
        mempools = get_mempools()
        self.assertIsInstance(mempools, list)
        for mempool in mempools:
            self.assertIsInstance(mempool, Mempool)
