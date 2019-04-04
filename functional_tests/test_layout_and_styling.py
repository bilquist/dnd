# functional_tests/tests.py

from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest



class LayoutAndStylingTest(FunctionalTest):

	def test_layout_and_styling(self):
		# Alice goes to the homepage
		self.browser.get(self.live_server_url)
		self.browser.set_window_size(1024, 768)
		
		# She notices the input box is nicely centered
		inputbox = self.browser.find_element_by_id('id_new_participant')
		self.assertAlmostEqual(
			inputbox.location['x'] + inputbox.size['width'] / 2,
			512, #1024/2
			delta=10
		)
		
		# She starts a new list and sees the input is nicely
		# centered there too
		inputbox.send_keys('testing')
		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_participant_table('1: testing')
		inputbox = self.browser.find_element_by_id('id_new_participant')
		self.assertAlmostEqual(
			inputbox.location['x'] + inputbox.size['width'] / 2,
			512, #1024/2
			delta=10
		)
	
	