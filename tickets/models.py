import uuid
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


def generate_reservation_id():
    return uuid.uuid4().hex[:8]


class Reservation(models.Model):
    PRIVATE_CLIENT = 'private_client'
    SWIM_SCHOOL = 'swim_school'

    id = models.CharField(max_length=8,
                          primary_key=True,
                          default=generate_reservation_id,
                          editable=False)

    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    swimlane = models.IntegerField(validators=[
            MinValueValidator(1),
            MaxValueValidator(20)])

    client_type = models.CharField(max_length=30,
                                   default=PRIVATE_CLIENT,
                                   choices=[(PRIVATE_CLIENT, 'Private client'),
                                            (SWIM_SCHOOL, 'Swim school')])

    price = models.DecimalField(max_digits=7, decimal_places=2)
    is_paid = models.BooleanField(default=False)

    @classmethod
    def get_overlapping_reservations(cls, date_from, date_to):
        """
        Returns from the database all reservations, which overlap 
        with the given interval in any point in time.
        """

        return cls.objects.filter(start_date__lte=date_to, end_date__gte=date_from)

    def __str__(self):
        start_date = self.start_date.strftime('%d/%m/%y %H:%M')

        return f'{self.id} - {self.client_type} - {start_date}'
