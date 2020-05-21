# -*- coding: utf-8 -*-

import logging
from typing import Dict, Text, Any, List, Union
from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
from rasa_sdk.events import AllSlotsReset

import re

from actions.constants import EntitySlotEnum, IntentEnum, UtteranceEnum

logger = logging.getLogger(__name__)


class BiometricsReportForm(FormAction):
    def name(self) -> Text:
        return "biometrics_report_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""

        return [EntitySlotEnum.PERSONAL_ID, EntitySlotEnum.BIOMETRICS_ID]

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
            ]
        }

    @staticmethod
    def query_employee_db() -> List[Text]:
        """Database of supported wifi networks"""

        # TODO: Validate user is employee
        return ["0301861340"]

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
        dispatcher.utter_message(
            "This action will create a ticket for requesting a biometrics report with "
            + f"ID: {personal_id} BIO_ID: {biometrics_id}"
        )
        return [AllSlotsReset()]
