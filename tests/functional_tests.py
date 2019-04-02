# tests/functional_tests.py

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest



class NewVisitorTest(unittest.TestCase):

	def setUp(self):
		self.browser = webdriver.Firefox()
	
	def tearDown(self):
		self.browser.quit()
	
	def test_can_start_an_initiative_and_retrieve_it_later(self):
		# Alice has heard about a cool new online dnd app. She goes
		# to check out its homepage
		self.browser.get('http://localhost:8000')

		# She notices the page title and header mention 'Initiative'
		self.assertIn('Initiative', self.browser.title)
		header_text = self.browser.find_element_by_tag_name('h1').text
		self.assertIn('Participants', header_text)
		self.assertEqual('Participants', header_text)
		
		# She is invited to enter a participant right away
		inputbox = self.browser.find_element_by_id('id_new_participant')
		self.assertEqual(
			inputbox.get_attribute('placeholder'),
			'Enter a participant'
		)
		
		# She types "Player Character 1" into a text box (Alice is entering a PC)
		inputbox.send_keys('Player Character 1')
		
		# When she hits enter, the page updates, and now the page
		# "1: Player Character 1" as an item in the participant list
		inputbox.send_keys(Keys.ENTER)
		time.sleep(10)
		
		table = self.browser.find_element_by_id('id_participant_table')
		rows = table.find_elements_by_tag_name('tr')
		self.assertTrue(
			any(row.text == '1: Player Character 1' for row in rows),
			"New participant did not appear in the table"
		)
		
		# There is still a text box inviting her to add another participant
		# She enters, "Player Character 2"

		# Auto fail
		self.fail('Finish the test!')
		
		# She is invited to click to create an account

if __name__ == '__main__':
	unittest.main(warnings='ignore')