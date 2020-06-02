# -*- coding: utf-8 -*-

import logging
from typing import Dict, Text, Any, List, Union
from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
from rasa_sdk.events import SlotSet

import re

from actions.actions_base import ask_if_success
from actions.constants import EntitySlotEnum, IntentEnum, UtteranceEnum

logger = logging.getLogger(__name__)


class WifiFaqForm(FormAction):
    def name(self) -> Text:
        return "wifi_faq_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""

        # logger.info(f'Current WIFI NET: {tracker.get_slot(EntitySlotEnum.WIFI_NETWORK)}')
        # TODO: check why it isn't asking for an email

        if (
            tracker.get_slot(EntitySlotEnum.WIFI_NETWORK)
            in WifiFaqForm.wifi_network_db()[:2]
        ):
            return [EntitySlotEnum.WIFI_NETWORK, EntitySlotEnum.EMAIL]
        else:
            return [EntitySlotEnum.WIFI_NETWORK]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""

        return {
            EntitySlotEnum.EMAIL: self.from_entity(
                entity=EntitySlotEnum.EMAIL
            ),
            EntitySlotEnum.WIFI_NETWORK: [
                self.from_entity(entity=EntitySlotEnum.WIFI_NETWORK),
                self.from_text(intent=[IntentEnum.CONNECT_WIFI, IntentEnum.INFORM]),
            ],
        }

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

    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        """Define what the form has to do
            after all required slots are filled"""

        wifi_network = tracker.get_slot(EntitySlotEnum.WIFI_NETWORK).lower()
        wifi_networks = self.wifi_network_db()
        instructions = {
            wifi_networks[0]: UtteranceEnum.EDUROAM_INSTRUCTIONS,
            wifi_networks[1]: UtteranceEnum.UCWIFI_INSTRUCTIONS,
            wifi_networks[2]: UtteranceEnum.GUEST_WIFI_INSTRUCTIONS,
        }

        dispatcher.utter_message(template=instructions[wifi_network])

        ask_if_success(dispatcher, incident_title="Problema de conexion a la red WIFI", itilcategory_id=52)

        return [SlotSet(EntitySlotEnum.WIFI_NETWORK, None)]


class CreateUserFaqForm(FormAction):
    def name(self) -> Text:
        return "create_user_faq_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""

        if tracker.get_slot(EntitySlotEnum.HAS_EMAIL):
            return [EntitySlotEnum.HAS_EMAIL]
        else:
            return [EntitySlotEnum.HAS_EMAIL, EntitySlotEnum.COURSE_TYPE]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""

        return {
            EntitySlotEnum.HAS_EMAIL: [
                self.from_intent(intent="confirm", value=True),
                self.from_intent(intent="deny", value=False),
            ],
            EntitySlotEnum.COURSE_TYPE: [
                self.from_entity(entity=EntitySlotEnum.COURSE_TYPE),
            ]
        }

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

    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        """Define what the form has to do
            after all required slots are filled"""

        has_email = tracker.get_slot(EntitySlotEnum.HAS_EMAIL)
        if has_email:
            dispatcher.utter_message(template=UtteranceEnum.RECOVER_PASSWORD)
        else:
            course_type = tracker.get_slot(EntitySlotEnum.COURSE_TYPE)
            course_types = self.course_type_db()
            instructions = {
                course_types[0]: "https://admision.ucuenca.edu.ec/",
                course_types[1]: "https://registro.ucuenca.edu.ec/",
            }

            dispatcher.utter_message(
                "Para poder registrar una cuenta por favor visita el siguiente enlace: "
                + instructions[course_type]
            )

        ask_if_success(dispatcher, incident_title="Problema para crear un usuario", itilcategory_id=56)

        return [
            SlotSet(EntitySlotEnum.COURSE_TYPE, None),
            SlotSet(EntitySlotEnum.HAS_EMAIL, None)
        ]
