import datetime
from django.db import models
from solo.models import SingletonModel


class SiteConfiguration(SingletonModel):
    name = models.CharField(max_length=255, default='Swimming pool management system')

    num_of_swimlanes = models.IntegerField(default=5)
    spots_per_swimlane = models.IntegerField(default=5)

    open_time_weekdays = models.TimeField(default=datetime.time(10, 0))
    close_time_weekdays = models.TimeField(default=datetime.time(18, 0))

    open_time_weekends = models.TimeField(default=datetime.time(10, 0))
    close_time_weekends = models.TimeField(default=datetime.time(16, 0))

    price_weekdays_private_clients = models.DecimalField(max_digits=6,
                                                         decimal_places=2, default=6.99)
    price_weekends_private_clients = models.DecimalField(max_digits=6,
                                                         decimal_places=2, default=7.59)

    price_weekdays_swim_schools = models.DecimalField(max_digits=6,
                                                         decimal_places=2, default=32.99)
    price_weekends_swim_schools = models.DecimalField(max_digits=6,
                                                      decimal_places=2, default=35.99)

    swim_schools_treshold = models.DecimalField(max_digits=3, decimal_places=2, default=0.35)
    entry_at_opening_discount = models.DecimalField(max_digits=3, decimal_places=2, default=1)

    def __str__(self):
        return f'{self.name} configuration'

    class Meta:
        verbose_name = 'Site Configuration'
