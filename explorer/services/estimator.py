from explorer.services import mempool
from explorer.services import utils


def get_fee_rate(weight: int, fee: int) -> float:
    v_size = weight / 4
    return fee / v_size


def get_min_max_fee_rate_from_bucket(bucket):
    min_fee_rate = float('inf')
    max_fee_rate = float('-inf')
    for transaction in bucket:
        fee_rate = transaction['fee_rate']
        min_fee_rate = min(min_fee_rate, fee_rate)
        max_fee_rate = max(max_fee_rate, fee_rate)

    return min_fee_rate, max_fee_rate


def estimate(target_fee_rate: float) -> int:
    transactions = mempool.get_mempools_transactions()

    # Calculate and append fee_rate to each transaction
    for tx_hash, tx_info in transactions.items():
        fee_btc = tx_info["fees"]["modified"]
        fee_sats = utils.btc_to_sat(fee_btc)
        tx_info["fee_rate"] = fee_sats / tx_info["vsize"]

    # Sort transactions based on the fee_rate
    sorted_transactions = sorted(
        transactions.items(),
        key=lambda x: x[1]["fee_rate"],
        reverse=True
    )

    # Group items into buckets with weight not over 4,000,000 weight unit
    buckets = []
    current_bucket = []
    current_bucket_size = 0
    bucket_wu_limit = 4000000
    for tx_hash, tx_info in sorted_transactions:
        if current_bucket_size + tx_info['weight'] > bucket_wu_limit:
            min_max_fee_rate = get_min_max_fee_rate_from_bucket(current_bucket)
            buckets.append(({'max_fee_rate': min_max_fee_rate[1],
                             'min_fee_rate': min_max_fee_rate[0],
                             'total_weight': current_bucket_size},
                            current_bucket))
            current_bucket = []
            current_bucket_size = 0

        current_bucket.append({'tx_hash': tx_hash, 'vsize': tx_info['vsize'], 'weight': tx_info['weight'],
                               'fee_rate': tx_info['fee_rate']})
        current_bucket_size += tx_info['weight']

    if current_bucket:
        min_max_fee_rate = get_min_max_fee_rate_from_bucket(current_bucket)
        buckets.append(({'max_fee_rate': min_max_fee_rate[1],
                         'min_fee_rate': min_max_fee_rate[0],
                         'total_weight': current_bucket_size},
                        current_bucket))

    # Find the bucket matching targeted fee rate
    # Todo: consider handling edge case with upper/lower bound coverage
    for i, bucket in enumerate(buckets):
        # print(i, bucket[0]['min_fee_rate'], target_fee_rate, bucket[0]['max_fee_rate'])
        if bucket[0]['min_fee_rate'] <= target_fee_rate < bucket[0]['max_fee_rate']:
            return (i + 1) * 10

    return 0


if __name__ == "__main__":
    print('Time to confirmation: ', estimate(20.1))
