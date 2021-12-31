from django.shortcuts import render


def tickets_home(request):
    return render(request, 'tickets/tickets.html')
