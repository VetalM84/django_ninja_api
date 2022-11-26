"""Test cases for Django API framework."""

from django.test import TestCase

from currency.models import Currency


class TestAPI(TestCase):
    """Ninja API testing methods."""

    @classmethod
    def setUpClass(cls):
        """Setup class."""
        super().setUpClass()
        currency_data = [
            {
                "id": 1,
                "code": "EUR",
                "name": "Euro",
                "image": "eur.jpg",
            },
            {
                "id": 2,
                "code": "USD",
                "name": "US Dollar",
                "image": "usd.jpg",
            },
        ]
        currency_list = [Currency(**data_dict) for data_dict in currency_data]
        Currency.objects.bulk_create(currency_list)

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
            "image": "/media/eur.jpg",
        }
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(raw=response.content, expected_data=content)

    def test_get_all_currencies(self):
        """Test GET all currencies."""
        response = self.client.get(path="/api/currencies")
        self.assertEqual(response.status_code, 200)

    def test_add_new_currency(self):
        """Test POST new currency."""
        data = {
            "code": "UAH",
            "name": "Hryvna",
            "image": "/uah.jpg",
        }
        response = self.client.post(
            path="/api/currencies", data=data, content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)

    def test_add_existing_currency(self):
        """Test POST existing currency."""
        data = {
            "code": "USD",
            "name": "Hryvna",
            "image": "/uah.jpg",
        }
        response = self.client.post(
            path="/api/currencies", data=data, content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)

    def test_edit_currency(self):
        """Test PUT currency."""
        data = {
            "code": "UAH",
            "name": "Hryvna",
            "image": "/uah.jpg",
        }
        response = self.client.put(
            path="/api/currencies/1", data=data, content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)

    def test_edit_currency_fail(self):
        """Test PUT currency fail."""
        data = {
            "code": "UAH",
            "name": "Hryvna",
            "image": "/uah.jpg",
        }
        response = self.client.put(
            path="/api/currencies/111", data=data, content_type="application/json"
        )
        self.assertEqual(response.status_code, 404)

    def test_delete_currency(self):
        """Test DELETE currency."""
        response = self.client.delete(path="/api/currencies/1")
        self.assertEqual(response.status_code, 204)

    def test_delete_currency_fail(self):
        """Test DELETE currency fail."""
        response = self.client.delete(path="/api/currencies/111")
        self.assertEqual(response.status_code, 404)
