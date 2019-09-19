# -*- coding: utf-8 -*-

import logging
import random
from typing import Text, List, Dict, Any, Union, Optional
from rasa_sdk import Tracker
from rasa_sdk import Action
from rasa_sdk.events import SlotSet
from rasa_sdk.forms import FormAction
from rasa_sdk.executor import CollectingDispatcher

logger = logging.getLogger(__name__)


class ComputeResourceForm(FormAction):
    """Contextual ActionForm to handle Compute Resources requests"""

    DEPARTMENT: Text = "departamento"
    ENVIRONMENT: Text = "entorno"
    RAM: Text = "ram"
    CPU_CORES: Text = "cpu_cores"
    DISK_SPACE: Text = "disk_space"
    SCALABILITY: Text = "escalabilidad"
    OBSERVATIONS: Text = "observaciones"

    def name(self) -> Text:
        """Unique identifier of the form"""

        return "compute_resource_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""

        # if environment == production
        if tracker.get_slot(ComputeResourceForm.ENVIRONMENT) == ComputeResourceForm.valid_environment_types()[2]:
            return [
                # ComputeResourceForm.DEPARTMENT,
                ComputeResourceForm.ENVIRONMENT, ComputeResourceForm.RAM,
                ComputeResourceForm.CPU_CORES, ComputeResourceForm.DISK_SPACE, ComputeResourceForm.SCALABILITY,
                ComputeResourceForm.OBSERVATIONS
            ]
        else:
            return [
                # ComputeResourceForm.DEPARTMENT,
                ComputeResourceForm.ENVIRONMENT, ComputeResourceForm.RAM,
                ComputeResourceForm.CPU_CORES, ComputeResourceForm.DISK_SPACE, ComputeResourceForm.OBSERVATIONS
            ]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""

        return {
            # ComputeResourceForm.DEPARTMENT: self.from_entity(entity=ComputeResourceForm.DEPARTMENT,
            #                                                  not_intent="chitchat"),
            ComputeResourceForm.ENVIRONMENT: self.from_entity(entity=ComputeResourceForm.ENVIRONMENT,
                                                              not_intent="chitchat"),
            ComputeResourceForm.RAM: self.from_entity(entity=ComputeResourceForm.RAM,
                                                      not_intent="chitchat"),
            ComputeResourceForm.CPU_CORES: self.from_entity(entity=ComputeResourceForm.CPU_CORES,
                                                            not_intent="chitchat"),
            ComputeResourceForm.DISK_SPACE: self.from_entity(entity=ComputeResourceForm.DISK_SPACE,
                                                             not_intent="chitchat"),
            ComputeResourceForm.SCALABILITY: [
                self.from_entity(entity=ComputeResourceForm.SCALABILITY),
                self.from_intent(intent="confirmar", value=True),
                self.from_intent(intent="cancelar", value=False),
            ],
            ComputeResourceForm.OBSERVATIONS: [
                self.from_entity(entity=ComputeResourceForm.OBSERVATIONS), self.from_text()
            ],

        }

    @staticmethod
    def valid_environment_types() -> List[Text]:
        """Database of supported environment types"""

        return [
            "desarrollo",
            "pruebas",
            "produccion"
        ]

    @staticmethod
    def is_int(string: Text) -> bool:
        """Check if a string is an integer"""

        try:
            int(string)
            return True
        except ValueError:
            return False

    @staticmethod
    def is_within_bound(value: int, lower_bount: int, upper_bound: int) -> bool:
        """Check if an int value is within a specified bound"""

        return True if lower_bount <= value <= upper_bound else False

    def validate_entorno(self, value: Text, dispatcher: CollectingDispatcher, tracker: Tracker,
                             domain: Dict[Text, Any]) -> Optional[Text]:
        """Validate environment value"""

        if value.lower() in self.valid_environment_types():
            # validation succeeded, set the value of the "cuisine" slot to value
            return {ComputeResourceForm.ENVIRONMENT: value}
        else:
            dispatcher.utter_template("utter_no_valido", tracker)
            # validation failed, set this slot to None, meaning the
            # user will be asked for the slot again
            return {ComputeResourceForm.ENVIRONMENT: None}

    def validate_ram(self, value: Text, dispatcher: CollectingDispatcher, tracker: Tracker,
                             domain: Dict[Text, Any]) -> Optional[Text]:
        """Validate ram value"""

        if self.is_int(value) and self.is_within_bound(int(value), 8, 64):
            return {ComputeResourceForm.RAM: value}
        else:
            dispatcher.utter_template("utter_no_valido", tracker)
            return {ComputeResourceForm.RAM: None}

    def validate_cpu_cores(self, value: Text, dispatcher: CollectingDispatcher, tracker: Tracker,
                     domain: Dict[Text, Any]) -> Optional[Text]:
        """Validate CPU cores value"""

        if self.is_int(value) and self.is_within_bound(int(value), 1, 8):
            return {ComputeResourceForm.CPU_CORES: value}
        else:
            dispatcher.utter_template("utter_no_valido", tracker)
            return {ComputeResourceForm.CPU_CORES: None}

    def validate_disk_space(self, value: Text, dispatcher: CollectingDispatcher, tracker: Tracker,
                     domain: Dict[Text, Any]) -> Optional[Text]:
        """Validate disk space value"""

        if self.is_int(value) and self.is_within_bound(int(value), 8, 1000):
            return {ComputeResourceForm.DISK_SPACE: value}
        else:
            dispatcher.utter_template("utter_no_numero", tracker)
            return {ComputeResourceForm.DISK_SPACE: None}

    def validate_escalabilidad(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Any:
        """Validate scalability value and set it to NO by default"""

        if isinstance(value, str):
            return {ComputeResourceForm.SCALABILITY: value}
        else:
            return {ComputeResourceForm.SCALABILITY: "No"}

    def submit(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict]:
        """Define what the form has to do after all required slots are filled"""

        # TODO: do something with the request
        ticket_no: Text = "{:04d}".format(random.randint(1, 1000))
        # utter submit template
        # dispatcher.utter_template("utter_compute_form_values", tracker)
        # dispatcher.utter_message("Nro de ticket: {:s}".format(ticket_no))
        # return [SlotSet("ticket_no", ticket_no), SlotSet(self.DEPARTMENT, None), SlotSet(self.ENVIRONMENT, None),
        #         SlotSet(self.RAM, None), SlotSet(self.CPU_CORES, None), SlotSet(self.DISK_SPACE, None),
        #         SlotSet(self.SCALABILITY, None), SlotSet(self.OBSERVATIONS, None)]
        return [SlotSet("ticket_no", ticket_no)]
