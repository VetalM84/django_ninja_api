"""Test cases for Django API framework."""

from django.test import TestCase


class TestAPI(TestCase):

    def setUp(self):
        """Set up method."""
        print("SetUp")

    def tearDown(self):
        """Tear down method."""
        print("TearDown")

    def test_server_status(self):
        response = self.client.get(path="/api/")
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"Server": "running..."})
