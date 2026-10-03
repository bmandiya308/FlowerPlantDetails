import os
import re
import tempfile
import unittest
from io import BytesIO

from app import FLOWERS, app


class FlowerAppTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        app.config["DATABASE"] = os.path.join(self.temp_dir.name, "test.sqlite3")
        app.config["UPLOAD_FOLDER"] = os.path.join(self.temp_dir.name, "uploads")
        self.client = app.test_client()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_homepage_shows_community_feed_and_composer(self):
        response = self.client.get("/")
        page = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn("Garden stories", page)
        self.assertIn('action="/posts"', page)
        self.assertIn("Maya Chen", page)

    def test_flower_collection_lists_every_flower(self):
        response = self.client.get("/flowers")
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

    def test_image_upload_is_saved_and_shown_in_feed(self):
        response = self.client.post(
            "/posts",
            data={
                "author": "Garden Tester",
                "caption": "The first tomato is finally here.",
                "media": (BytesIO(b"test image bytes"), "tomato.jpg", "image/jpeg"),
            },
            content_type="multipart/form-data",
            follow_redirects=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("The first tomato is finally here.", response.get_data(as_text=True))
        uploaded_name = os.listdir(app.config["UPLOAD_FOLDER"])[0]
        with self.client.get(f"/uploads/{uploaded_name}") as uploaded_response:
            self.assertEqual(uploaded_response.data, b"test image bytes")

    def test_video_upload_renders_video_player(self):
        response = self.client.post(
            "/posts",
            data={
                "author": "Garden Tester",
                "caption": "A quick garden tour.",
                "media": (BytesIO(b"test video bytes"), "tour.mp4", "video/mp4"),
            },
            content_type="multipart/form-data",
            follow_redirects=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("<video", response.get_data(as_text=True))

    def test_unsupported_upload_is_rejected(self):
        response = self.client.post(
            "/posts",
            data={
                "author": "Garden Tester",
                "media": (BytesIO(b"not a photo"), "notes.exe", "application/octet-stream"),
            },
            content_type="multipart/form-data",
            follow_redirects=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("Use a JPG, PNG", response.get_data(as_text=True))
        self.assertFalse(os.path.exists(app.config["UPLOAD_FOLDER"]))


if __name__ == "__main__":
    unittest.main()