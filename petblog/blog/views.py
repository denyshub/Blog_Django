from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    return HttpResponse('Сторінка блогу')

def categories(request):
    return HttpResponse("<h1>Блоги за категоріями</h1>")
