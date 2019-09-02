# -*- coding: utf-8 -*-

import logging
import requests
import json
from rasa_sdk import Action

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