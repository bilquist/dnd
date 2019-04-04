# initiative/test.py

from django.core.exceptions import ValidationError
from django.test import TestCase
from initiative.models import Initiative, Participant



# Create your tests here.
class ParticipantModelsTest(TestCase):
	
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
	
	def test_cannot_save_empty_initiative_participants(self):
		initiative = Initiative.objects.create()
		participant = Participant(name='', initiative=initiative)
		with self.assertRaises(ValidationError):
			participant.save()
			participant.full_clean()
	
	def test_get_absolute_url(self):
		initiative = Initiative.objects.create()
		self.assertEqual(initiative.get_absolute_url(), f'/initiative/{initiative.id}/')
		