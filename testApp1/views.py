from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("こんにちは Discord開発サーバーの記念すべき1ページ目です。")
