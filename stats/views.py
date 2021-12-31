from django.shortcuts import render
from django.http import HttpResponse


def stats_home(request):
    return HttpResponse("Stats")
