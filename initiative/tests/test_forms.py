# initiative/tests/test_forms.py


import unittest
from unittest.mock import patch, Mock
from django.test import TestCase

from initiative.forms import (
	DUPLICATE_PARTICIPANT_ERROR, EMPTY_PARTICIPANT_ERROR,
	ExistingInitiativeParticipantForm, ParticipantForm, NewInitiativeForm
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
		#print(form.errors.keys())
		self.assertEqual(form.errors['name'], [EMPTY_PARTICIPANT_ERROR])
	
		
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
	
	def test_form_save(self):
		initiative = Initiative.objects.create()
		form = ExistingInitiativeParticipantForm(for_initiative=initiative, data={'name': 'my_name'})
		new_participant = form.save()
		self.assertEqual(new_participant, Participant.objects.all()[0])
		
		
class NewInitiativeFormTest(unittest.TestCase):
	
	@patch('initiative.forms.Initiative.create_new')
	def test_save_creates_new_initiative_from_post_data_if_user_not_authenticated(
		self, mock_Initiative_create_new
	):
		user = Mock(is_authenticated=False)
		form = NewInitiativeForm(data={'name': 'Player A'})
		form.is_valid()
		form.save(owner=user)
		mock_Initiative_create_new.assert_called_once_with(
			first_participant_text = 'Player A'
		)
	
	@patch('initiative.forms.Initiative.create_new')
	def test_save_creates_new_initiative_with_owner_if_user_authenticated(
		self, mock_Initiative_create_new
	):
		user = Mock(is_authenticated=True)
		form = NewInitiativeForm(data={'name': 'Player A'})
		form.is_valid()
		form.save(owner=user)
		mock_Initiative_create_new.assert_called_once_with(
			first_participant_text = 'Player A', owner=user
		)