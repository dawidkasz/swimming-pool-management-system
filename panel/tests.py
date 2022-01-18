from django.test import TestCase
from .utils import get_config
from .models import SiteConfiguration


class TestUtils(TestCase):
    def test_get_config(self):
        config = get_config()
        self.assertIs(isinstance(config, SiteConfiguration), True)
        self.assertEqual(config.name, "Swimming pool management system")
