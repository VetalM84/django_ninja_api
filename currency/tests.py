"""Test cases for Django API framework."""

from django.contrib.auth.models import User
from django.test import TestCase

from currency import api
from currency.models import Currency, Deal, Offer


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
            {
                "id": 3,
                "code": "CAD",
                "name": "Canadian Dollar",
                "image": "cad.jpg",
            },
        ]
        currency_list = [Currency(**data_dict) for data_dict in currency_data]
        Currency.objects.bulk_create(currency_list)
        User.objects.create_user(
            username="TestUserName",
            email="test@test.com",
            password="test",
            first_name="TestFirstName",
            last_name="TestLastName",
        )
        User.objects.create_user(
            username="TestUserName2",
            email="test2@test.com",
            password="test2",
            first_name="TestFirstName2",
            last_name="TestLastName2",
        )
        Offer.objects.create(
            id=1,
            currency_to_sell_id=1,
            currency_to_buy_id=2,
            amount=1000,
            exchange_rate=9,
            seller_id=1,
        )
        Offer.objects.create(
            id=2,
            currency_to_sell_id=1,
            currency_to_buy_id=2,
            amount=1000,
            exchange_rate=9,
            seller_id=1,
        )
        Deal.objects.create(
            id=1,
            buyer_id=2,
            offer_id=1,
            amount=100,
        )
        cls.token = api.create_token("TestUserName")

    @classmethod
    def tearDownClass(cls):
        """Tear down class."""
        print("tearDownClass")

    def setUp(self):
        """Set up method."""
        self.headers = {"HTTP_AUTHORIZATION": f"Bearer {self.token}"}
        print("SetUp")

    def tearDown(self):
        """Tear down method."""
        print("TearDown")

    def test_create_token(self):
        """Test create token method."""
        token = api.create_token("TestUserName")
        self.assertTrue(token, str)

    def test_sign_in(self):
        """Test Sing in."""
        data = {"username": "TestUserName", "password": "test"}
        response = self.client.post(path="/api/sign_in", data=data)
        # or like this
        # data=f"username=TestUserName&password=test"
        # content_type="application/x-www-form-urlencoded"
        self.assertEqual(response.status_code, 200)

    def test_sign_in_404_422(self):
        """Test Sing in fails."""
        data = {"username": "TestUser404", "password": "test"}
        response = self.client.post(path="/api/sign_in", data=data)
        self.assertEqual(response.status_code, 404)

        data = {"username": "TestUserName", "password": "wrong"}
        response = self.client.post(path="/api/sign_in", data=data)
        self.assertEqual(response.status_code, 422)

    def test_sign_up(self):
        """Test Sing up."""
        data = {"username": "NewTestUserName", "password": "newtest"}
        response = self.client.post(path="/api/sign_up", data=data)
        self.assertEqual(response.status_code, 201)

    def test_sign_up_422(self):
        """Test Sing up fails."""
        data = {"username": "TestUserName", "password": "test"}
        response = self.client.post(path="/api/sign_up", data=data)
        self.assertEqual(response.status_code, 422)

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
        self.assertEqual(response.status_code, 200)

    def test_get_all_currencies(self):
        """Test GET all currencies."""
        response = self.client.get(path="/api/currencies?limit=100&offset=0")
        self.assertEqual(response.status_code, 200)

    def test_add_new_currency(self):
        """Test POST new currency."""
        data = {
            "code": "UAH",
            "name": "Hryvna",
            "image": "/uah.jpg",
        }
        response = self.client.post(
            path="/api/currencies",
            data=data,
            content_type="application/json",
            **{"HTTP_AUTHORIZATION": f"Bearer {self.token}"},
            follow=True,
        )
        self.assertEqual(response.status_code, 201)

    def test_add_currency_400(self):
        """Test POST existing currency."""
        data = {
            "code": "USD",
            "name": "Hryvna",
            "image": "/uah.jpg",
        }
        response = self.client.post(
            path="/api/currencies",
            data=data,
            content_type="application/json",
            **{"HTTP_AUTHORIZATION": f"Bearer {self.token}"},
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
            path="/api/currencies/1",
            data=data,
            content_type="application/json",
            **{"HTTP_AUTHORIZATION": f"Bearer {self.token}"},
        )
        self.assertEqual(response.status_code, 200)

    def test_edit_currency_404(self):
        """Test PUT currency fail."""
        data = {
            "code": "UAH",
            "name": "Hryvna",
            "image": "/uah.jpg",
        }
        response = self.client.put(
            path="/api/currencies/111",
            data=data,
            content_type="application/json",
            **{"HTTP_AUTHORIZATION": f"Bearer {self.token}"},
        )
        self.assertEqual(response.status_code, 404)

    def test_delete_currency(self):
        """Test DELETE currency."""
        response = self.client.delete(
            path="/api/currencies/3", **{"HTTP_AUTHORIZATION": f"Bearer {self.token}"}
        )
        self.assertEqual(response.status_code, 204)

    def test_delete_currency_404_400(self):
        """Test DELETE currency fail."""
        response = self.client.delete(
            path="/api/currencies/111", **{"HTTP_AUTHORIZATION": f"Bearer {self.token}"}
        )
        self.assertEqual(response.status_code, 404)

        response = self.client.delete(
            path="/api/currencies/1", **{"HTTP_AUTHORIZATION": f"Bearer {self.token}"}
        )
        self.assertEqual(response.status_code, 400)

    def test_get_single_offer(self):
        """Test GET single offer."""
        response = self.client.get(path="/api/offers/1")
        self.assertContains(response=response, text="seller_id")

    def test_get_single_offer_404(self):
        """Test GET single offer fail."""
        response = self.client.get(path="/api/offers/111")
        self.assertEqual(response.status_code, 404)

    def test_get_all_active_offers(self):
        """Test GET all active offers."""
        response = self.client.get(path="/api/offers?limit=100&offset=0")
        self.assertEqual(response.status_code, 200)

    def test_get_user_offers(self):
        """Test GET all user offers."""
        response = self.client.get(
            path="/api/users/1/offers?limit=100&offset=0",
            **{"HTTP_AUTHORIZATION": f"Bearer {self.token}"},
        )
        self.assertContains(response=response, text='"active_state": true')

    def test_get_all_offers_by_sell_currency(self):
        """Test GET all offers by sell currency with pagination."""
        response = self.client.get(path="/api/currencies/1/offers?limit=100&offset=0")
        self.assertContains(response=response, text='"currency_to_sell_id": 1')

    def test_add_new_offer(self):
        """Test POST new offer."""
        data = {
            "currency_to_sell_id": 1,
            "currency_to_buy_id": 2,
            "amount": 100.25,
            "exchange_rate": 10.44,
            "seller_id": 2,
        }
        response = self.client.post(
            path="/api/offers",
            data=data,
            content_type="application/json",
            **{"HTTP_AUTHORIZATION": f"Bearer {self.token}"},
        )
        self.assertEqual(response.status_code, 201)

    def test_toggle_offer_state(self):
        """Test toggle offer state (enable/disable)."""
        data = {"active_state": False}
        response = self.client.patch(
            path="/api/offers/1",
            data=data,
            content_type="application/json",
            **{"HTTP_AUTHORIZATION": f"Bearer {self.token}"},
        )
        self.assertEqual(response.status_code, 200)

    def test_toggle_offer_state_404(self):
        """Test toggle offer state (enable/disable) fails."""
        data = {"active_state": True}
        response = self.client.patch(
            path="/api/offers/1111",
            data=data,
            content_type="application/json",
            **{"HTTP_AUTHORIZATION": f"Bearer {self.token}"},
        )
        self.assertEqual(response.status_code, 404)

    def test_delete_offer(self):
        """Test DELETE offer."""
        response = self.client.delete(
            path="/api/offers/2", **{"HTTP_AUTHORIZATION": f"Bearer {self.token}"}
        )
        self.assertEqual(response.status_code, 204)

    def test_delete_offer_404_400(self):
        """Test DELETE offer fails."""
        response = self.client.delete(
            path="/api/offers/111", **{"HTTP_AUTHORIZATION": f"Bearer {self.token}"}
        )
        self.assertEqual(response.status_code, 404)

        response = self.client.delete(
            path="/api/offers/1", **{"HTTP_AUTHORIZATION": f"Bearer {self.token}"}
        )
        self.assertEqual(response.status_code, 400)

    def test_get_user_info(self):
        """Test GET user profile information with offers and deals."""
        response = self.client.get(
            path="/api/users/1", **{"HTTP_AUTHORIZATION": f"Bearer {self.token}"}
        )
        self.assertContains(response=response, text="offers")
        self.assertContains(response=response, text="deal")

    def test_get_single_deal(self):
        """Test GET single deal."""
        response = self.client.get(path="/api/deals/1")
        self.assertContains(response=response, text="offer")

    def test_get_single_deal_404(self):
        """Test GET single deal fail."""
        response = self.client.get(path="/api/deals/111")
        self.assertEqual(response.status_code, 404)

    def test_get_all_deals(self):
        """Test GET all deals for corresponding offer."""
        response = self.client.get(path="/api/deals/1/offer?limit=100&offset=0")
        self.assertEqual(response.status_code, 200)

    def test_add_new_deal(self):
        """Test POST new deal."""
        data = {
            "buyer_id": 2,
            "offer_id": 2,
            "amount": 100,
        }
        response = self.client.post(
            path="/api/deals",
            data=data,
            content_type="application/json",
            **{"HTTP_AUTHORIZATION": f"Bearer {self.token}"},
        )
        self.assertEqual(response.status_code, 201)

    def test_add_new_deal_404_400(self):
        """Test POST new deal."""
        response = self.client.post(
            path="/api/deals",
            data={"buyer_id": 2, "offer_id": 55, "amount": 100},
            content_type="application/json",
            **{"HTTP_AUTHORIZATION": f"Bearer {self.token}"},
        )
        self.assertEqual(response.status_code, 404)

        # test user can not buy own offer
        response = self.client.post(
            path="/api/deals",
            data={"buyer_id": 1, "offer_id": 1, "amount": 100},
            content_type="application/json",
            **{"HTTP_AUTHORIZATION": f"Bearer {self.token}"},
        )
        self.assertEqual(response.status_code, 400)

        # test user can not order more than offer has
        response = self.client.post(
            path="/api/deals",
            data={"buyer_id": 1, "offer_id": 1, "amount": 100000},
            content_type="application/json",
            **{"HTTP_AUTHORIZATION": f"Bearer {self.token}"},
        )
        self.assertEqual(response.status_code, 400)
