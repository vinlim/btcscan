from django.conf import settings
from explorer.services import request


class Mempool:
    def __init__(self, name: str, endpoint: str, authorisation=''):
        self.name = name
        self.endpoint = endpoint
        self.authorisation = authorisation

    def __str__(self):
        return self.name + ": " + self.endpoint


def get_mempools():
    # return [
    #     Mempool('quicknode',
    #             'https://burned-wispy-firefly.btc.discover.quiknode.pro/4001e4ad07ad483349e64a1ad75b6fce7b573f5e/'),
    #     Mempool('getblock',
    #             'https://btc.getblock.io/13a75767-3f11-452c-9949-a13a06c24ef2/mainnet/',
    #             'Basic YWRtaW46cGFzc3dvcmQ=')
    # ]
    return [
        Mempool('quicknode',
                settings.NODE_PROVIDERS['quicknode']['endpoint']),
        Mempool('getblock',
                settings.NODE_PROVIDERS['getblock']['endpoint'],
                settings.NODE_PROVIDERS['getblock']['auth'])
    ]


def make_request(mempool: Mempool):
    result = request.json_rpc(
        endpoint=mempool.endpoint,
        method='getrawmempool',
        authorisation=mempool.authorisation or '',
        params=[
            True
        ],
    )

    # print(f'Count for {mempool.name}', len(result))
    return result


def get_mempools_transactions():
    mempools = get_mempools()

    combined = {}
    for mempool in mempools:
        # Todo: consider making async request to reduce wait time
        results = make_request(mempool)
        combined = {**combined, **results}

    # print(f'Combined count: ', len(combined))
    return combined


if __name__ == "__main__":
    get_mempools_transactions()
