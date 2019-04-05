# functional_tests/tests.py

from selenium.webdriver.common.keys import Keys
from unittest import skip
from .base import FunctionalTest



class ParticipantValidationTest(FunctionalTest):
	
	def test_cannot_add_empty_list_items(self):
		# Alice goes to the home page and accidently tries to submit
		# an empty initiative item. She hits Enter on the empty input box
		self.browser.get(self.live_server_url)
		self.get_participant_input_box().send_keys(Keys.ENTER)
		
		# The browser intercepts the request and does not load the initiative
		# page
		self.wait_for(lambda: self.browser.find_elements_by_css_selector(
			'#id_text:invalid'
		))
		
		# She starts typing some text for the new participant and the error
		# disappears
		self.get_participant_input_box().send_keys('Test Participant')
		self.wait_for(lambda: self.browser.find_elements_by_css_selector(
			'#id_text:valid'
		))
		
		# And she can submit it successfully
		self.get_participant_input_box().send_keys(Keys.ENTER)
		self.wait_for_row_in_participant_table('1: Test Participant')
		
		# Preversely, she now decides to submit a second blank initiative item
		self.get_participant_input_box().send_keys(Keys.ENTER)
		
		# Again, the browser will not comply
		self.wait_for_row_in_participant_table('1: Test Participant')
		self.wait_for(lambda: self.browser.find_elements_by_css_selector(
			'#id_text:invalid'
		))
		
		# And she can correct it by filling some text in
		self.get_participant_input_box().send_keys('Magician Waldo')
		self.wait_for(lambda: self.browser.find_elements_by_css_selector(
			'#id_text:valid'
		))
		self.get_participant_input_box().send_keys(Keys.ENTER)
		self.wait_for_row_in_participant_table('1: Test Participant')
		self.wait_for_row_in_participant_table('2: Magician Waldo')
	
	def test_cannot_add_duplicate_participants(self):
		# Alice goes to the home page and starts a new list
		self.browser.get(self.live_server_url)
		self.get_participant_input_box().send_keys('Babe')
		self.get_participant_input_box().send_keys(Keys.ENTER)
		self.wait_for_row_in_participant_table('1: Babe')
		
		# She accidently tries to enter a duplicate participant
		self.get_participant_input_box().send_keys('Babe')
		self.get_participant_input_box().send_keys(Keys.ENTER)
		
		# She sees a helpful error message
		self.wait_for(lambda: self.assertEqual(
			self.browser.find_element_by_css_selector('.has-error').text,
			"You've already got this in your initiative!"
		))
		