# -*- coding: utf-8 -*-

import logging
from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
from rasa_sdk.events import SlotSet, EventType
import re
from typing import Dict, Text, Any, List, Union, Optional

from actions.actions_base import request_next_slot
from actions.constants import UtteranceEnum, IntentEnum, EntitySlotEnum
from actions.glpi import GLPIService, GlpiException, load_glpi_config, Ticket
from actions.parsing import remove_accents

logger = logging.getLogger(__name__)

glpi_api_uri, glpi_app_token, glpi_auth_token, local_mode = load_glpi_config()
glpi = GLPIService.get_instance(glpi_api_uri, glpi_app_token, glpi_auth_token) if not local_mode else None


class OpenIncidentForm(FormAction):

	def name(self) -> Text:
		return "open_incident_form"

	@staticmethod
	def required_slots(tracker: Tracker) -> List[Text]:
		"""A list of required slots that the form has to fill"""

		return [EntitySlotEnum.EMAIL,
		        EntitySlotEnum.INCIDENT_TITLE,
		        EntitySlotEnum.INCIDENT_DESCRIPTION,
		        # EntitySlotEnum.PRIORITY,
		        EntitySlotEnum.ITILCATEGORY_ID,
		        EntitySlotEnum.CONFIRM]

	def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
		"""A dictionary to map required slots to
		- an extracted entity
		- intent: value pairs
		- a whole message
		or a list of them, where a first match will be picked"""

		return {
			EntitySlotEnum.EMAIL: self.from_entity(entity=EntitySlotEnum.EMAIL),
			EntitySlotEnum.INCIDENT_TITLE: [
				self.from_trigger_intent(
					intent=IntentEnum.PASSWORD_RESET,
					value="Problema para recuperar contrasena",
				),
				self.from_trigger_intent(
					intent=IntentEnum.PROBLEM_EMAIL,
					value="Problema con correo electronico",
				),
				self.from_text(
					intent=[IntentEnum.PASSWORD_RESET, IntentEnum.PROBLEM_EMAIL, IntentEnum.INFORM]
				),
				self.from_text()
			],
			EntitySlotEnum.INCIDENT_DESCRIPTION: [
				self.from_text(
					intent=[IntentEnum.PASSWORD_RESET, IntentEnum.PROBLEM_EMAIL, IntentEnum.INFORM]
				),
				self.from_text(not_intent=IntentEnum.OUT_OF_SCOPE)
			],
			# EntitySlotEnum.PRIORITY: self.from_entity(entity=EntitySlotEnum.PRIORITY),
			EntitySlotEnum.ITILCATEGORY_ID: [
				self.from_trigger_intent(
					intent=IntentEnum.PASSWORD_RESET,
					value="56",  # Gestion de usuarios
				),
				self.from_trigger_intent(
					intent=IntentEnum.PROBLEM_EMAIL,
					value="41"  # Correo electronico,
				),
				self.from_trigger_intent(
					intent=IntentEnum.OPEN_INCIDENT,
					value="65"  # Varios
				)
			],
			EntitySlotEnum.CONFIRM: [
				self.from_intent(intent=IntentEnum.CONFIRM, value=True),
				self.from_intent(intent=IntentEnum.DENY, value=False)
			]
		}

	def request_next_slot(
        self,
        dispatcher: "CollectingDispatcher",
        tracker: "Tracker",
        domain: Dict[Text, Any],
    ) -> Optional[List[EventType]]:
		"""Customize ask utterance for certain slots
			This is Required to enable the {form_name}_{confirm} slot
		"""
		return request_next_slot(self, dispatcher, tracker, domain)

	@staticmethod
	def priority_db() -> List[Text]:
		"""Database of supported priorities"""

		# return ["baja", "media", "alta"]
		return GLPIService.priority_values().keys()

	def validate_email(
			self,
			value: Text,
			dispatcher: CollectingDispatcher,
			tracker: Tracker,
			domain: Dict[Text, Any],
	) -> Dict[Text, Any]:
		"""Validate email is in ticket system."""
		if local_mode:
			return {EntitySlotEnum.EMAIL: value}

		# TODO: validate if email format
		return {EntitySlotEnum.EMAIL: value}

	# results = email_to_sysid(value)

	# def validate_priority(
	# 		self,
	# 		value: Text,
	# 		dispatcher: CollectingDispatcher,
	# 		tracker: Tracker,
	# 		domain: Dict[Text, Any],
	# ) -> Dict[Text, Any]:
	# 	"""Validate priority is a valid value."""
	#
	# 	if value.lower() in self.priority_db():
	# 		# validation succeeded,
	# 		# set the value of the "priority" slot to value
	# 		return {EntitySlotEnum.PRIORITY: value.lower()}
	# 	else:
	# 		dispatcher.utter_message(template=UtteranceEnum.PRIORITY_NO_MATCH)
	# 		# validation failed, set this slot to None, meaning the
	# 		# user will be asked for the slot again
	# 		return {EntitySlotEnum.PRIORITY: None}

	def submit(
			self,
			dispatcher: CollectingDispatcher,
			tracker: Tracker,
			domain: Dict[Text, Any],
	) -> List[Dict]:
		"""Define what the form has to do after all required slots are filled"""

		email = tracker.get_slot(EntitySlotEnum.EMAIL)
		incident_title = tracker.get_slot(EntitySlotEnum.INCIDENT_TITLE)
		incident_description = tracker.get_slot(EntitySlotEnum.INCIDENT_DESCRIPTION)
		# priority = tracker.get_slot(EntitySlotEnum.PRIORITY)
		itilcategory_id = tracker.get_slot(EntitySlotEnum.ITILCATEGORY_ID)

		events = [SlotSet(EntitySlotEnum.EMAIL, None),
		          SlotSet(EntitySlotEnum.INCIDENT_TITLE, None),
		          SlotSet(EntitySlotEnum.INCIDENT_DESCRIPTION, None),
		          # SlotSet(EntitySlotEnum.PRIORITY, None),
		          SlotSet(EntitySlotEnum.ITILCATEGORY_ID, None),
		          SlotSet(EntitySlotEnum.CONFIRM, None)]

		if tracker.get_slot(EntitySlotEnum.CONFIRM):
			# Check priority and set number value accordingly
			# priorities = GLPIService.priority_values()
			# priority_values = list(priorities.keys())
			# if priority in priority_values:
			# 	glpi_priority = priorities[priority]
			# else:
			# 	logger.warning(f'Priority value not found: {priority}. Setting it to default: (media)')
			# 	glpi_priority = priorities[priority_values[1]]

			ticket: Ticket = Ticket({
				'username': 'normal',  # TODO: set the actual logged in user
				'title': incident_title,
				'description': remove_accents(incident_description),
				# 'priority': glpi_priority
				'itilcategories_id': int(itilcategory_id),
				'alternative_email': email  # TODO: set as conditional if username is not logged in
			})

			if local_mode:
				dispatcher.utter_message(f"Esta acción crearía un ticket con la siguiente información: {ticket}")
				ticket_id = "DUMMY"
				events.append(SlotSet(EntitySlotEnum.TICKET_NO, ticket_id))
			else:  # TODO: integrate with GLPI
				try:
					response = glpi.create_ticket(ticket)
					ticket_id = response['id']
					# This is not actually required as its value is sent directly to the utter_message
					events.append(SlotSet(EntitySlotEnum.TICKET_NO, ticket_id))
				except GlpiException as e:
					logger.error("Error when trying to create a ticket", e)
					logger.error(f"Ticket: {ticket}")
					dispatcher.utter_message(template=UtteranceEnum.PROCESS_FAILED)
					return events
			dispatcher.utter_message(template=UtteranceEnum.TICKET_NO, ticket_no=ticket_id)
			dispatcher.utter_message(template=UtteranceEnum.CONFIRM_REQUEST)
		else:
			events.append(SlotSet(EntitySlotEnum.TICKET_NO, None))
			dispatcher.utter_message(template=UtteranceEnum.PROCESS_CANCELLED)

		return events


