from django.http import HttpRequest
from django.shortcuts import render


def index(request: HttpRequest):
    return render(request, "index.html")


def view(request: HttpRequest, tx_hash: str):
    context = {
        "tx_hash": tx_hash
    }
    return render(request, "view.html", context)
