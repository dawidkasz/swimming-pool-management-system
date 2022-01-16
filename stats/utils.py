from datetime import datetime
from tickets.models import Reservation


def preprocess_income_data(year):
    income_data = {
        "private_clients": [0 for _ in range(12)],
        "swim_schools": [0 for _ in range(12)],
    }

    reservations = Reservation.objects.filter(start_date__year=year)

    for reservation in reservations:
        if not reservation.is_paid:
            continue

        reservation_month = reservation.start_date.month - 1
        reservation_income = reservation.price

        if reservation.client_type == Reservation.PRIVATE_CLIENT:
            income_data["private_clients"][reservation_month] += reservation_income
        if reservation.client_type == Reservation.SWIM_SCHOOL:
            income_data["swim_schools"][reservation_month] += reservation_income

    return income_data


def preprocess_reservations_data(year):
    reservations_data = {
        "paid_reservations": [0 for _ in range(12)],
        "unpaid_reservations": [0 for _ in range(12)],
    }

    reservations = Reservation.objects.filter(start_date__year=year)

    for reservation in reservations:
        reservation_month = reservation.start_date.month - 1
        data_key = "paid_reservations" if reservation.is_paid else "unpaid_reservations"

        reservations_data[data_key][reservation_month] += 1

    return reservations_data


def get_year_or_current(request_get):
    year = int(request_get.get("year", datetime.now().year))

    if year <= 0:
        raise ValueError("Year must be greater than 0.")

    return year


def generate_n_past_years(n):
    current_year = datetime.now().year
    return [year for year in reversed(range(current_year-n+1, current_year+1))]
