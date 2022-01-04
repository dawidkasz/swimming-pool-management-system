import datetime
from .models import Reservation


def is_weekday(date):
    return 0 <= date.weekday() <= 4


def facility_open(config, start_date, end_date):
    start_time = datetime.time(hour=start_date.hour, minute=start_date.minute)
    end_time = datetime.time(hour=end_date.hour, minute=end_date.minute)

    if is_weekday(start_date):
        start_date_valid = config.open_time_weekdays <= start_time <= config.close_time_weekdays
        end_date_valid = config.open_time_weekdays <= end_time <= config.close_time_weekdays
    else:
        start_date_valid = config.open_time_weekends <= start_time <= config.close_time_weekends
        end_date_valid = config.open_time_weekends <= end_time <= config.close_time_weekends

    return start_date_valid and end_date_valid


def calculate_ticket_price(config, client_type, reservation_date):
    weekday = is_weekday(reservation_date)

    if client_type == Reservation.PRIVATE_CLIENT:
        return config.price_weekdays_private_clients if weekday \
            else config.price_weekends_private_clients

    if client_type == Reservation.SWIM_SCHOOL:
        return config.price_weekdays_swim_schools if weekday \
            else config.price_weekends_swim_schools


def get_swimlines_info(config, reservations):
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
    overlapping_reservations = Reservation.get_overlapping_reservations(date_from, date_to)

    swimlines_info, lines_reserved_by_swim_schools = get_swimlines_info(config,
                                                                        overlapping_reservations)

    if client_type == Reservation.SWIM_SCHOOL and \
            lines_reserved_by_swim_schools / config.num_of_swimlanes > config.swim_schools_treshold:
        return

    for swimlane, free_spots in swimlines_info.items():
        if (client_type == Reservation.SWIM_SCHOOL and free_spots == config.spots_per_swimlane) or\
                (client_type == Reservation.PRIVATE_CLIENT and free_spots > 0):
            return swimlane