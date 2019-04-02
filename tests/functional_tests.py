# tests/functional_tests.py

from selenium import webdriver
import unittest



class NewVisitorTest(unittest.TestCase):

	def setUp(self):
		self.browser = webdriver.Firefox()
	
	def tearDown(self):
		self.browser.quit()
	
	def test_can_create_a_profile(self):
		# Alice has heard about a cool new online dnd app. She goes
		# to check out its homepage
		self.browser.get('http://localhost:8000')

		# She notices the page title and header mention 'Drage Eventyr'
		self.assertIn('Initiative', self.browser.title)

		# Auto fail
		self.fail('Finish the test!')
		
		# She is invited to click to create an account

if __name__ == '__main__':
	unittest.main(warnings='ignore')