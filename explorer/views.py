from urllib.error import HTTPError
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse
from explorer.services import transaction


def index(request: HttpRequest):
    return render(request, "index.html")


def search(request):
    tx_hash = request.GET.get('tx_hash')
    print('yes i got: ', tx_hash)
    return redirect('explorer_view', tx_hash=tx_hash)


def view(request: HttpRequest, tx_hash: str):
    try:
        tx = transaction.get_transaction(tx_hash)
        context = {
            'transaction': tx,
            'description': tx.describe
        }
        return render(request, "view.html", context)
    except HTTPError:
        return redirect(f'{reverse("explorer_index")}?err=tx_404')
