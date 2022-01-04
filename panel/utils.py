from .models import SiteConfiguration


def get_config() -> SiteConfiguration:
    return SiteConfiguration.get_solo()
