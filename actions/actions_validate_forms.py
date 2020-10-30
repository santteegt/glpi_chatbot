# -*- coding: utf-8 -*-

import logging
from rasa_sdk import Tracker, FormValidationAction
from rasa_sdk.events import EventType, SlotSet
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import REQUESTED_SLOT
import re
from typing import Any, Dict, List, Optional, Text

from actions import users_api
from actions.constants import EntitySlotEnum, IntentEnum, UtteranceEnum, DTICApplication
from actions.glpi import load_glpi_config
from actions.parsing import (
    get_entity_details,
    parse_duckling_time_as_interval,
)
from actions.user_api import User

logger = logging.getLogger(__name__)

# Loading GLPI API config
_, _, _, glpi_local_mode = load_glpi_config()
# glpi_api_uri, glpi_app_token, glpi_auth_token, glpi_local_mode = load_glpi_config()
# glpi = (
#     GLPIService.get_instance(glpi_api_uri, glpi_app_token, glpi_auth_token)
#     if not glpi_local_mode
#     else None
# )


class ValidateFormBase(FormValidationAction):
    """
        Base class for applying Form validation
    """

    def name(self) -> Text:
        return "validate_base_form"  # this form does not exist. It is just an abstract class

    def validate_ticket_no(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate email is in ticket system."""
        if glpi_local_mode:
            return {EntitySlotEnum.TICKET_NO: value}

        # logger.info(f'ticket value => {value}:{type(value)}')

        if re.match(r"^[0-9]+$", f'{value}') is not None:
            return {EntitySlotEnum.TICKET_NO: value}
        else:
            dispatcher.utter_message(template=UtteranceEnum.INVALID)
            # validation failed, set this slot to None, meaning the
            # user will get info to connect to the guest network
            return {EntitySlotEnum.TICKET_NO: None}

    def validate_email(
            self,
            slot_value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate email is in ticket system."""

        # Intents that we should validate email
        # intents = [
        #     IntentEnum.PROBLEM_EMAIL,
        #     IntentEnum.PASSWORD_RESET,
        # ]
        filter_intents = [
            IntentEnum.OPEN_INCIDENT,  # should allow anyone to report an incident
            IntentEnum.GET_INCIDENT_STATUS,  # email is validated with glpi records
            # in case user don't have a institutional email and want's to open incident from FAQs
            IntentEnum.DENY,
        ]
        trigger_intent = dict(tracker.active_loop)['trigger_message']['intent']['name']
        # logger.info(f"intent: {trigger_intent} in {intents} ?")
        logger.info(f"intent: {trigger_intent} in {filter_intents} ?")
        if not users_api or trigger_intent in filter_intents:
            return {EntitySlotEnum.EMAIL: slot_value.lower()}

        user = users_api.validate_user(email=slot_value.lower())
        logger.info(f'user for {slot_value.lower()}: {user}')
        if user:
            return {EntitySlotEnum.EMAIL: slot_value.lower()}
        else:
            dispatcher.utter_message(template=UtteranceEnum.EMAIL_NO_MATCH)
            return {EntitySlotEnum.EMAIL: None}

    def fetch_employee(self, identity: Text) -> (Optional[User], bool):
        """Fetch Users API using personal Id"""

        user_data = users_api.validate_user(identity=identity)
        # TODO: create ad-hoc metohod to validate user is employee => 'nombreGestor': 'GestorOpenLdap'
        is_employee = False
        return user_data, is_employee

    def validate_personal_id(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate personal_id has a valid value."""
        # logger.info('VALIDATE_PERSONAL_ID')

        # TODO: Validate it is registered as employee is a requirement. Set it as another slot
        user, is_employee = self.fetch_employee(value)
        # if re.match(r"[0-9]+$", value) and user and is_employee:
        if re.match(r"[0-9]+$", value) and user:
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


# class ValidateIncidentForm(FormValidationAction):
class ValidateOpenIncidentForm(ValidateFormBase):
    def name(self) -> Text:
        return "validate_open_incident_form"

    # def validate_email(
    #         self,
    #         slot_value: Text,
    #         dispatcher: CollectingDispatcher,
    #         tracker: Tracker,
    #         domain: Dict[Text, Any],
    # ) -> Dict[Text, Any]:
    #     """Validate email is in ticket system."""
    #
    #     # # Intents that we should validate email
    #     # intents = [
    #     #     IntentEnum.PROBLEM_EMAIL,
    #     #     IntentEnum.PASSWORD_RESET,
    #     # ]
    #     # trigger_intent = dict(tracker.active_loop)['trigger_message']['intent']['name']
    #     # logger.info(f"intent: {trigger_intent} in {intents} ?")
    #     # if not users_api or trigger_intent not in intents:
    #     #     return {EntitySlotEnum.EMAIL: slot_value.lower()}
    #
    #     user = users_api.validate_user(email=slot_value.lower())
    #     logger.info(f'user for {slot_value.lower()}: {user}')
    #     if user:
    #         return {EntitySlotEnum.EMAIL: slot_value.lower()}
    #     else:
    #         dispatcher.utter_message(template=UtteranceEnum.EMAIL_NO_MATCH)
    #         return {EntitySlotEnum.EMAIL: None}


class ValidateIncidentStatusForm(ValidateFormBase):
    def name(self) -> Text:
        return "validate_incident_status_form"


class ValidateBiometricsReportForm(ValidateFormBase):
    def name(self) -> Text:
        return "validate_biometrics_report_form"


class ValidateCreateAppUserForm(ValidateFormBase):
    def name(self) -> Text:
        return "validate_create_app_user_form"

    def validate_email(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """
            Override validate_email. This validation is crosschecked with user data fetched by id
        :param value:
        :param dispatcher:
        :param tracker:
        :param domain:
        :return:
        """
        # logger.info('VALIDATE EMAIL SUBCLASS')
        found_email = tracker.slots.get(EntitySlotEnum.FOUND_EMAIL)
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
        # logger.info("VALIDATE FACULTY")
        # if value is None:
        #     dispatcher.utter_message(template=UtteranceEnum.INVALID)
        email = tracker.slots.get(EntitySlotEnum.EMAIL)
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

    async def run(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:

        slots = await self.validate(dispatcher, tracker, domain)
        app_name = tracker.slots.get(EntitySlotEnum.APPLICATION)

        if len([True for slot in slots if slot["value"] is None]) > 0:
            # logger.info("SOME THINGS NEED VALIDATION")
            return slots

        if app_name is None:
            return [SlotSet(REQUESTED_SLOT, EntitySlotEnum.APPLICATION)] + slots
        else:
            required_slots = [
                EntitySlotEnum.PERSONAL_ID,
                EntitySlotEnum.EMAIL,
            ]

            if app_name == DTICApplication.URKUND:
                required_slots.extend([
                    EntitySlotEnum.FACULTY,
                    EntitySlotEnum.ACCEPT_AGREEMENT,
                ])
            else:
                required_slots.extend([
                    EntitySlotEnum.ROLE,
                    EntitySlotEnum.CONFIRM,
                ])

            for slot_name in required_slots:
                if tracker.slots.get(slot_name) is None:
                    # The slot is not filled yet. Request the user to fill this slot next.
                    return [SlotSet(REQUESTED_SLOT, slot_name)] + slots

        # All slots are filled.
        return [SlotSet(REQUESTED_SLOT, None)] + slots
