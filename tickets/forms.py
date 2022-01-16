import datetime
import PIL
from pyzbar import pyzbar
from django import forms
from .models import Reservation
from panel.utils import get_config
from .utils import calculate_ticket_price, find_next_available_swimlane, facility_open
from .exceptions import NoAvailableSwimlaneError, FacilityClosedError


class ReservationForm(forms.ModelForm):
    duration_choices = [(duration, f"{duration}h") for duration in range(1, 8)]

    duration = forms.ChoiceField(choices=duration_choices)
    start_date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))

    def save(self, commit=True):
        """
        Parses the form data. When everything is validated, saves a Reservation
        instance to the database and returns it.
        """

        config = get_config()

        reservation = super().save(commit=False)

        end_date = datetime.timedelta(hours=int(self.cleaned_data['duration']))
        reservation.end_date = reservation.start_date + end_date

        swimlane = find_next_available_swimlane(config,
                                                reservation.client_type,
                                                reservation.start_date,
                                                reservation.end_date)

        if not swimlane:
            raise NoAvailableSwimlaneError("No available swimlane found for this reservation time.")

        if not facility_open(config, reservation.start_date, reservation.end_date):
            raise FacilityClosedError(f"{config.name} is closed during provided reservation time.")

        reservation.swimlane = swimlane
        reservation.price = calculate_ticket_price(config, reservation.client_type,
                                                   reservation.start_date)

        if commit:
            reservation.save()

        return reservation

    class Meta:
        model = Reservation
        fields = ['start_date', 'client_type']


class PayForReservationForm(forms.Form):
    reservation_id = forms.CharField(max_length=8, strip=True, required=False)
    ticket = forms.ImageField(required=False)

    def is_valid(self):
        """
        Returns a boolean representing whether the form data is valid.
        """

        if not super().is_valid():
            return False

        return self.cleaned_data['reservation_id'] or self.cleaned_data['ticket']

    def parse_reservation_id(self):
        """
        Parses reservation_id from the form: firstly considers id provided
        in the CharField, then tries to decode it from the uploaded QR code.
        """

        if self.cleaned_data['reservation_id']:
            return self.cleaned_data['reservation_id']

        if self.cleaned_data['ticket']:
            image_bytes = self.cleaned_data['ticket'].file
            decoded_qr = pyzbar.decode(PIL.Image.open(image_bytes))

            return decoded_qr[0].data.decode()
