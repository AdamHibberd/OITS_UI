from django.test import TestCase, Client, override_settings
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
media_root = os.path.join(BASE_DIR, 'results_viewer/test_files')


@override_settings(MEDIA_ROOT = media_root)
class ViewsTestCase(TestCase):

    def setUp(self):
        pass


    def test_get_csv(self):

        client = Client()
        response = client.get('/results/4b8e997c-0ce5-45d8-87fb-0f314505754a/paths/')

        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'PROBE\n7.0739567e+08,-0.32819958,-0.95950251,4.9871959e-05' in response.content)
