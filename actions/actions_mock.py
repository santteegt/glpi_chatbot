# -*- coding: utf-8 -*-

import logging
import requests
import json
from rasa_sdk import Action
from rasa_sdk.events import FollowupAction
from rasa_sdk.events import SlotSet

logger = logging.getLogger(__name__)


class ActionJoke(Action):
	"""An action to test the possibility to communicate with REST APIs"""

	def name(self):
		# define the name of the action which can then be included in training stories
		return "action_joke"

	def run(self, dispatcher, tracker, domain):
		# what your action should do
		request = json.loads(requests.get('https://api.chucknorris.io/jokes/random').text)  # make an api call
		joke = request['value']  # extract a joke from returned json response
		dispatcher.utter_message(joke)  # send the message back to the user
		return []


class ValidateAuth(Action):
	"""An action that validates if the user is authenticated"""

	_LOGGED_IN = "logged_in"

	def name(self):
		# define the name of the action which can then be included in training stories
		return "action_validate_auth"

	def run(self, dispatcher, tracker, domain):
		# what your action should do
		auth_token = tracker.get_slot("auth_token")
		logged_in = False
		events = []
		if not auth_token:
			# json_payload = {self._LOGGED_IN: logged_in}
			# dispatcher.utter_message(\
			# 	"Para continuar es necesario que Inicie Sesión con su cuenta institucional", json_message=json_payload)
			dispatcher.utter_message( \
				"Para continuar es necesario que Inicie Sesión con su cuenta institucional")
		else:  # TODO: validate auth with provider
			# events.append(FollowupAction("utter_intro"))
			logged_in = True

		events.append(SlotSet(self._LOGGED_IN, logged_in))

		return events

