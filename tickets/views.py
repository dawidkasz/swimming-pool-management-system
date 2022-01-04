from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from .forms import ReservationForm
from .exceptions import NoAvailableSwimlaneError, FacilityClosedError


def tickets_home(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)

        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Reservation made!', extra_tags='success')
            except (NoAvailableSwimlaneError, FacilityClosedError) as error_msg:
                messages.error(request, error_msg, extra_tags='danger')
        else:
            messages.error(request, 'Reservation form contains errors.', extra_tags='danger')

        return HttpResponseRedirect('/')

    form = ReservationForm()
    return render(request, 'tickets/tickets.html', {'form': form})
