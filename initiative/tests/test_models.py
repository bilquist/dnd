# initiative/test.py

from django.core.exceptions import ValidationError
from django.test import TestCase
from initiative.models import Initiative, Participant



# Create your tests here.
class InitiativeAndParticipantModelsTest(TestCase):

	def test_participant_is_related_to_initiative(self):
		initiative = Initiative.objects.create()
		participant = Participant()
		participant.initiative = initiative
		participant.save()
		self.assertIn(participant, initiative.participant_set.all())


class InitiativeModelTest(TestCase):
	
	def test_get_absolute_url(self):
		initiative = Initiative.objects.create()
		self.assertEqual(initiative.get_absolute_url(), f'/initiative/{initiative.id}/')


class ParticipantModelTest(TestCase):
	
	def test_default_name(self):
		participant = Participant()
		self.assertEqual(participant.name, '')
	
	def test_cannot_save_empty_initiative_participants(self):
		initiative = Initiative.objects.create()
		participant = Participant(name='', initiative=initiative)
		with self.assertRaises(ValidationError):
			participant.save()
			participant.full_clean()
	
	def test_duplicate_participants_are_invalid(self):
		initiative = Initiative.objects.create()
		Participant.objects.create(name='bla', initiative=initiative)
		with self.assertRaises(ValidationError):
			participant = Participant(name='bla', initiative=initiative)
			participant.full_clean()
	
	def test_CAN_save_item_to_different_initiatives(self):
		initiative1 = Initiative.objects.create()
		initiative2 = Initiative.objects.create()
		Participant.objects.create(name='bla', initiative=initiative1)
		participant = Participant(name='bla', initiative=initiative2)
		participant.full_clean() # should not raise
	
	def test_initiative_ordering(self):
		initiative = Initiative.objects.create()
		participant1 = Participant.objects.create(name='p1', initiative=initiative)
		participant2 = Participant.objects.create(name='p2', initiative=initiative)
		participant3 = Participant.objects.create(name='p3', initiative=initiative)
		self.assertEqual(
			list(Participant.objects.all()),
			[participant1, participant2, participant3]
		)
	
	def test_string_representation(self):
		participant = Participant(name='some name')
		self.assertEqual(str(participant), 'some name')