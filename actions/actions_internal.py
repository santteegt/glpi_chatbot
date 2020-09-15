# -*- coding: utf-8 -*-

import logging
from typing import Any, Dict, List, Optional, Text, Union
from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
from rasa_sdk.events import AllSlotsReset, SlotSet

import re

from actions import users_api
from actions.constants import EntitySlotEnum, GLPICategories, IntentEnum, TicketTypes, UtteranceEnum
from actions.glpi import GLPIService, GlpiException, load_glpi_config, Ticket
from actions.user_api import User
from actions.parsing import (
    get_entity_details,
    parse_duckling_time_as_interval,
    remove_accents,
)

logger = logging.getLogger(__name__)

# Loading GLPI API config
glpi_api_uri, glpi_app_token, glpi_auth_token, local_mode = load_glpi_config()
glpi = (
    GLPIService.get_instance(glpi_api_uri, glpi_app_token, glpi_auth_token)
    if not local_mode
    else None
)


class BiometricsReportForm(FormAction):
    def name(self) -> Text:
        return "biometrics_report_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""

        return [
            EntitySlotEnum.PERSONAL_ID,
            EntitySlotEnum.BIOMETRICS_ID,
            EntitySlotEnum.TIME_PERIOD,
        ]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""

        return {
            EntitySlotEnum.PERSONAL_ID: [
                self.from_entity(entity=EntitySlotEnum.PERSONAL_ID),
                self.from_text(not_intent=IntentEnum.OUT_OF_SCOPE),
            ],
            EntitySlotEnum.BIOMETRICS_ID: [
                self.from_entity(entity=EntitySlotEnum.BIOMETRICS_ID),
                self.from_text(not_intent=IntentEnum.OUT_OF_SCOPE),
            ],
            EntitySlotEnum.TIME_PERIOD: [self.from_entity(entity=EntitySlotEnum.TIME)],
        }

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
                EntitySlotEnum.EMAIL: user['email']
            }
        else:
            dispatcher.utter_message(template=UtteranceEnum.NO_PERSONAL_ID)
            # validation failed, set this slot to None, meaning the
            # user will get info to connect to the guest network
            return {EntitySlotEnum.PERSONAL_ID: None}

    def validate_biometrics_id(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate personal_id has a valid value."""

        # TODO: Validate it is registered
        if re.match(r"[0-9]{10}$", value) is not None:
            # validation succeeded
            return {EntitySlotEnum.BIOMETRICS_ID: value}
        else:
            dispatcher.utter_message(template=UtteranceEnum.INVALID)
            # validation failed, set this slot to None, meaning the
            # user will get info to connect to the guest network
            return {EntitySlotEnum.BIOMETRICS_ID: None}

    def validate_time_period(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate time value."""
        time_entity = get_entity_details(tracker, EntitySlotEnum.TIME)
        parsed_interval = parse_duckling_time_as_interval(time_entity)
        if not parsed_interval:
            dispatcher.utter_message(template=UtteranceEnum.INVALID)
            return {EntitySlotEnum.TIME_PERIOD: None}
        # Returns { EntitySlotEnum.START_TIME, EntitySlotEnum.END_TIME, EntitySlotEnum.GRAIN }
        return parsed_interval

    def submit(
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

        return [AllSlotsReset(), SlotSet(EntitySlotEnum.TICKET_NO, ticket_id)]
