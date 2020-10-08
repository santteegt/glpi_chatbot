# -*- coding: utf-8 -*-

import logging
from typing import Text, List, Dict, Any, Union, Optional
from rasa_sdk import Tracker
from rasa_sdk.events import EventType, SlotSet
from rasa_sdk.forms import FormAction
from rasa_sdk.executor import CollectingDispatcher

from actions.actions_base import request_next_slot
from actions.constants import EntitySlotEnum, IntentEnum, UtteranceEnum
from actions.glpi import GLPIService, GlpiException, load_glpi_config, Ticket
from actions.parsing import remove_accents

logger = logging.getLogger(__name__)

glpi_api_uri, glpi_app_token, glpi_auth_token, local_mode = load_glpi_config()
glpi = (
    GLPIService.get_instance(glpi_api_uri, glpi_app_token, glpi_auth_token)
    if not local_mode
    else None
)


class ComputeResourceForm(FormAction):
    """Contextual ActionForm to handle Compute Resources requests
        CURRENTLY unused!
    """

    def name(self) -> Text:
        """Unique identifier of the form"""

        return "compute_resource_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""

        # if environment == production
        if (
            tracker.get_slot(EntitySlotEnum.VM_ENVIRONMENT)
            == ComputeResourceForm.valid_environment_types()[2]
        ):
            return [
                EntitySlotEnum.DEPARTMENT,
                EntitySlotEnum.VM_ENVIRONMENT,
                EntitySlotEnum.VM_RAM,
                EntitySlotEnum.VM_CPU_CORES,
                EntitySlotEnum.VM_DISK_SPACE,
                EntitySlotEnum.VM_SCALABILITY,
                EntitySlotEnum.OBSERVATIONS,
                EntitySlotEnum.CONFIRM,
            ]
        else:
            return [
                EntitySlotEnum.DEPARTMENT,
                EntitySlotEnum.VM_ENVIRONMENT,
                EntitySlotEnum.VM_RAM,
                EntitySlotEnum.VM_CPU_CORES,
                EntitySlotEnum.VM_DISK_SPACE,
                EntitySlotEnum.OBSERVATIONS,
                EntitySlotEnum.CONFIRM,
            ]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        """A dictionary to map required slots to
			- an extracted entity
			- intent: value pairs
			- a whole message
			or a list of them, where a first match will be picked"""

        return {
            EntitySlotEnum.DEPARTMENT: [
                self.from_entity(
                    entity=EntitySlotEnum.DEPARTMENT, not_intent=IntentEnum.OUT_OF_SCOPE,
                ),
                self.from_text(),
            ],
            EntitySlotEnum.VM_ENVIRONMENT: self.from_entity(
                entity=EntitySlotEnum.VM_ENVIRONMENT, not_intent=IntentEnum.OUT_OF_SCOPE,
            ),
            EntitySlotEnum.VM_RAM: self.from_entity(
                entity=EntitySlotEnum.VM_RAM, not_intent=IntentEnum.OUT_OF_SCOPE,
            ),
            EntitySlotEnum.VM_CPU_CORES: self.from_entity(
                entity=EntitySlotEnum.VM_CPU_CORES, not_intent=IntentEnum.OUT_OF_SCOPE,
            ),
            EntitySlotEnum.VM_DISK_SPACE: self.from_entity(
                entity=EntitySlotEnum.VM_DISK_SPACE, not_intent=IntentEnum.OUT_OF_SCOPE,
            ),
            EntitySlotEnum.VM_SCALABILITY: [
                self.from_entity(
                    entity=EntitySlotEnum.VM_SCALABILITY,
                    not_intent=IntentEnum.OUT_OF_SCOPE,
                ),
                self.from_intent(intent=IntentEnum.CONFIRM, value=True),
                self.from_intent(intent=IntentEnum.DENY, value=False),
            ],
            EntitySlotEnum.OBSERVATIONS: [
                self.from_entity(entity=EntitySlotEnum.OBSERVATIONS),
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

    @staticmethod
    def valid_environment_types() -> List[Text]:
        """Database of supported environment types"""

        return ["desarrollo", "pruebas", "produccion"]

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

    def validate_vm_environment(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate vm_environment value"""

        if value.lower() in self.valid_environment_types():
            # validation succeeded, set the value of the "cuisine" slot to value
            return {EntitySlotEnum.VM_ENVIRONMENT: value}
        else:
            dispatcher.utter_message(template=UtteranceEnum.INVALID)
            # validation failed, set this slot to None, meaning the
            # user will be asked for the slot again
            return {EntitySlotEnum.VM_ENVIRONMENT: None}

    def validate_vm_ram(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate ram value"""

        if self.is_int(value) and self.is_within_bound(int(value), 8, 64):
            return {EntitySlotEnum.VM_RAM: value}
        else:
            dispatcher.utter_message(template=UtteranceEnum.INVALID)
            return {EntitySlotEnum.VM_RAM: None}

    def validate_vm_cpu_cores(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate CPU cores value"""

        if self.is_int(value) and self.is_within_bound(int(value), 1, 8):
            return {EntitySlotEnum.VM_CPU_CORES: value}
        else:
            dispatcher.utter_message(template=UtteranceEnum.INVALID)
            return {EntitySlotEnum.VM_CPU_CORES: None}

    def validate_vm_disk_space(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate disk space value"""

        if self.is_int(value) and self.is_within_bound(int(value), 8, 1000):
            return {EntitySlotEnum.VM_DISK_SPACE: value}
        else:
            dispatcher.utter_message(template=UtteranceEnum.INVALID)
            return {EntitySlotEnum.VM_DISK_SPACE: None}

    def validate_vm_scalability(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate scalability value and set it to NO by default"""

        if isinstance(value, str):
            return {EntitySlotEnum.VM_SCALABILITY: value}
        else:
            return {EntitySlotEnum.VM_SCALABILITY: "No"}

    def submit(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any],
    ) -> List[Dict]:
        """Define what the form has to do after all required slots are filled"""

        department = tracker.get_slot(EntitySlotEnum.DEPARTMENT)
        vm_environment = tracker.get_slot(EntitySlotEnum.VM_ENVIRONMENT)
        vm_ram = tracker.get_slot(EntitySlotEnum.VM_RAM)
        vm_cpu_cores = tracker.get_slot(EntitySlotEnum.VM_CPU_CORES)
        vm_disk_space = tracker.get_slot(EntitySlotEnum.VM_DISK_SPACE)
        vm_scalability = tracker.get_slot(EntitySlotEnum.VM_SCALABILITY)
        observations = tracker.get_slot(EntitySlotEnum.OBSERVATIONS)

        request_description = (
            "Solicito una maquina virtual con las siguientes caracteristicas: "
            + f"Departamento: {department} ||"
            + f"Entorno: {vm_environment} ||"
            + f"Memoria RAM: {vm_ram} ||"
            + f"No CPUs: {vm_cpu_cores} ||"
            + f"Disco duro: {vm_disk_space} Gb ||"
            + f"Escalabilidad: {vm_scalability if vm_scalability is not None else 'No'} ||"
            + f"Observaciones: {observations}"
        )

        logger.info(f"{self.name()}: {request_description}")

        events = [
            SlotSet(EntitySlotEnum.ITILCATEGORY_ID, None),
            SlotSet(EntitySlotEnum.DEPARTMENT, None),
            SlotSet(EntitySlotEnum.VM_ENVIRONMENT, None),
            SlotSet(EntitySlotEnum.VM_RAM, None),
            SlotSet(EntitySlotEnum.VM_CPU_CORES, None),
            SlotSet(EntitySlotEnum.VM_DISK_SPACE, None),
            SlotSet(EntitySlotEnum.VM_SCALABILITY, None),
            SlotSet(EntitySlotEnum.OBSERVATIONS, None),
        ]

        if tracker.get_slot(EntitySlotEnum.CONFIRM):
            # priorities = GLPIService.priority_values()
            # priority_values = list(priorities.keys())
            # glpi_priority = priorities[priority_values[1]]  # media
            ticket: Ticket = Ticket(
                {
                    "username": "normal",  # TODO: set the actual logged in user
                    "title": "Peticion de Maquina Virtual",
                    "description": remove_accents(request_description),
                    # 'priority': glpi_priority
                    "itilcategories_id": 54,  # Equipos de computo
                }
            )
            if local_mode:
                dispatcher.utter_message(
                    f"Esta acción crearía un ticket con la siguiente información: {ticket}"
                )
                ticket_id: Text = "DUMMY"
                events.append(SlotSet(EntitySlotEnum.TICKET_NO, ticket_id))
            else:  # TODO: integrate with GLPI
                try:
                    response = glpi.create_ticket(ticket, ticket_type=2)  # Solicitud
                    ticket_id = response["id"]
                    # This is not actually required as its value is sent directly to the utter_message
                    events.append(SlotSet(EntitySlotEnum.TICKET_NO, ticket_id))
                except GlpiException as e:
                    logger.error("Error when trying to create a ticket", e)
                    logger.error(f"Ticket: {ticket}")
                    dispatcher.utter_message(template=UtteranceEnum.PROCESS_FAILED)
                    return events
            dispatcher.utter_message(
                template=UtteranceEnum.TICKET_NO, ticket_no=ticket_id
            )
            dispatcher.utter_message(template=UtteranceEnum.CONFIRM_REQUEST)
        else:
            events.append(SlotSet(EntitySlotEnum.TICKET_NO, None))
            dispatcher.utter_message(template=UtteranceEnum.PROCESS_CANCELLED)

        return events
