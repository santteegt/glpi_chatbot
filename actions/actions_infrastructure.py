# -*- coding: utf-8 -*-

import logging
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from typing import Any, Dict, List, Text

from actions.constants import (
    DTICApplication, EntitySlotEnum, GLPICategories, TicketTypes, UtteranceEnum
)
from actions.glpi import GLPIService, GlpiException, load_glpi_config, Ticket
from actions.parsing import remove_accents

logger = logging.getLogger(__name__)

# Loading GLPI API config
glpi_api_uri, glpi_app_token, glpi_auth_token, glpi_local_mode = load_glpi_config()
glpi = (
    GLPIService.get_instance(glpi_api_uri, glpi_app_token, glpi_auth_token)
    if not glpi_local_mode
    else None
)


class CreateAppUser(Action):

    def name(self) -> Text:
        return "action_create_app_user"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        """Define what the form has to do
            after all required slots are filled"""

        events = [
            SlotSet(EntitySlotEnum.APPLICATION, None),
            SlotSet(EntitySlotEnum.PERSONAL_ID, None),
            SlotSet(EntitySlotEnum.EMAIL, None),
            SlotSet(EntitySlotEnum.FACULTY, None),
            SlotSet(EntitySlotEnum.AGREEMENT_REASON, None),
            SlotSet(EntitySlotEnum.DATA_CONFIRMATION, None),
            SlotSet(EntitySlotEnum.ACCEPT_AGREEMENT, None),
            SlotSet(EntitySlotEnum.ROLE, None),
            SlotSet(EntitySlotEnum.CONFIRM, None),
        ]

        application = tracker.get_slot(EntitySlotEnum.APPLICATION)
        confirm = tracker.get_slot(EntitySlotEnum.ACCEPT_AGREEMENT) \
            if application == DTICApplication.URKUND \
            else tracker.get_slot(EntitySlotEnum.CONFIRM)

        if confirm:
            personal_id = tracker.get_slot(EntitySlotEnum.PERSONAL_ID)
            email = tracker.get_slot(EntitySlotEnum.EMAIL)
            faculty = tracker.get_slot(EntitySlotEnum.FACULTY) if application == DTICApplication.URKUND else None
            role = tracker.get_slot(EntitySlotEnum.ROLE) if application != DTICApplication.URKUND else None

            description = f"Informacion de usuario: \n ID: {personal_id}\n EMAIL: {email}\n"
            if application in [DTICApplication.URKUND]:
                description += f"Facultad: {faculty.upper()}"
            else:
                description += f"Rol: {role.upper()}"

            ticket: Ticket = Ticket(
                {
                    "username": "normal",  # TODO: set the actual logged in user
                    "title": f"Creacion de Usuario en {application.upper()}",
                    "description": remove_accents(description),
                    # 'priority': glpi_priority
                    "itilcategories_id": GLPICategories.USER_MGMT,
                    "alternative_email": email
                }
            )

            if glpi_local_mode:
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
        else:
            events.append(SlotSet(EntitySlotEnum.TICKET_NO, None))
            dispatcher.utter_message(template=UtteranceEnum.PROCESS_CANCELLED)

        return events
        # return [AllSlotsReset(), SlotSet(EntitySlotEnum.TICKET_NO, ticket_id)]
