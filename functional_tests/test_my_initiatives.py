# functional_tests/test_my_initiative.py

from django.conf import settings
from django.contrib.auth import BACKEND_SESSION_KEY, SESSION_KEY, get_user_model
from django.contrib.sessions.backends.db import SessionStore

from .base import FunctionalTest
from .management.commands.create_session import create_pre_authenticated_session
from .server_tools import create_session_on_server

import time



User = get_user_model()

class MyInitiativesTest(FunctionalTest):
	
	def create_pre_authenticated_session(self, email):
		if self.staging_server:
			session_key = create_session_on_server(self.staging_server, email)
		else:
			session_key = create_pre_authenticated_session(email)
		## to set a cookie we need to first visit the domain.
		## 404 pages load the quickest!
		self.browser.get(self.live_server_url + '/404_no_such_url/')
		self.browser.add_cookie(dict(
			name=settings.SESSION_COOKIE_NAME,
			value=session_key,
			path='/',
		))
	
	def test_logged_in_users_initiatives_are_saved_as_my_initiatives(self):
		# Alice is a logged-in user
		self.create_pre_authenticated_session('alice@example.com')
		
		# She goes to the home page and starts a list
		self.browser.get(self.live_server_url)
		self.add_initiative_participant('Player 1')
		self.add_initiative_participant('Player 2')
		first_initiative_url = self.browser.current_url
		
		# She notices a "My initiatives" link, for the first time.
		self.browser.find_element_by_link_text('My initiatives').click()
		
		# She sees that her initiative is in there, named according to its first
		# initiative participant
		self.wait_for(
			lambda: self.browser.find_element_by_link_text('Player 1')
		)
		self.browser.find_element_by_link_text('Player 1').click()
		self.wait_for(
			lambda: self.assertEqual(self.browser.current_url, first_initiative_url)
		)
		
		# She decides to start another initiative, just to see
		self.browser.get(self.live_server_url)
		self.add_initiative_participant('Monster 1')
		second_initiative_url = self.browser.current_url
		
		# Under "my lists", her new list appears
		self.browser.find_element_by_link_text('My initiatives').click()
		self.wait_for(
			lambda: self.browser.find_element_by_link_text('Monster 1')
		)
		self.browser.find_element_by_link_text('Monster 1').click()
		self.wait_for(
			lambda: self.assertEqual(self.browser.current_url, second_initiative_url)
		)
		
		# She logs out. The "My initiatives" option disappears
		self.browser.find_element_by_link_text('Log out').click()
		self.wait_for(
			lambda: self.assertEqual(self.browser.find_elements_by_link_text('My initiative'),
			[]
		))
	