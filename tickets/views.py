import qrcode
from datetime import datetime
from django.http.response import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from django.views.decorators.http import require_GET, require_POST
from .forms import ReservationForm, PayForReservationForm
from .utils import get_swimlines_info, pay_for_reservation
from .models import Reservation
from panel.utils import get_config
from .exceptions import NoAvailableSwimlaneError, FacilityClosedError, ReservationAlreadyPaidForError


@require_GET
def tickets_home(request):
    config = get_config()
    current_reservations = Reservation.get_overlapping_reservations(datetime.now(),
                                                                    datetime.now())

    info = get_swimlines_info(config, current_reservations)[0]
    form = ReservationForm()
    pay_form = PayForReservationForm()

    return render(request, 'tickets/tickets.html', {'form': form, 'pay_form': pay_form, 'info': info})


@require_POST
def make_reservation(request):
    form = ReservationForm(request.POST)
    reservation_id = None

    if form.is_valid():
        try:
            reservation = form.save()
            reservation_id = reservation.id

            # flake8: noqa E501
            qr_code_ahref = f"<a href='{reverse('generate-qr', args=[reservation_id])}'>Get the ticket.</a>"

            messages.success(request, f'Reservation <b>{reservation_id}</b> created. ' \
                                      f'Price: {reservation.price}. {qr_code_ahref}', extra_tags='success')
        except (NoAvailableSwimlaneError, FacilityClosedError) as error_msg:
            messages.error(request, error_msg, extra_tags='danger')
    else:
        messages.error(request, 'Reservation form contains errors.', extra_tags='danger')

    return HttpResponseRedirect(reverse('home'))


@require_POST
def reservation_pay(request):
    pay_form = PayForReservationForm(request.POST, request.FILES)

    if not pay_form.is_valid():
        messages.error(request, 'Invalid form data.', extra_tags='danger')
        return HttpResponseRedirect(reverse('home'))

    try:
        pay_for_reservation(pay_form.parse_reservation_id())
        messages.success(request, f'Payment succesfull.', extra_tags='success')
    except Reservation.DoesNotExist:
        messages.error(request, 'Invalid reservation id.', extra_tags='danger')
    except ReservationAlreadyPaidForError as err:
        messages.error(request, err, extra_tags='danger')

    return HttpResponseRedirect(reverse('home'))


@require_GET
def generate_qr(request, id):
    img = qrcode.make(id)
    response = HttpResponse(content_type='image/png')
    response['Content-Disposition'] = f"attachment; filename=Reservation_{id}.png"
    img.save(response, "PNG")

    return response
