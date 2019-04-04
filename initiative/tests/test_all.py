# initiative/test.py

from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest
from initiative.models import Initiative, Participant

from initiative.views import home_page



# Create your tests here.
class HomePageTest(TestCase):

	def test_home_page_returns_correct_html(self):
		response = self.client.get('/')
		self.assertTemplateUsed(response, 'initiative/home.html')


class ParticipantModelTest(TestCase):
	
	def test_saving_and_retrieving_participants(self):
		initiative = Initiative()
		initiative.save()
		
		first_participant = Participant()
		first_participant.name = 'Alice'
		first_participant.is_pc = 1
		first_participant.initiative = initiative
		first_participant.save()
		
		second_participant = Participant()
		second_participant.name = 'Bob'
		second_participant.is_pc = 1
		second_participant.initiative = initiative
		second_participant.save()
		
		saved_initiative = Initiative.objects.first()
		self.assertEqual(saved_initiative, initiative)
		
		saved_participants = Participant.objects.all()
		self.assertEqual(saved_participants.count(), 2)
		
		first_saved_participant = saved_participants[0]
		second_saved_participant = saved_participants[1]
		self.assertEqual(first_saved_participant.name, 'Alice')
		self.assertEqual(first_saved_participant.is_pc, 1)
		self.assertEqual(first_saved_participant.initiative, initiative)
		self.assertEqual(second_saved_participant.name, 'Bob')
		self.assertEqual(second_saved_participant.initiative, initiative)
		


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
		
		
class NewInitiativeTest(TestCase):

	def test_can_save_a_POST_request_to_an_existing_initiative(self):
		other_initiative = Initiative.objects.create()
		correct_initiative = Initiative.objects.create()
		
		self.client.post(
			f'/initiative/{correct_initiative.id}/add_participant',
			data={'participant_text': 'James Ihara'}
		)
		
		self.assertEqual(Participant.objects.count(), 1)
		new_participant = Participant.objects.first()
		self.assertEqual(new_participant.name, 'James Ihara')
		self.assertEqual(new_participant.initiative, correct_initiative)
		
	def test_redirects_to_initiative_view(self):
		other_initiative = Initiative.objects.create()
		correct_initiative = Initiative.objects.create()
		
		response = self.client.post(
			f'/initiative/{correct_initiative.id}/add_participant',
			data={'participant_text': 'James Ihara'}
		)
		
		
		self.assertRedirects(response, f'/initiative/{correct_initiative.id}/')
		
		