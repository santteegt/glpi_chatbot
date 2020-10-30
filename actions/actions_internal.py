# -*- coding: utf-8 -*-

import logging
from typing import Any, Dict, List, Text
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import AllSlotsReset, SlotSet

from actions.constants import EntitySlotEnum, GLPICategories, TicketTypes, UtteranceEnum
from actions.glpi import GLPIService, GlpiException, load_glpi_config, Ticket
from actions.parsing import remove_accents

logger = logging.getLogger(__name__)

# Loading GLPI API config
glpi_api_uri, glpi_app_token, glpi_auth_token, local_mode = load_glpi_config()
glpi = (
    GLPIService.get_instance(glpi_api_uri, glpi_app_token, glpi_auth_token)
    if not local_mode
    else None
)


class BiometricsReportForm(Action):
    def name(self) -> Text:
        return "action_biometrics_report"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any],
    ) -> List[Dict]:
        """Define what the form has to do
            after all required slots are filled"""

        personal_id = tracker.get_slot(EntitySlotEnum.PERSONAL_ID)
        email = tracker.get_slot(EntitySlotEnum.EMAIL)
        biometrics_id = tracker.get_slot(EntitySlotEnum.BIOMETRICS_ID)

        start_time = tracker.get_slot(EntitySlotEnum.START_TIME)
        end_time = tracker.get_slot(EntitySlotEnum.END_TIME)
        grain = tracker.get_slot(EntitySlotEnum.GRAIN)

        events = [
            SlotSet(EntitySlotEnum.ITILCATEGORY_ID, None),
            SlotSet(EntitySlotEnum.PERSONAL_ID, None),
            SlotSet(EntitySlotEnum.EMAIL, None),
            SlotSet(EntitySlotEnum.BIOMETRICS_ID, None),
            SlotSet(EntitySlotEnum.TIME, None),
            SlotSet(EntitySlotEnum.TIME_PERIOD, None),
            SlotSet(EntitySlotEnum.START_TIME, None),
            SlotSet(EntitySlotEnum.END_TIME, None),
            SlotSet(EntitySlotEnum.GRAIN, None),
        ]

        description = f"Datos de Validacion: \n ID: {personal_id}\n BIOMETRICS_ID: {biometrics_id}\n"
        description += f"Periodo: {start_time} / {end_time} ({grain})"

        ticket: Ticket = Ticket(
            {
                "username": "normal",  # TODO: set the actual logged in user
                "title": "Solicitud Informe Sistema Biometrico",
                "description": remove_accents(description),
                # 'priority': glpi_priority
                "itilcategories_id": GLPICategories.DATA_REPORT,
            }
        )
        if email:
            ticket['alternative_email'] = email

        if local_mode:
            dispatcher.utter_message(
                f"Esta acción crearía un ticket con la siguiente información: {ticket}"
            )
            ticket_id = "DUMMY"
            events.append(SlotSet(EntitySlotEnum.TICKET_NO, ticket_id))
        else:
            try:
                response = glpi.create_ticket(ticket, ticket_type=TicketTypes.REQUEST)
                ticket_id = response["id"]
                # This is not actually required as its value is sent directly to the utter_message
                events.append(SlotSet(EntitySlotEnum.TICKET_NO, ticket_id))
            except GlpiException as e:
                logger.error("Error when trying to create a ticket", e)
                logger.error(f"Ticket: {ticket}")
                dispatcher.utter_message(template=UtteranceEnum.PROCESS_FAILED)
                return events
        dispatcher.utter_message(template=UtteranceEnum.TICKET_NO, ticket_no=ticket_id)
        dispatcher.utter_message(template=UtteranceEnum.CONFIRM_REQUEST)

        # return events
        return [AllSlotsReset(), SlotSet(EntitySlotEnum.TICKET_NO, ticket_id)]
