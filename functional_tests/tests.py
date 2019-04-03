# functional_tests/tests.py

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
import time



class NewVisitorTest(StaticLiveServerTestCase):

	def setUp(self):
		self.browser = webdriver.Firefox()
		self.MAX_WAIT = 10
	
	def tearDown(self):
		self.browser.quit()
	
	def wait_for_row_in_participant_table(self, row_text):
		start_time = time.time()
		while True:
			try:
				table = self.browser.find_element_by_id('id_participant_table')
				rows = table.find_elements_by_tag_name('tr')
				self.assertIn(row_text, [row.text for row in rows])
				return
			except (AssertionError, WebDriverException) as e:
				if time.time() - start_time > self.MAX_WAIT:
					raise e
				time.sleep(0.5)
	
	def test_can_start_an_initiative_and_retrieve_it_later(self):
		# Alice has heard about a cool new online dnd app. She goes
		# to check out its homepage
		self.browser.get(self.live_server_url)

		# She notices the page title and header mention 'Initiative'
		self.assertIn('Initiative', self.browser.title)
		header_text = self.browser.find_element_by_tag_name('h1').text
		self.assertIn('Start a new Initiative', header_text)
		self.assertEqual('Start a new Initiative', header_text)
		
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
		self.wait_for_row_in_participant_table('1: Player Character 1')
		
		# There is still a text box inviting her to add another participant
		# She enters, "Player Character 2"
		inputbox = self.browser.find_element_by_id('id_new_participant')
		inputbox.send_keys('Player Character 2')
		inputbox.send_keys(Keys.ENTER)
		
		# The page updates again, and now shows both characters as participants
		self.wait_for_row_in_participant_table('1: Player Character 1')
		self.wait_for_row_in_participant_table('2: Player Character 2')
		
		# Satisfied, she goes back to sleep
	
	def test_multiple_users_can_start_lists_at_different_urls(self):
		# Alice starts a new initiative
		self.browser.get(self.live_server_url)
		inputbox = self.browser.find_element_by_id('id_new_participant')
		inputbox.send_keys('Player Character 1')
		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_participant_table('1: Player Character 1')
		
		# She notices that her list has a unique URL
		alice_initiative_url = self.browser.current_url
		
		self.assertRegex(alice_initiative_url, '/initiative/.+')
		
		# Now a new user, Francis, comes along to the site
		
		## We use a new browser session to make sure that no information
		## of Alice's is coming through from cookies, etc.
		self.browser.quit()
		self.browser = webdriver.Firefox()
		
		# Francis visits the home page. There is no sign of Alice's list
		self.browser.get(self.live_server_url)
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Player Character 1', page_text)
		self.assertNotIn('Player Character 2', page_text)
		
		# Francis starts a new initiative by entering a new participant. He
		# is more interesting than Alice
		inputbox = self.browser.find_element_by_id('id_new_participant')
		inputbox.send_keys('Gork the Exterminator!')
		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_participant_table('1: Gork the Exterminator!')
		
		# Francis gets his own URL
		francis_initiative_url = self.browser.current_url
		self.assertRegex(francis_initiative_url, '/initiative/.+')
		self.assertNotEqual(francis_initiative_url, alice_initiative_url)
		
		# Again, there is no trace of Alice's initiative
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Player Character 1', page_text)
		self.assertIn('Gork the Exterminator!', page_text)
		
		# Satisfied, they both go back to sleep

		# Auto fail
		self.fail('Finish the test!')
		
		# She is invited to click to create an account

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