class IncidentStatusForm(FormAction):

	def name(self) -> Text:
		return "incident_status_form"

	@staticmethod
	def required_slots(tracker: Tracker) -> List[Text]:
		"""A list of required slots that the form has to fill"""
		return [
			EntitySlotEnum.TICKET_NO,
			EntitySlotEnum.EMAIL
		]

	def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
		"""A dictionary to map required slots to
		- an extracted entity
		- intent: value pairs
		- a whole message
		or a list of them, where a first match will be picked"""

		return {
			EntitySlotEnum.TICKET_NO: [
				self.from_entity(entity=EntitySlotEnum.TICKET_NO),
				self.from_text(not_intent=IntentEnum.OUT_OF_SCOPE)
			],
			EntitySlotEnum.EMAIL: self.from_entity(entity=EntitySlotEnum.EMAIL)
		}

	def validate_ticket_no(
			self,
			value: Text,
			dispatcher: CollectingDispatcher,
			tracker: Tracker,
			domain: Dict[Text, Any],
	) -> Dict[Text, Any]:
		"""Validate email is in ticket system."""
		if local_mode:
			return {EntitySlotEnum.TICKET_NO: value}

		if re.match(r"^[0-9]+$", value) is not None:
			return {EntitySlotEnum.TICKET_NO: value}
		else:
			dispatcher.utter_message(template=UtteranceEnum.INVALID)
			# validation failed, set this slot to None, meaning the
			# user will get info to connect to the guest network
			return {EntitySlotEnum.TICKET_NO: None}

	def validate_email(
			self,
			value: Text,
			dispatcher: CollectingDispatcher,
			tracker: Tracker,
			domain: Dict[Text, Any],
	) -> Dict[Text, Any]:
		"""Validate email is in ticket system."""
		if local_mode:
			return {EntitySlotEnum.EMAIL: value}

		# TODO: validate if email format
		return {EntitySlotEnum.EMAIL: value}

	def submit(
			self,
			dispatcher: CollectingDispatcher,
			tracker: Tracker,
			domain: Dict[Text, Any],
	) -> List[Dict]:
		"""Define what the form has to do after all required slots are filled"""

		ticket_no = tracker.get_slot(EntitySlotEnum.TICKET_NO)
		email = tracker.get_slot(EntitySlotEnum.EMAIL)

		events = []

		if local_mode:
			dispatcher.utter_message(f"Esta acción obtendría información del ticket con id: {ticket_no}")
		else:
			try:
				response = glpi.get_ticket_status(ticket_no)  # to get alternative_email?
				# TODO: validate ticket with provided username and email
				if len(response['alternative_email']) == 0:
					user = glpi.get_user(user_id=response['user_id'])
					logger.warning(f'User found: {user}')
					# TODO: complete logic
				elif response['alternative_email'] != email:
					message = 'Lo siento! No se ha encontrado un ticket asociado a la información especificada'
					dispatcher.utter_message(message)
					events.append(SlotSet(EntitySlotEnum.TICKET_NO, None))
					events.append(SlotSet(EntitySlotEnum.EMAIL, None))

				# TODO: set values properly
				# closedate
				status = response['status']
				resolution = response['solvedate'] if response['solvedate'] else 'No disponible'

				dispatcher.utter_message('A continuación se encuentra la última información sobre su incidencia')
				dispatcher.utter_message(template=UtteranceEnum.TICKET_STATUS, ticket_no=ticket_no,
				                         title=response['title'], category=response['category'],
				                         status=status, resolution=resolution, date_mod=response['date_mod'])
			except GlpiException as e:
				logger.error(f"Error when trying to fetch ticket status: {ticket_no}", e)
				dispatcher.utter_message(template=UtteranceEnum.PROCESS_FAILED)

		return events
