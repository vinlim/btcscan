from explorer.services import request, utils


class Transaction:
    def __init__(self,
                 txid: str,
                 size: int,
                 weight: int,
                 fee: int,
                 vin: list = list,
                 vout: list = list,
                 confirmed: bool = False,
                 block_height: int = None,
                 block_hash: str = None,
                 block_time: int = None
                 ):
        self.txid = txid
        self.size = size
        self.weight = weight
        self.fee = fee
        self.vin = vin
        self.vout = vout
        self.confirmed = confirmed
        self.block_height = block_height
        self.block_hash = block_hash
        self.block_time = block_time
        self.v_size = int(weight / 4)
        self.fee_rate = fee / weight * 4
        self.amount: int = sum(output['value'] for output in vout)

    def __str__(self):
        return self.txid

    def describe(self, estimated_time_to_confirmation: int = None):
        address_count = len(self.vout)
        transaction_doing = f"This is transaction is sending { '{:.8f}'.format(utils.sat_to_btc(self.amount)) } BTC to {address_count} addresses. " \
            if not self.confirmed else \
            f"This transaction sent { '{:.8f}'.format(utils.sat_to_btc(self.amount)) } BTC to {address_count} addresses. "
        transaction_state = f"The transaction is now confirming" \
            if not self.confirmed else \
            f"The transaction is confirmed."
        transaction_estimation = f", and will be confirmed in approximately {estimated_time_to_confirmation} minutes. "

        if self.confirmed:
            return transaction_doing + transaction_state
        elif not self.confirmed and estimated_time_to_confirmation:
            return transaction_doing + transaction_state + transaction_estimation
        else:
            return transaction_doing + transaction_state + '.'


def get_transaction(tx_hash: str):
    payload = request.get_request(f'https://mempool.space/api/tx/{tx_hash}')
    return Transaction(
        txid=payload['txid'],
        size=payload['size'],
        weight=payload['weight'],
        fee=payload['fee'],
        vin=payload['vin'],
        vout=payload['vout'],
        confirmed=payload['status']['confirmed'],
        block_height=payload['status'].get('block_height', None),
        block_hash=payload['status'].get('block_hash', None),
        block_time=payload['status'].get('block_time', None)
    )
