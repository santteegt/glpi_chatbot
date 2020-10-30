# -*- coding: utf-8 -*-

import logging
from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from rasa_sdk import Action
from typing import Any, Dict, List, Text

from actions.constants import EntitySlotEnum, UtteranceEnum
from actions.glpi import GLPIService, GlpiException, load_glpi_config, Ticket
from actions.parsing import remove_accents

logger = logging.getLogger(__name__)

# Loading GLPI API config
glpi_api_uri, glpi_app_token, glpi_auth_token, glpi_local_mode = load_glpi_config()
glpi = GLPIService.get_instance(glpi_api_uri, glpi_app_token, glpi_auth_token) if not glpi_local_mode else None


class OpenIncident(Action):

	def name(self) -> Text:
		return "action_open_incident"

	def run(self,
	        dispatcher: CollectingDispatcher,
	        tracker: Tracker,
	        domain: Dict[Text, Any]) -> List[Dict]:
		"""
				Define what the form has to do after all required slots are filled
			:param dispatcher:
			:param tracker:
			:param domain:
			:return:
			"""

		email = tracker.get_slot(EntitySlotEnum.EMAIL)
		incident_title = tracker.get_slot(EntitySlotEnum.INCIDENT_TITLE)
		incident_description = tracker.get_slot(EntitySlotEnum.INCIDENT_DESCRIPTION)
		# priority = tracker.get_slot(EntitySlotEnum.PRIORITY)
		itilcategory_id = tracker.get_slot(EntitySlotEnum.ITILCATEGORY_ID)

		events = [
			SlotSet(EntitySlotEnum.EMAIL, None),
			SlotSet(EntitySlotEnum.INCIDENT_TITLE, None),
			SlotSet(EntitySlotEnum.INCIDENT_DESCRIPTION, None),
			# SlotSet(EntitySlotEnum.PRIORITY, None),
			SlotSet(EntitySlotEnum.ITILCATEGORY_ID, None),
			SlotSet(EntitySlotEnum.CONFIRM, None),
		]

		if tracker.get_slot(EntitySlotEnum.CONFIRM):
			ticket: Ticket = Ticket({
				"username": "normal",  # TODO: set the actual logged in user
				"title": incident_title,
				"description": remove_accents(incident_description),
				# 'priority': glpi_priority
				"itilcategories_id": int(itilcategory_id),
				"alternative_email": email,  # TODO: set as conditional if username is not logged in
			})

			if glpi_local_mode:
				dispatcher.utter_message(
					f"Esta acción crearía un ticket con la siguiente información: {ticket}"
				)
				ticket_id = "DUMMY"
				events.append(SlotSet(EntitySlotEnum.TICKET_NO, ticket_id))
			else:  # TODO: integrate with GLPI
				try:
					response = glpi.create_ticket(ticket)
					ticket_id = response["id"]
					# This is not actually required as its value is sent directly to the utter_message
					events.append(SlotSet(EntitySlotEnum.TICKET_NO, ticket_id))
				except GlpiException as e:
					logger.error("Error when trying to create a ticket", e)
					logger.error(f"Ticket: {ticket}")
					dispatcher.utter_message(template=UtteranceEnum.PROCESS_FAILED)
					return events
			dispatcher.utter_message(
				template=UtteranceEnum.TICKET_NO, ticket_no=f'{ticket_id}'
			)
			dispatcher.utter_message(template=UtteranceEnum.CONFIRM_REQUEST)

		else:
			events.append(SlotSet(EntitySlotEnum.TICKET_NO, None))
			dispatcher.utter_message(template=UtteranceEnum.PROCESS_CANCELLED)

		return events


class IncidentStatus(Action):
	def name(self) -> Text:
		return "action_incident_status"

	def run(self,
	        dispatcher: CollectingDispatcher,
	        tracker: Tracker,
	        domain: Dict[Text, Any]) -> List[Dict]:
		"""
			Define what the form has to do after all required slots are filled
		"""
		ticket_no = tracker.get_slot(EntitySlotEnum.TICKET_NO)
		email = tracker.get_slot(EntitySlotEnum.EMAIL)

		events = []

		if glpi_local_mode:
			dispatcher.utter_message(
				f"Esta acción obtendría información del ticket con id: {ticket_no}"
			)
		else:
			show_info = True
			message = "Lo siento! No se ha encontrado un ticket asociado a la información especificada"
			try:
				response = glpi.get_ticket_status(ticket_no)  # to get alternative_email?
				# TODO: validate ticket with provided username and email
				if not response:
					show_info = False
				else:
					if len(response["alternative_email"]) == 0:
						user = glpi.get_user(user_id=response["user_id"])
						logger.warning(f"User found: {user}")
						# TODO: complete logic
					elif response["alternative_email"] != email:
						logger.warning(f'User email does not match: {email} != {response["alternative_email"]}')
						show_info = False

				if not show_info:
					dispatcher.utter_message(message)
				else:

					# TODO: set values properly
					# closedate
					status = response["status"]
					resolution = (
						response["solvedate"] if response["solvedate"] else "No disponible"
					)

					dispatcher.utter_message(
						"A continuación se encuentra la última información sobre su incidencia"
					)
					dispatcher.utter_message(
						template=UtteranceEnum.TICKET_STATUS,
						ticket_no=ticket_no,
						title=response["title"],
						category=response["category"],
						status=status,
						resolution=resolution,
						date_mod=response["date_mod"],
					)
			except GlpiException as e:
				logger.error(f"Error when trying to fetch ticket status: {ticket_no}", e)
				dispatcher.utter_message(template=UtteranceEnum.PROCESS_FAILED)

			events.append(SlotSet(EntitySlotEnum.TICKET_NO, None))
			events.append(SlotSet(EntitySlotEnum.EMAIL, None))

		return events
