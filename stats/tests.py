from datetime import datetime, date
from django.test import TestCase
from tickets.models import Reservation
from .utils import (preprocess_income_data, preprocess_reservations_data,
                    get_year_or_current, generate_n_past_years, generate_report)


class TestSetUp(TestCase):
    @classmethod
    def setUp(cls):
        cls.r1 = Reservation.objects.create(start_date=datetime(2021, 10, 20, 10, 30),
                                            end_date=datetime(2021, 10, 20, 11, 30),
                                            swimlane=2,
                                            client_type=Reservation.PRIVATE_CLIENT,
                                            is_paid=True,
                                            price=10)
        cls.r2 = Reservation.objects.create(start_date=datetime(2021, 12, 13, 14, 45),
                                            end_date=datetime(2022, 12, 13, 16, 30),
                                            swimlane=1,
                                            client_type=Reservation.SWIM_SCHOOL,
                                            is_paid=True,
                                            price=8)
        cls.r3 = Reservation.objects.create(start_date=datetime(2022, 1, 25, 8, 0),
                                            end_date=datetime(2022, 1, 25, 10, 30),
                                            swimlane=1,
                                            client_type=Reservation.PRIVATE_CLIENT,
                                            is_paid=True,
                                            price=13),
        cls.r4 = Reservation.objects.create(start_date=datetime(2022, 2, 1, 8, 0),
                                            end_date=datetime(2022, 2, 1, 10, 0),
                                            swimlane=1,
                                            client_type=Reservation.PRIVATE_CLIENT,
                                            is_paid=False,
                                            price=17)
        cls.r5 = Reservation.objects.create(start_date=datetime(2022, 2, 2, 15, 25),
                                            end_date=datetime(2022, 2, 2, 16, 25),
                                            swimlane=1,
                                            client_type=Reservation.PRIVATE_CLIENT,
                                            is_paid=True,
                                            price=7)
        cls.r6 = Reservation.objects.create(start_date=datetime(2022, 2, 2, 15, 0),
                                            end_date=datetime(2022, 2, 2, 17, 0),
                                            swimlane=3,
                                            client_type=Reservation.SWIM_SCHOOL,
                                            is_paid=True,
                                            price=25)
        cls.r7 = Reservation.objects.create(start_date=datetime(2022, 2, 24, 10, 25),
                                            end_date=datetime(2022, 2, 24, 14, 25),
                                            swimlane=1,
                                            client_type=Reservation.PRIVATE_CLIENT,
                                            is_paid=True,
                                            price=9)
        cls.r8 = Reservation.objects.create(start_date=datetime(2022, 12, 5, 10, 0),
                                            end_date=datetime(2022, 12, 5, 13, 0),
                                            swimlane=1,
                                            client_type=Reservation.SWIM_SCHOOL,
                                            is_paid=True,
                                            price=11)
        cls.r9 = Reservation.objects.create(start_date=datetime(2022, 2, 2, 8, 0),
                                            end_date=datetime(2022, 2, 2, 10, 0),
                                            swimlane=4,
                                            client_type=Reservation.SWIM_SCHOOL,
                                            is_paid=False,
                                            price=11)


class UtilsTestCase(TestSetUp):
    def test_preprocess_income_data(self):
        expected_output = {
            "private_clients": [13, 16, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            "swim_schools": [0, 25, 0, 0, 0, 0, 0, 0, 0, 0, 0, 11]
        }

        self.assertEqual(preprocess_income_data(2022), expected_output)

    def test_preprocess_income_data_empty(self):
        expected_output = {
            "private_clients": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            "swim_schools": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        }

        self.assertEqual(preprocess_income_data(1110), expected_output)

    def test_preprocess_reservations_data(self):
        expected_output = {
            "paid_reservations": [1, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            "unpaid_reservations": [0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        }

        self.assertEqual(preprocess_reservations_data(2022), expected_output)

    def test_preprocess_reservations_data_empty(self):
        self.maxDiff = None
        expected_output = {
            "paid_reservations": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            "unpaid_reservations": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        }

        self.assertEqual(preprocess_reservations_data(1110), expected_output)

    def test_get_year_or_current(self):
        self.assertEqual(get_year_or_current({"year": 2019}), 2019)

    def test_get_year_or_current_empty(self):
        self.assertEqual(get_year_or_current({}), datetime.now().year)

    def test_generate_n_past_years(self):
        current_year = datetime.now().year
        expected_output = [current_year, current_year-1, current_year-2, current_year-3]

        self.assertEqual(generate_n_past_years(4), expected_output)

    def test_generate_report(self):
        report = f"REPORT 2022-02-02\n" \
             f"=======================================\n" \
             f"Total income: 32.00\n" \
             f"Amount of paid reservations: 2\n" \
             f"Amount of unpaid reservations: 1\n" \
             f"Private clients: 1\n" \
             f"Swim school clients: 2\n\n" \
             f"reservation_id;client_type;income\n" \
             f"{self.r5.id};private_client;7.00\n" \
             f"{self.r6.id};swim_school;25.00\n"\
             f"{self.r9.id};swim_school;0\n"

        self.assertEqual(generate_report(date(2022, 2, 2)), report)