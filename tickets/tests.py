from datetime import datetime, time
from django.test import TestCase
from .models import Reservation
from .utils import (is_weekday, facility_open,
                    calculate_ticket_price, get_swimlines_info,
                    find_next_available_swimlane, pay_for_reservation)
from .exceptions import ReservationAlreadyPaidForError


class TestSetUp(TestCase):
    @classmethod
    def setUp(cls):
        cls.config = cls.MockConfig()

        cls.r1 = Reservation.objects.create(start_date=datetime(2021, 12, 29, 10, 30),
                                            end_date=datetime(2021, 12, 29, 11, 30),
                                            swimlane=2,
                                            client_type=Reservation.PRIVATE_CLIENT,
                                            price=9.9)
        cls.r2 = Reservation.objects.create(start_date=datetime(2022, 1, 10, 14, 45),
                                            end_date=datetime(2022, 1, 10, 16, 30),
                                            swimlane=1,
                                            client_type=Reservation.SWIM_SCHOOL,
                                            price=8)
        cls.r3 = Reservation.objects.create(start_date=datetime(2022, 1, 25, 8, 0),
                                            end_date=datetime(2022, 1, 25, 10, 30),
                                            swimlane=1,
                                            client_type=Reservation.PRIVATE_CLIENT,
                                            price=14.9)
        cls.r4 = Reservation.objects.create(start_date=datetime(2022, 2, 2, 15, 25),
                                            end_date=datetime(2022, 2, 2, 16, 25),
                                            swimlane=1,
                                            client_type=Reservation.PRIVATE_CLIENT,
                                            price=5.9)
        cls.r5 = Reservation.objects.create(start_date=datetime(2022, 2, 2, 15, 0),
                                            end_date=datetime(2022, 2, 2, 17, 0),
                                            swimlane=3,
                                            client_type=Reservation.SWIM_SCHOOL,
                                            price=29)
        cls.r6 = Reservation.objects.create(start_date=datetime(2022, 3, 5, 17, 10),
                                            end_date=datetime(2022, 3, 5, 18, 0),
                                            swimlane=2,
                                            client_type=Reservation.PRIVATE_CLIENT,
                                            price=19.9)
        cls.r7 = Reservation.objects.create(start_date=datetime(2022, 3, 5, 15, 0),
                                            end_date=datetime(2022, 3, 5, 18, 0),
                                            swimlane=1,
                                            client_type=Reservation.SWIM_SCHOOL,
                                            price=49.9)

    class MockConfig:
        name = 'Swimming pool management system'
        num_of_swimlanes = 3
        spots_per_swimlane = 5
        open_time_weekdays = time(9, 0)
        close_time_weekdays = time(16, 0)
        open_time_weekends = time(9, 0)
        close_time_weekends = time(18, 0)
        price_weekdays_private_clients = 7.99
        price_weekends_private_clients = 8.99
        price_weekdays_swim_schools = 34.99
        price_weekends_swim_schools = 39.99
        swim_schools_treshold = 0.35
        entry_at_opening_discount = 1


class ReservationTestCase(TestSetUp):
    def test_get_overlapping_reservations_long_period(self):
        date_from = datetime(2022, 1, 25, 9, 0)
        date_to = datetime(2022, 3, 5, 17, 10)
        overlapping_reservations = list(Reservation.get_overlapping_reservations(date_from,
                                                                                 date_to))

        self.assertEqual(len(overlapping_reservations), 5)
        self.assertEqual(overlapping_reservations[0], self.r3)
        self.assertEqual(overlapping_reservations[1], self.r4)
        self.assertEqual(overlapping_reservations[2], self.r5)
        self.assertEqual(overlapping_reservations[3], self.r6)
        self.assertEqual(overlapping_reservations[4], self.r7)

    def test_get_overlapping_reservations_single_point(self):
        date_from = datetime(2022, 2, 2, 15, 25)
        date_to = datetime(2022, 2, 2, 15, 25)
        overlapping_reservations = list(Reservation.get_overlapping_reservations(date_from,
                                                                                 date_to))

        self.assertEqual(len(overlapping_reservations), 2)
        self.assertEqual(overlapping_reservations[0], self.r4)
        self.assertEqual(overlapping_reservations[1], self.r5)

    def test_get_overlapping_reservations_empty(self):
        date_from = datetime(2022, 3, 5, 18, 11)
        date_to = datetime(2022, 3, 5, 19, 11)
        overlapping_reservations = list(Reservation.get_overlapping_reservations(date_from,
                                                                                 date_to))

        self.assertEqual(len(overlapping_reservations), 0)


