from django.shortcuts import render
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_GET
from .utils import (preprocess_income_data, preprocess_reservations_data,
                    get_year_or_current, generate_n_past_years)


@require_GET
def stats_home(request):
    years_choices = generate_n_past_years(4)

    return render(request, 'stats/stats.html', {"years_choices": years_choices})


@require_GET
def income_data(request):
    try:
        year = get_year_or_current(request.GET)
    except ValueError:
        return HttpResponseBadRequest("Invalid year format.")

    income_data = preprocess_income_data(year)
    return JsonResponse(income_data)


@require_GET
def paid_unpaid_reservations_data(request):
    try:
        year = get_year_or_current(request.GET)
    except ValueError:
        return HttpResponseBadRequest("Invalid year format.")

    reservations_data = preprocess_reservations_data(year)
    return JsonResponse(reservations_data)
