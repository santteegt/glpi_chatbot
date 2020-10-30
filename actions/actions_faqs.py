# -*- coding: utf-8 -*-

import logging
from typing import Any, Dict, List, Text
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from rasa_sdk.forms import REQUESTED_SLOT

import re

from actions.actions import ask_if_success
from actions.constants import EntitySlotEnum, GLPICategories, UtteranceEnum

logger = logging.getLogger(__name__)


class WifiFaq(Action):
	def name(self) -> Text:
		return "validate_wifi_faq_form"

	@staticmethod
	def wifi_network_db() -> List[Text]:
		"""Database of supported wifi networks"""

		return ["eduroam", "ucwifi", "guest"]

	def validate_wifi_network(
			self,
			value: Text,
			dispatcher: CollectingDispatcher,
			tracker: Tracker,
			domain: Dict[Text, Any],
	) -> Dict[Text, Any]:
		"""Validate wifi_network has a valid value."""

		if value.lower() in self.wifi_network_db():
			# validation succeeded
			return {EntitySlotEnum.WIFI_NETWORK: value}
		else:
			dispatcher.utter_message(template=UtteranceEnum.NO_WIFI_NETWORK)
			dispatcher.utter_message(
				text=f"Redes WiFi disponibles: {self.wifi_network_db()}"
			)
			# validation failed, set this slot to None, meaning the
			# user will be asked for the slot again
			return {EntitySlotEnum.WIFI_NETWORK: None}

	def validate_email(
			self,
			value: Text,
			dispatcher: CollectingDispatcher,
			tracker: Tracker,
			domain: Dict[Text, Any],
	) -> Dict[Text, Any]:
		"""Validate email has a valid value."""

		if re.search(r"@ucuenca\.edu\.ec$", value.lower()) is not None:
			# validation succeeded
			return {EntitySlotEnum.EMAIL: value.lower()}
		else:
			dispatcher.utter_message(template=UtteranceEnum.EMAIL_NO_MATCH)
			# validation failed, set this slot to None, meaning the
			# user will get info to connect to the guest network
			return {
				EntitySlotEnum.WIFI_NETWORK: "guest",
				EntitySlotEnum.EMAIL: value.lower(),
			}

	def run(
			self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any],
	) -> List[Dict]:
		"""
			Define what the form has to do after all required slots are filled
		"""

		wifi_network = tracker.slots.get(EntitySlotEnum.WIFI_NETWORK)
		wifi_networks = self.wifi_network_db()

		if wifi_network is None:
			return [SlotSet(REQUESTED_SLOT, EntitySlotEnum.WIFI_NETWORK)]
		elif wifi_network.lower() in wifi_networks[:2] and \
				tracker.slots.get(EntitySlotEnum.EMAIL) is None:
			return [SlotSet(REQUESTED_SLOT, EntitySlotEnum.EMAIL)]

		instructions = {
			wifi_networks[0]: UtteranceEnum.EDUROAM_INSTRUCTIONS,
			wifi_networks[1]: UtteranceEnum.UCWIFI_INSTRUCTIONS,
			wifi_networks[2]: UtteranceEnum.GUEST_WIFI_INSTRUCTIONS,
		}

		dispatcher.utter_message(template=instructions[wifi_network.lower()])

		ask_if_success(
			dispatcher,
			incident_title="Problema de conexion a la red WIFI",
			itilcategory_id=GLPICategories.NETWORK_CONNECTIVITY,
		)

		return [
			SlotSet(REQUESTED_SLOT, None),
			SlotSet(EntitySlotEnum.WIFI_NETWORK, None),
			SlotSet(EntitySlotEnum.EMAIL, None)
		]


class CreateUserFaq(Action):
	def name(self) -> Text:
		return "validate_create_user_faq_form"

	@staticmethod
	def course_type_db() -> List[Text]:
		"""Database of supported student types"""

		return ["carrera", "curso"]

	def validate_course_type(
		self,
		value: Text,
		dispatcher: CollectingDispatcher,
		tracker: Tracker,
		domain: Dict[Text, Any],
	) -> Dict[Text, Any]:
		"""Validate COURSE_TYPE has a valid value."""

		# logger.info(f"COURSE TYPE ===> {value.lower()}:{value.lower() in self.course_type_db()}")
		if value.lower() in self.course_type_db():
			# validation succeeded
			return {EntitySlotEnum.COURSE_TYPE: value.lower()}
		else:
			dispatcher.utter_message(template=UtteranceEnum.INVALID)
			# validation failed, set this slot to None, meaning the
			# user will be asked for the slot again
			return {EntitySlotEnum.COURSE_TYPE: None}

	def run(
		self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any],
	) -> List[Dict]:

		has_email = tracker.slots.get(EntitySlotEnum.HAS_EMAIL)
		course_type = tracker.slots.get(EntitySlotEnum.COURSE_TYPE)
		if has_email is None:
			return [SlotSet(REQUESTED_SLOT, EntitySlotEnum.HAS_EMAIL)]
		elif has_email:
			dispatcher.utter_message(template=UtteranceEnum.RECOVER_PASSWORD)
		elif course_type is None:
			return [SlotSet(REQUESTED_SLOT, EntitySlotEnum.COURSE_TYPE)]
		else:
			course_types = self.course_type_db()
			instructions = {
				course_types[0]: "https://admision.ucuenca.edu.ec/",
				course_types[1]: "https://registro.ucuenca.edu.ec/",
			}

			dispatcher.utter_message(
				"Para poder registrar una cuenta por favor visita el siguiente enlace: "
				+ instructions[course_type]
			)

		logger.info('final')
		ask_if_success(
			dispatcher,
			incident_title="Problema para crear un usuario",
			itilcategory_id=GLPICategories.USER_MGMT,
		)

		return [
			SlotSet(REQUESTED_SLOT, None),
			SlotSet(EntitySlotEnum.HAS_EMAIL, None),
			SlotSet(EntitySlotEnum.COURSE_TYPE, None),
		]
