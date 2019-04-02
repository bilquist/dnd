# initiative/test.py

from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest

from initiative.views import home_page



# Create your tests here.
class HomePageTest(TestCase):

	def test_home_page_returns_correct_html(self):
		response = self.client.get('/')
		self.assertTemplateUsed(response, 'initiative/home.html')
	
	def test_can_save_a_POST_request(self):
		response = self.client.post('/', data={'participant_text': 'A new participant'})
		self.assertIn('A new participant', response.content.decode())
		self.assertTemplateUsed(response, 'initiative/home.html')