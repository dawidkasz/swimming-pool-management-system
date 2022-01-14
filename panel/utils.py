from .models import SiteConfiguration


def get_config() -> SiteConfiguration:
    """
    Returns SiteConfiguration singleton from the database.
    """

    return SiteConfiguration.get_solo()
