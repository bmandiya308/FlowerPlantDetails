import unittest

from app import FLOWERS, app


class FlowerAppTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_homepage_lists_every_flower(self):
        response = self.client.get("/")
        page = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        for flower in FLOWERS:
            self.assertIn(flower["name"], page)

    def test_every_flower_has_a_detail_page(self):
        for flower in FLOWERS:
            response = self.client.get(f"/flower/{flower['slug']}")
            self.assertEqual(response.status_code, 200)
            self.assertIn(flower["name"], response.get_data(as_text=True))

    def test_unknown_flower_returns_not_found(self):
        self.assertEqual(self.client.get("/flower/not-a-flower").status_code, 404)


if __name__ == "__main__":
    unittest.main()