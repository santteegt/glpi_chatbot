# -*- coding: utf-8 -*-

import logging
from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction, REQUESTED_SLOT
from rasa_sdk.events import AllSlotsReset, SlotSet, EventType
import re
from typing import Dict, Text, Any, List, Union, Optional

from actions import users_api
from actions.actions_base import request_next_slot
from actions.constants import (
    DTICApplication, EntitySlotEnum, GLPICategories, IntentEnum, TicketTypes,
    UtteranceEnum
)
from actions.glpi import GLPIService, GlpiException, load_glpi_config, Ticket
from actions.user_api import User
from actions.parsing import remove_accents

logger = logging.getLogger(__name__)

# Loading GLPI API config
glpi_api_uri, glpi_app_token, glpi_auth_token, glpi_local_mode = load_glpi_config()
glpi = (
    GLPIService.get_instance(glpi_api_uri, glpi_app_token, glpi_auth_token)
    if not glpi_local_mode
    else None
)


class CreateAppUserForm(FormAction):

    def name(self) -> Text:
        return "create_app_user_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""

        slots = [
            EntitySlotEnum.APPLICATION,
            EntitySlotEnum.PERSONAL_ID,
            EntitySlotEnum.EMAIL,

        ]
        if tracker.get_slot(EntitySlotEnum.APPLICATION) == DTICApplication.URKUND:
            slots.extend([
                EntitySlotEnum.FACULTY,
                EntitySlotEnum.ACCEPT_AGREEMENT,
            ])
        else:
            slots.extend([
                EntitySlotEnum.ROLE,
                EntitySlotEnum.CONFIRM,
            ])

        return slots

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""

        return {
            EntitySlotEnum.APPLICATION: [
                self.from_entity(entity=EntitySlotEnum.APPLICATION)
            ],
            EntitySlotEnum.PERSONAL_ID: [
                self.from_entity(entity=EntitySlotEnum.PERSONAL_ID),
                self.from_text(not_intent=IntentEnum.OUT_OF_SCOPE),
            ],
            EntitySlotEnum.EMAIL: self.from_entity(entity=EntitySlotEnum.EMAIL),
            EntitySlotEnum.FACULTY: [
                self.from_entity(entity=EntitySlotEnum.FACULTY),
                self.from_text(not_intent=IntentEnum.OUT_OF_SCOPE),
                # self.from_text(intent=[IntentEnum.INFORM]),
            ],
            EntitySlotEnum.ACCEPT_AGREEMENT: [
                self.from_intent(intent=IntentEnum.CONFIRM, value=True),
                self.from_intent(intent=IntentEnum.DENY, value=False),
            ],
            EntitySlotEnum.ROLE: [
                self.from_entity(entity=EntitySlotEnum.ROLE),
                self.from_text(not_intent=IntentEnum.OUT_OF_SCOPE),
            ],
            EntitySlotEnum.CONFIRM: [
                self.from_intent(intent=IntentEnum.CONFIRM, value=True),
                self.from_intent(intent=IntentEnum.DENY, value=False),
            ],
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

    def fetch_employee(self, identity: Text) -> (Optional[User], bool):
        """Fetch Users API using personal Id"""

        user_data = users_api.validate_user(identity=identity)
        # TODO: create ad-hoc metohod to validate user is employee => 'nombreGestor': 'GestorOpenLdap'
        is_employee = True
        return user_data, is_employee

    def validate_personal_id(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate personal_id has a valid value."""

        # TODO: Validate it is registered as employee
        user, is_employee = self.fetch_employee(value)
        if re.match(r"[0-9]+$", value) and user and is_employee:
            # validation succeeded
            return {
                EntitySlotEnum.PERSONAL_ID: value,
                EntitySlotEnum.FOUND_EMAIL: user['email']
            }
        else:
            dispatcher.utter_message(template=UtteranceEnum.NO_PERSONAL_ID)
            # validation failed, set this slot to None, meaning the
            # user will get info to connect to the guest network
            return {EntitySlotEnum.PERSONAL_ID: None}

    def validate_email(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        found_email = tracker.get_slot(EntitySlotEnum.FOUND_EMAIL)
        if found_email == value.lower():
            return {
                EntitySlotEnum.EMAIL: found_email,
                EntitySlotEnum.FOUND_EMAIL: None,
            }
        else:
            dispatcher.utter_message(template=UtteranceEnum.EMAIL_NO_MATCH)
            return {
                EntitySlotEnum.PERSONAL_ID: None,
                EntitySlotEnum.FOUND_EMAIL: None,
                EntitySlotEnum.EMAIL: None,
            }

    def validate_faculty(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        # if value is None:
        #     dispatcher.utter_message(template=UtteranceEnum.INVALID)
        email = tracker.get_slot(EntitySlotEnum.EMAIL)
        faculty = value.upper()
        data_confirmation = f""" - email: {email}
        - Faculty: {faculty}
        - [Terminos y Condiciones](https://drive.google.com/file/d/15enlmQJGg0nygWmclhjCvqPuMLCyzHwQ/view?usp=sharing)
        """
        return {
            EntitySlotEnum.FACULTY: faculty,
            EntitySlotEnum.AGREEMENT_REASON: "crear un usuario en URKUND",
            EntitySlotEnum.DATA_CONFIRMATION: data_confirmation
        }

    # def validate_role(
    #     self,
    #     value: Text,
    #     dispatcher: CollectingDispatcher,
    #     tracker: Tracker,
    #     domain: Dict[Text, Any],
    # ) -> Dict[Text, Any]:
    #     if value is None:
    #         dispatcher.utter_message(template=UtteranceEnum.INVALID)
    #     return {
    #         EntitySlotEnum.ROLE: value.upper()
    #     }

    def submit(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any],
    ) -> List[Dict]:
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
