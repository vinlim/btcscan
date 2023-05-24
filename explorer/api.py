from django.http import HttpRequest, JsonResponse
from explorer.services import estimator, transaction


def estimate(request: HttpRequest):
    tx_hash = request.GET.get('tx_hash')
    if not tx_hash:
        return JsonResponse({'error': 'Transaction hash required'}, status=400)

    tx = transaction.get_transaction(tx_hash)
    time_to_confirmation = estimator.estimate(tx.fee_rate)
    print(time_to_confirmation)
    data = {
        'status': 'ok',
        'result': {
            'time_to_confirmation': time_to_confirmation,
            'description': tx.describe(time_to_confirmation)
        }
    }
    return JsonResponse(data)
