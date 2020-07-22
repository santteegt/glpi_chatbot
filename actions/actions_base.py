# -*- coding: utf-8 -*-

import logging

from rasa_sdk import Action, Tracker
from rasa_sdk.events import EventType, SlotSet
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction, REQUESTED_SLOT
from typing import Dict, Text, Any, List, Optional

from actions.constants import EntitySlotEnum, IntentEnum, UtteranceEnum

logger = logging.getLogger(__name__)


def request_next_slot(
    form: FormAction,
    dispatcher: CollectingDispatcher,
    tracker: Tracker,
    domain: Dict[Text, Any],
) -> Optional[List[EventType]]:
    """
    Custom method to set a custom utterance templata if slot == confirm
    :param form: Form Action object
    :param dispatcher: Rasa SDK Dispatcher
    :param tracker: Rasa SDK tracker
    :param domain: Rasa domain
    :return: SlotSet event
    """
    for slot in form.required_slots(tracker):
        if form._should_request_slot(tracker, slot):
            utter_template = f"utter_ask{f'_{form.name()}' if slot == EntitySlotEnum.CONFIRM else ''}_{slot}"
            dispatcher.utter_message(template=utter_template, **tracker.slots)
            return [SlotSet(REQUESTED_SLOT, slot)]


def ask_if_success(
    dispatcher: CollectingDispatcher, incident_title: Text, itilcategory_id: int = None
):
    """
    Ask if request was succesful. Otherwise redirects to report an incident
    :param dispatcher: Rasa SDK Dispatcher
    :param incident_title: Incident title for the ticket
    :param itilcategory_id: ITIL category for the incident
    """

    params = "{"
    params += f'"{EntitySlotEnum.INCIDENT_TITLE}":"{incident_title}"'
    if itilcategory_id:
        params += f', "{EntitySlotEnum.ITILCATEGORY_ID}":"{itilcategory_id}"'
    params += "}"

    dispatcher.utter_message(
        template=UtteranceEnum.CONFIRM_SUCCESS,
        buttons=[
            {"title": "Si", "payload": f"/{IntentEnum.CONFIRM}"},
            {"title": "No", "payload": f"/{IntentEnum.DENY}" + params},
        ],
    )


class ActionDefaultAskAffirmation(Action):
    """Asks for an affirmation of the intent if NLU threshold is not met."""

    def name(self):
        return "action_default_ask_affirmation"

    def __init__(self):
        self.intent_mappings = {
            IntentEnum.CONNECT_WIFI: "Ayuda con conexión al WiFI",
            IntentEnum.CREATE_USER: "Ayuda a crear un usuario",
            IntentEnum.REQUEST_BIOMETRICS_REPORT: "Informe de marcación en biométrico",
            IntentEnum.REQUEST_VM: "Solicitud de máquina virtual",
            IntentEnum.PASSWORD_RESET: "Recuperar contraseña",
            IntentEnum.PROBLEM_EMAIL: "Problema con el correo electrónico",
            IntentEnum.OPEN_INCIDENT: "Reportar una incidencia",
            IntentEnum.SHOW_MENU: "Ver menu de opciones",
        }
        # read the mapping from a csv and store it in a dictionary
        # with open('intent_mapping.csv', newline='', encoding='utf-8') as file:
        #     csv_reader = csv.reader(file)
        #     for row in csv_reader:
        #         self.intent_mappings[row[0]] = row[1]

    def run(self, dispatcher, tracker, domain):
        # get the most likely intent
        last_intent_name = tracker.latest_message["intent"]["name"]

        mapping_exists = (
            True if last_intent_name in self.intent_mappings.keys() else False
        )

        if mapping_exists:
            # get the prompt for the intent
            intent_prompt = self.intent_mappings[last_intent_name]

            # Create the affirmation message and add two buttons to it.
            # Use '/<intent_name>' as payload to directly trigger '<intent_name>'
            # when the button is clicked.
            message = "Tal vez quiso decir '{}'?".format(intent_prompt)
            buttons = [
                {"title": "Si", "payload": f"/{last_intent_name}"},
                {"title": "No", "payload": f"/{IntentEnum.SHOW_MENU}"},
            ]
            dispatcher.utter_button_message(message, buttons=buttons)
        else:
            # TODO: narrow a list of most probable intents?
            logger.info("NO ACTION FOUND. Showing suggestions")
            dispatcher.utter_image_url(
                "http://www.crear-meme.com/public/img/memes_users/what-7.jpg"
            )
            # tracker.trigger_followup_action("utter_sugerencias")
            dispatcher.utter_message(template=UtteranceEnum.SUGGEST)

        return []
