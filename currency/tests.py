"""Test cases for Django API framework."""

from django.test import TestCase

from currency.models import Currency


class TestAPI(TestCase):
    """Ninja API testing methods."""

    @classmethod
    def setUpClass(cls):
        """Setup class."""
        super().setUpClass()
        Currency.objects.create(
            id=1,
            code="EUR",
            name="Euro",
            image="default_image.jpg",
        )

    @classmethod
    def tearDownClass(cls):
        """Tear down class."""
        print("tearDownClass")

    def setUp(self):
        """Set up method."""
        print("SetUp")

    def tearDown(self):
        """Tear down method."""
        print("TearDown")

    def test_server_status(self):
        """Test server status response."""
        response = self.client.get(path="/api/")
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            raw=response.content, expected_data={"Server": "running..."}
        )

    def test_get_single_currency(self):
        """Test GET single currency."""
        response = self.client.get(path="/api/currencies/1")
        content = {
            "id": 1,
            "code": "EUR",
            "name": "Euro",
            "image": "/media/default_image.jpg",
        }
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(raw=response.content, expected_data=content)
