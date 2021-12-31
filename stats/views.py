from django.shortcuts import render


def stats_home(request):
    return render(request, 'stats/stats.html')
