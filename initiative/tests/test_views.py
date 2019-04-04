# initiative/test.py

from django.http import HttpRequest
from django.test import TestCase
from django.urls import resolve
from django.utils.html import escape
from initiative.forms import ParticipantForm
from initiative.models import Initiative, Participant
from initiative.views import home_page



# Create your tests here.
class HomePageTest(TestCase):

	def test_home_page_returns_correct_html(self):
		response = self.client.get('/')
		self.assertTemplateUsed(response, 'initiative/home.html')
	
	def test_home_page_uses_participant_form(self):
		response = self.client.get('/')
		self.assertIsInstance(response.context['form'], ParticipantForm)


class InitiativeViewTest(TestCase):
	
	def test_uses_initiative_template(self):
		initiative = Initiative.objects.create()
		response = self.client.get(f'/initiative/{initiative.id}/')
		self.assertTemplateUsed(response, 'initiative/initiative.html')
	
	def test_displays_only_participants_for_that_initiative(self):
		correct_initiative = Initiative.objects.create()
		Participant.objects.create(name='Player 1', initiative=correct_initiative)
		Participant.objects.create(name='Player 2', initiative=correct_initiative)
		
		other_initiative = Initiative.objects.create()
		Participant.objects.create(name='Ghost 1', initiative=other_initiative)
		Participant.objects.create(name='Ghost 2', initiative=other_initiative)
		
		response = self.client.get(f'/initiative/{correct_initiative.id}/')
		
		self.assertTemplateUsed(response, 'initiative/initiative.html')
		self.assertContains(response, 'Player 1')
		self.assertContains(response, 'Player 2')
		self.assertNotContains(response, 'Ghost 1')
		self.assertNotContains(response, 'Ghost 2')
	
	def test_passes_correct_initiative_to_template(self):
		other_initiative = Initiative.objects.create()
		correct_initiative = Initiative.objects.create()
		response = self.client.get(f'/initiative/{correct_initiative.id}/')
		self.assertTemplateUsed(response, 'initiative/initiative.html')
		self.assertEqual(response.context['initiative'], correct_initiative)
	
	def test_can_save_a_POST_request_to_an_existing_initiative(self):
		other_initiative = Initiative.objects.create()
		correct_initiative = Initiative.objects.create()
		
		self.client.post(
			f'/initiative/{correct_initiative.id}/',
			data={'participant_text': 'James Ihara'}
		)
		
		self.assertEqual(Participant.objects.count(), 1)
		new_participant = Participant.objects.first()
		self.assertEqual(new_participant.name, 'James Ihara')
		self.assertEqual(new_participant.initiative, correct_initiative)
		
	def test_POST_redirects_to_initiative_view(self):
		other_initiative = Initiative.objects.create()
		correct_initiative = Initiative.objects.create()
		
		response = self.client.post(
			f'/initiative/{correct_initiative.id}/',
			data={'participant_text': 'James Ihara'}
		)
		
		self.assertRedirects(response, f'/initiative/{correct_initiative.id}/')
	
	def test_validation_errors_end_up_on_initiative_page(self):
		initiative = Initiative.objects.create()
		response = self.client.post(
			f'/initiative/{initiative.id}/',
			data={'participant_text': ''}
		)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'initiative/initiative.html')
		expected_error = escape("You can't have an empty initiative participant!")
		self.assertContains(response, expected_error)
		
		
class NewInitiativeTest(TestCase):
	
	def test_validation_errors_are_sent_back_to_home_page_template(self):
		response = self.client.post('/initiative/new', data={'participant_text': ''})
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'initiative/home.html')
		expected_error = escape("You can't have an empty initiative participant!")
		self.assertContains(response, expected_error)
	
	def test_invalid_initiative_participants_arent_saved(self):
		self.client.post('/initiative/new', data={'participant_text': ''})
		self.assertEqual(Initiative.objects.count(), 0)
		self.assertEqual(Participant.objects.count(), 0)
		
		
		