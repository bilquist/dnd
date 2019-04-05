# initiative/test.py

from django.http import HttpRequest
from django.test import TestCase
from django.urls import resolve
from django.utils.html import escape
from initiative.forms import (
	DUPLICATE_PARTICIPANT_ERROR, EMPTY_PARTICIPANT_ERROR,
	ExistingInitiativeParticipantForm, ParticipantForm
)
from initiative.models import Initiative, Participant
from initiative.views import home_page
from unittest import skip



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
			data={'name': 'James Ihara'}
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
			data={'name': 'James Ihara'}
		)
		
		self.assertRedirects(response, f'/initiative/{correct_initiative.id}/')
		
	def post_invalid_input(self):
		initiative = Initiative.objects.create()
		return self.client.post(
			f'/initiative/{initiative.id}/',
			data={'name': ''}
		)
	
	def test_for_invalid_input_nothing_saved_to_db(self):
		self.post_invalid_input()
		self.assertEqual(Participant.objects.count(), 0)
	
	def test_for_invalid_input_renders_initiative_template(self):
		response = self.post_invalid_input()
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'initiative/initiative.html')
	
	def test_for_invalid_input_passes_form_to_template(self):
		response = self.post_invalid_input()
		self.assertIsInstance(response.context['form'], ExistingInitiativeParticipantForm)
	
	def test_for_invalid_input_shows_error_on_page(self):
		response = self.post_invalid_input()
		self.assertContains(response, escape(EMPTY_PARTICIPANT_ERROR))
		
	def test_displays_participant_form(self):
		initiative = Initiative.objects.create()
		response = self.client.get(f'/initiative/{initiative.id}/')
		self.assertIsInstance(response.context['form'], ExistingInitiativeParticipantForm)
		self.assertContains(response, 'name="name"')
	
	def test_duplicate_participant_validation_errors_end_up_on_initiatives_page(self):
		initiative1 = Initiative.objects.create()
		participant1 = Participant.objects.create(name='textey', initiative=initiative1)
		response = self.client.post(
			f'/initiative/{initiative1.id}/',
			data={'name': 'textey'}
		)
		
		expected_error = escape(DUPLICATE_PARTICIPANT_ERROR)
		self.assertContains(response, expected_error)
		self.assertTemplateUsed(response, 'initiative/initiative.html')
		self.assertEqual(Participant.objects.all().count(), 1)
		
		
class NewInitiativeTest(TestCase):
	
	def test_for_invalid_input_renders_home_template(self):
		response = self.client.post('/initiative/new', data={'name': ''})
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'initiative/home.html')
	
	def test_validation_errors_are_shown_on_home_page(self):
		response = self.client.post('/initiative/new', data={'name': ''})
		self.assertContains(response, escape(EMPTY_PARTICIPANT_ERROR))
	
	def test_for_invalid_input_pass_form_to_template(self):
		response = self.client.post('/initiative/new', data={'name': ''})
		self.assertIsInstance(response.context['form'], ParticipantForm)

		
		