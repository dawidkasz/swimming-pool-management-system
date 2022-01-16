from datetime import datetime
from tickets.models import Reservation


def preprocess_income_data(year):
    """
    Returns a dict, which maps client types to arrays, that represent income
    in corresponding months, where January = array[0] etc.
    """

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
    """
    Returns a dict containg number of paid/unpaid reservations in corresponding months.
    """

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
    """
    Returns either year from the dictionary or the current year, if such key doesn't exist.
    """

    year = int(request_get.get("year", datetime.now().year))
    if year <= 0:
        raise ValueError("Year must be greater than 0.")

    return year


def generate_n_past_years(n):
    """
    Returns an array containg integers representing years
    from the current_one up to current_one - n + 1.
    """

    current_year = datetime.now().year
    return [year for year in reversed(range(current_year-n+1, current_year+1))]


def generate_report(report_date):
    """
    Generates a raport containg detailed information about reservations on a given day.
    """

    report = "reservation_id;client_type;income\n"
    total_income = 0
    paid_reservations = 0
    unpaid_reservations = 0
    private_clients = 0
    swim_schools = 0
    reservations = Reservation.objects.filter(start_date__year=report_date.year,
                                              start_date__month=report_date.month,
                                              start_date__day=report_date.day)

    for reservation in reservations:
        income = reservation.price if reservation.is_paid else 0
        report += f"{reservation.id};{reservation.client_type};{income}\n"
        total_income += income

        if reservation.is_paid:
            paid_reservations += 1
        else:
            unpaid_reservations += 1

        if reservation.client_type == Reservation.PRIVATE_CLIENT:
            private_clients += 1
        if reservation.client_type == Reservation.SWIM_SCHOOL:
            swim_schools += 1

    report = f"REPORT {report_date}\n" \
             f"=======================================\n" \
             f"Total income: {total_income}\n" \
             f"Amount of paid reservations: {paid_reservations}\n" \
             f"Amount of unpaid reservations: {unpaid_reservations}\n" \
             f"Private clients: {private_clients}\n" \
             f"Swim school clients: {swim_schools}\n\n" \
             f"{report}"

    return report
