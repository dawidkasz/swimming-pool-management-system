from django.http.response import HttpResponse
from django.shortcuts import render
from django.http import HttpResponse


def panel_home(request):
    return HttpResponse("Panel")