class UtilsTestCase(TestSetUp):
    def test_is_weekday_weekday(self):
        self.assertIs(is_weekday(datetime(2021, 12, 20)), True)
        self.assertIs(is_weekday(datetime(2021, 12, 24)), True)

    def test_is_weekday_weekend(self):
        self.assertIs(is_weekday(datetime(2021, 12, 25)), False)
        self.assertIs(is_weekday(datetime(2021, 12, 26)), False)

    def test_facility_open_is_open(self):
        is_open = facility_open(self.config,
                                datetime(2021, 12, 20, 15, 30),
                                datetime(2021, 12, 20, 16, 0))
        self.assertIs(is_open, True)

    def test_facility_open_is_closed(self):
        is_open = facility_open(self.config,
                                datetime(2021, 12, 25, 10, 30),
                                datetime(2021, 12, 20, 18, 15))
        self.assertIs(is_open, False)

    def test_calculate_ticket_price_private_client(self):
        price = calculate_ticket_price(self.config,
                                       Reservation.PRIVATE_CLIENT,
                                       datetime(2021, 12, 20, 14, 0))
        self.assertEqual(price, 7.99)

    def test_calculate_ticket_price_swim_school(self):
        price = calculate_ticket_price(self.config,
                                       Reservation.SWIM_SCHOOL,
                                       datetime(2021, 12, 25, 12, 0))
        self.assertEqual(price, 39.99)

    def test_get_swimlines_info(self):
        date_from = datetime(2021, 12, 29, 11, 0)
        date_to = datetime(2022, 2, 2, 16, 45)
        overlapping_reservations = Reservation.get_overlapping_reservations(date_from,
                                                                            date_to)

        swimlines_info, lines_reserved_by_swim_schools = get_swimlines_info(
            self.config, overlapping_reservations
        )

        self.assertEqual(swimlines_info, {
            1: 0,
            2: 4,
            3: 0
        })
        self.assertEqual(lines_reserved_by_swim_schools, 2)

    def test_find_next_available_swimlane_private_client(self):
        date_from = datetime(2022, 1, 10, 16, 0)
        date_to = datetime(2022, 1, 10, 17, 0)
        swimline = find_next_available_swimlane(self.config, Reservation.PRIVATE_CLIENT,
                                                date_from, date_to)

        self.assertEqual(swimline, 2)

    def test_find_next_available_swimlane_swim_school(self):
        date_from = datetime(2022, 3, 5, 16, 10)
        date_to = datetime(2022, 3, 5, 18, 10)
        swimline = find_next_available_swimlane(self.config, Reservation.SWIM_SCHOOL,
                                                date_from, date_to)

        self.assertEqual(swimline, 3)

    def test_find_next_available_swimlane_swim_school_above_treshold(self):
        date_from = datetime(2022, 2, 2, 14, 0)
        date_to = datetime(2022, 3, 5, 15, 30)
        swimline = find_next_available_swimlane(self.config, Reservation.SWIM_SCHOOL,
                                                date_from, date_to)

        self.assertIs(swimline, None)

    def test_pay_for_reservation(self):
        obj_before_payment = Reservation.objects.get(pk=self.r1.id)
        self.assertIs(obj_before_payment.is_paid, False)

        pay_for_reservation(self.r1.id)

        obj_after_payment = Reservation.objects.get(pk=self.r1.id)
        self.assertIs(obj_after_payment.is_paid, True)

    def test_pay_for_reservation_invalid_id(self):
        with self.assertRaises(Reservation.DoesNotExist):
            pay_for_reservation("this_reservation_id_is_for_sure_invalid")

    def test_pay_for_reservation_already_paid(self):
        pay_for_reservation(self.r2.id)

        with self.assertRaises(ReservationAlreadyPaidForError):
            pay_for_reservation(self.r2.id)
