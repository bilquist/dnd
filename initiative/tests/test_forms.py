# initiative/tests/test_forms.py

from django.test import TestCase

from initiative.forms import (
	DUPLICATE_PARTICIPANT_ERROR, EMPTY_PARTICIPANT_ERROR,
	ExistingInitiativeParticipantForm, ParticipantForm
)
from initiative.models import Initiative, Participant



class ParticipantFormTest(TestCase):

	def test_form_participant_input_has_placeholder_and_css_classes(self):
		form = ParticipantForm()
		self.assertIn('placeholder="Enter a participant"', form.as_p())
		self.assertIn('class="form-control input-lg"', form.as_p())
	
	def test_form_validation_for_blank_participants(self):
		form = ParticipantForm(data={'name': ''})
		self.assertFalse(form.is_valid())
		print(form.errors.keys())
		self.assertEqual(form.errors['name'], [EMPTY_PARTICIPANT_ERROR])
	
	def test_form_save_handles_saving_to_a_list(self):
		initiative = Initiative.objects.create()
		form = ParticipantForm(data={'name': 'Scooby DooMe'})
		new_participant = form.save(for_initiative=initiative)
		self.assertEqual(new_participant, Participant.objects.first())
		self.assertEqual(new_participant.name, 'Scooby DooMe')
		self.assertEqual(new_participant.initiative, initiative)
		
		
class ExistingInitiativeParticipantFormTest(TestCase):
	
	def test_form_renders_participant_name_input(self):
		initiative = Initiative.objects.create()
		form = ExistingInitiativeParticipantForm(for_initiative=initiative)
		self.assertIn('placeholder="Enter a participant"', form.as_p())
	
	def test_form_validation_for_blank_items(self):
		initiative = Initiative.objects.create()
		Participant.objects.create(name='no twins!', initiative=initiative)
		form = ExistingInitiativeParticipantForm(for_initiative=initiative, data={'name': 'no twins!'})
		self.assertFalse(form.is_valid())
		self.assertEqual(form.errors['name'], [DUPLICATE_PARTICIPANT_ERROR])
		
		