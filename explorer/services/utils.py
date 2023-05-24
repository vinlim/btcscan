def sat_to_btc(sat):
    return sat / 1e8


def btc_to_sat(btc):
    return btc * 100000000


def short_hash(hash):
    return hash[:6] + '...' + hash[-6:]
