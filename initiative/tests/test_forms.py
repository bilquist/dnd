# initiative/tests/test_forms.py

from django.test import TestCase

from initiative.forms import EMPTY_PARTICIPANT_ERROR, ParticipantForm



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