import datetime
from .models import Reservation
from .exceptions import ReservationAlreadyPaidForError


def is_weekday(date):
    """
    Returns True if the given date is weekday, False otherwise.
    """

    return 0 <= date.weekday() <= 4


def facility_open(config, start_date, end_date):
    """
    Returns True if the facility is open during provided
    start_date and end_date, False otherwise.
    """

    start_time = datetime.time(hour=start_date.hour, minute=start_date.minute)
    end_time = datetime.time(hour=end_date.hour, minute=end_date.minute)

    if is_weekday(start_date):
        start_date_valid = config.open_time_weekdays <= start_time <= config.close_time_weekdays
        end_date_valid = config.open_time_weekdays <= end_time <= config.close_time_weekdays
    else:
        start_date_valid = config.open_time_weekends <= start_time <= config.close_time_weekends
        end_date_valid = config.open_time_weekends <= end_time <= config.close_time_weekends

    return start_date_valid and end_date_valid


def calculate_ticket_price(config, client_type, start_date, end_date):
    """
    Calculates adequate ticket price based on provided client_type and reservation_date.
    """

    duration = (end_date - start_date)
    duration_hours = duration.seconds // 3600
    weekday = is_weekday(start_date)

    if client_type == Reservation.PRIVATE_CLIENT:
        price = config.price_weekdays_private_clients if weekday \
            else config.price_weekends_private_clients

    if client_type == Reservation.SWIM_SCHOOL:
        price = config.price_weekdays_swim_schools if weekday \
            else config.price_weekends_swim_schools

    return price * duration_hours


def get_swimlanes_info(config, reservations):
    """
    Given a collection of reservations returns a tuple containing a dictionary
    of swimlanes with the corresponding free spots and total number of lines, which
    are taken by swim schools.
    """

    num_of_lines_reserved_by_swim_schools = 0
    free_spots_on_swimlanes = {idx: config.spots_per_swimlane
                               for idx in range(1, config.num_of_swimlanes + 1)}

    for reservation in reservations:
        if reservation.client_type == Reservation.SWIM_SCHOOL:
            free_spots_on_swimlanes[reservation.swimlane] = 0
            num_of_lines_reserved_by_swim_schools += 1
        else:
            free_spots_on_swimlanes[reservation.swimlane] = max(
                free_spots_on_swimlanes[reservation.swimlane]-1, 0)

    return free_spots_on_swimlanes, num_of_lines_reserved_by_swim_schools


def find_next_available_swimlane(config, client_type, date_from, date_to):
    """
    Finds id of the next available swimlane.
    If there is no available swimlane during provided reservation time returns None.
    """

    overlapping_reservations = Reservation.get_overlapping_reservations(date_from, date_to)

    swimlanes_info, lines_reserved_by_swim_schools = get_swimlanes_info(config,
                                                                        overlapping_reservations)

    if client_type == Reservation.SWIM_SCHOOL and \
            lines_reserved_by_swim_schools / config.num_of_swimlanes > config.swim_schools_treshold:
        return

    for swimlane, free_spots in swimlanes_info.items():
        if (client_type == Reservation.SWIM_SCHOOL and free_spots == config.spots_per_swimlane) or\
                (client_type == Reservation.PRIVATE_CLIENT and free_spots > 0):
            return swimlane


def pay_for_reservation(reservation_id):
    """
    Given reservation_id marks corresponding Reservation as paid.
    Raises an error if reservation with such id doesn't exist or if it is already paid.
    """

    reservation = Reservation.objects.get(pk=reservation_id)

    if reservation.is_paid:
        raise ReservationAlreadyPaidForError("You have already paid for this reservation.")

    reservation.is_paid = True
    reservation.save()


def find_next_free_term(config, client_type, date_from, duration, max_future_days=90):
    """
    Finds the next free reservation term, starting from the given date. Only considers
    full hours e.g.
    """

    duration_timedelta = datetime.timedelta(hours=duration)
    date_from_timedelta = datetime.timedelta(hours=1)
    _date_from = datetime.datetime(year=date_from.year, month=date_from.month,
                                   day=date_from.day, hour=date_from.hour)

    while abs(_date_from - date_from) < datetime.timedelta(days=max_future_days):
        _date_to = _date_from + duration_timedelta
        if not facility_open(config, _date_from, _date_to):
            _date_from += date_from_timedelta
            continue

        if find_next_available_swimlane(config, client_type, _date_from, _date_to):
            return (_date_from, _date_to)

        _date_from += date_from_timedelta
