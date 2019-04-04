# functional_tests/tests.py

from selenium.webdriver.common.keys import Keys
from unittest import skip
from .base import FunctionalTest



class ItemValidationTest(FunctionalTest):
	
	def test_cannot_add_empty_list_items(self):
		# Alice goes to the home page and accidently tries to submit
		# an empty initiative item. She hits Enter on the empty input box
		self.browser.get(self.live_server_url)
		self.browser.find_element_by_id('id_new_participant').send_keys(Keys.ENTER)
		
		# The home page refreshes, and there is an error message saying
		# that initiative participants cannot be blank
		self.wait_for(lambda: self.assertEqual(
			self.browser.find_element_by_css_selector('.has-error').text,
			"You can't have an empty initiative participant!"
		))
		
		# She tries again with some text for the participant, which now works
		self.browser.find_element_by_id('id_new_participant').send_keys('Zilch the Puppet Master')
		self.browser.find_element_by_id('id_new_participant').send_keys(Keys.ENTER)
		self.wait_for_row_in_participant_table('1: Zilch the Puppet Master')
		
		# Perversely, she now decides to submit a second blank participant
		self.browser.find_element_by_id('id_new_participant').send_keys(Keys.ENTER)
		
		# She receives a similar warning on the initiative page
		self.wait_for(lambda: self.assertEqual(
			self.browser.find_element_by_css_selector('.has-error').text,
			"You can't have an empty initiative participant!"
		))
		
		# And she can correct it by filling some text in
		self.browser.find_element_by_id('id_new_participant').send_keys('Jim Puddington')
		self.browser.find_element_by_id('id_new_participant').send_keys(Keys.ENTER)
		self.wait_for_row_in_participant_table('1: Zilch the Puppet Master')
		self.wait_for_row_in_participant_table('2: Jim Puddington')
		
		
		