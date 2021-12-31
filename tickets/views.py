from django.http.response import HttpResponse
from django.shortcuts import render
from django.http import HttpResponse


def tickets_home(request):
    return HttpResponse("Tickets")
