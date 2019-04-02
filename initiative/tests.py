# initiative/test.py

from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest
from initiative.models import Participant

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


class ParticipantModelTest(TestCase):
	
	def test_saving_and_retrieving_participants(self):
		first_participant = Participant()
		first_participant.name = 'Alice'
		first_participant.is_pc = 1
		first_participant.save()
		
		second_participant = Participant()
		second_participant.name = 'Bob'
		second_participant.is_pc = 1
		second_participant.save()
		
		saved_participants = Participant.objects.all()
		self.assertEqual(saved_participants.count(), 2)
		
		first_saved_participant = saved_participants[0]
		second_saved_participant = saved_participants[1]
		self.assertEqual(first_saved_participant.name, 'Alice')
		self.assertEqual(first_saved_participant.is_pc, 1)
		self.assertEqual(second_saved_participant.name, 'Bob')
		
		
		