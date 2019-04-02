# initiative/test.py

from django.urls import resolve
from django.test import TestCase
from initiative.views import home_page



# Create your tests here.
class HomePageTest(TestCase):

	def test_rool_url_resolves_to_home_page_view(self):
		found = resolve('/')
		self.assertEqual(found.func, home_page)