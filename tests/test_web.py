import unittest

from .context import app


class WebTest(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()


class IndexTests(WebTest):
    def test_index(self):
        response = self.app.get('/')
        self.assertEqual("200 OK", response.status)


class ClientTests(WebTest):
    def test_client(self):
        response = self.app.get('/client')
        self.assertEqual("200 OK", response.status)
