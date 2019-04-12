# initiative/test.py

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from initiative.models import Initiative, Participant



User = get_user_model()

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
	
	def test_create_new_creates_initiative_and_first_participant(self):
		Initiative.create_new(first_participant_text='Player A')
		new_participant = Participant.objects.first()
		self.assertEqual(new_participant.name, 'Player A')
		new_initiative = Initiative.objects.first()
		self.assertEqual(new_participant.initiative, new_initiative)
	
	def test_create_new_optionally_saves_owner(self):
		user = User.objects.create()
		Initiative.create_new(first_participant_text='Player A', owner=user)
		new_initiative = Initiative.objects.first()
		self.assertEqual(new_initiative.owner, user)
	
	def test_initiatives_can_have_owners(self):
		Initiative(owner=User()) # should not raise
	
	def test_list_owner_is_optional(self):
		Initiative().full_clean()
	
	def test_initiative_name_is_first_participant_name(self):
		initiative = Initiative.objects.create()
		Participant.objects.create(initiative=initiative, name='Monster 1')
		Participant.objects.create(initiative=initiative, name='Monster 2')
		self.assertEqual(initiative.name, 'Monster 1')


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