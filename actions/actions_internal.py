# -*- coding: utf-8 -*-

import logging
from typing import Dict, Text, Any, List, Union
from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
from rasa_sdk.events import AllSlotsReset, SlotSet

import re

from actions.constants import EntitySlotEnum, IntentEnum, UtteranceEnum
from actions.glpi import GLPIService, GlpiException, load_glpi_config, Ticket
from actions.parsing import get_entity_details, parse_duckling_time_as_interval, remove_accents

logger = logging.getLogger(__name__)

glpi_api_uri, glpi_app_token, glpi_auth_token, local_mode = load_glpi_config()
glpi = GLPIService.get_instance(glpi_api_uri, glpi_app_token, glpi_auth_token)


class BiometricsReportForm(FormAction):
    def name(self) -> Text:
        return "biometrics_report_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""

        return [
            EntitySlotEnum.PERSONAL_ID,
            EntitySlotEnum.BIOMETRICS_ID,
            EntitySlotEnum.TIME
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
            EntitySlotEnum.TIME: [
                self.from_entity(entity=EntitySlotEnum.TIME)
            ]
        }

    @staticmethod
    def query_employee_db() -> List[Text]:
        """Database of supported wifi networks"""

        # TODO: Validate user is employee
        return ["1111111111"]

    def validate_personal_id(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate personal_id has a valid value."""

        # TODO: Validate it is registered as employee
        if (
            re.match(r"[0-9]+$", value) is not None
            and value in self.query_employee_db()
        ):
            # validation succeeded
            return {EntitySlotEnum.PERSONAL_ID: value}
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

    def validate_time(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate time value."""
        time_entity = get_entity_details(tracker, "time")
        parsed_interval = parse_duckling_time_as_interval(time_entity)
        if not parsed_interval:
            dispatcher.utter_message(template="utter_no_transactdate")
            return {EntitySlotEnum.TIME: None}
        # Returns { EntitySlotEnum.START_TIME, EntitySlotEnum.END_TIME, EntitySlotEnum.GRAIN }
        return parsed_interval

    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        """Define what the form has to do
            after all required slots are filled"""

        personal_id = tracker.get_slot(EntitySlotEnum.PERSONAL_ID)
        biometrics_id = tracker.get_slot(EntitySlotEnum.BIOMETRICS_ID)

        start_time = tracker.get_slot(EntitySlotEnum.START_TIME)
        end_time = tracker.get_slot(EntitySlotEnum.END_TIME)
        grain = tracker.get_slot(EntitySlotEnum.GRAIN)

        events = [SlotSet(EntitySlotEnum.PERSONAL_ID, None),
                  SlotSet(EntitySlotEnum.BIOMETRICS_ID, None),
                  SlotSet(EntitySlotEnum.TIME, None),
                  SlotSet(EntitySlotEnum.START_TIME, None),
                  SlotSet(EntitySlotEnum.END_TIME, None),
                  SlotSet(EntitySlotEnum.GRAIN, None)]

        description = f'Datos de Validacion: \n ID: {personal_id}\n BIOMETRICS_ID: {biometrics_id}\n'
        description += f'Periodo: {start_time} / {end_time} ({grain})'

        ticket: Ticket = Ticket({
            'username': 'normal',  # TODO: set the actual logged in user
            'title': 'Solicitud Informe Sistema Biometrico',
            'description': remove_accents(description),
            # 'priority': glpi_priority
            'itilcategories_id': 60  # Reporte de datos
        })

        try:
            response = glpi.create_ticket(ticket, ticket_type=2)  # Solicitud
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
        # dispatcher.utter_message(
        #     "This action will create a ticket for requesting a biometrics report with "
        #     + f"ID: {personal_id} BIO_ID: {biometrics_id}"
        # )
        # return [AllSlotsReset()]
        return events