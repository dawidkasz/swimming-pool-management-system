import datetime
from django import forms
from .models import Reservation
from panel.utils import get_config
from .utils import calculate_ticket_price, find_next_available_swimlane, facility_open
from .exceptions import NoAvailableSwimlaneError, FacilityClosedError


class ReservationForm(forms.ModelForm):
    duration_choices = [(duration, duration) for duration in range(1, 8)]
    duration = forms.ChoiceField(choices=duration_choices)

    start_date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))

    def save(self, commit=True):
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
