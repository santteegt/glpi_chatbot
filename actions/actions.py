# -*- coding: utf-8 -*-

import logging
from typing import Dict, Text, Any, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from actions.constants import EntitySlotEnum, IntentEnum, RasaConstants, UtteranceEnum

logger = logging.getLogger(__name__)


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

    def name(self) -> Text:
        return RasaConstants.ACTION_DEFAULT_ASK_AFFIRMATION_NAME

    def __init__(self):
        self.intent_mappings = {
            IntentEnum.CONNECT_WIFI: "Ayuda con conexión al WiFI",
            IntentEnum.FAQ_CREATE_USER: "Como crear un usuario?",
            IntentEnum.CREATE_APP_USER: "Ayuda a crear un usuario",
            IntentEnum.REQUEST_BIOMETRICS_REPORT: "Informe de marcación en biométrico",
            IntentEnum.PASSWORD_RESET: "Recuperar contraseña",
            IntentEnum.PROBLEM_EMAIL: "Problema con el correo electrónico",
            IntentEnum.OPEN_INCIDENT: "Reportar una incidencia",
            IntentEnum.GET_INCIDENT_STATUS: "Obtener estado de una incidencia",
            IntentEnum.SHOW_MENU: "Ver menu de opciones",
        }

    def run(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:

        # get the most likely intent
        intent_to_affirm = tracker.latest_message['intent']["name"]
        intent_ranking = tracker.latest_message[RasaConstants.INTENT_RANKING_KEY]
        if intent_to_affirm == RasaConstants.DEFAULT_NLU_FALLBACK_INTENT_NAME \
                and intent_ranking and len(intent_ranking) > 1:
            intent_to_affirm = intent_ranking[1]["name"]

        mapping_exists = (
            True if intent_to_affirm in self.intent_mappings.keys() else False
        )

        if mapping_exists:
            # get the prompt for the intent
            intent_description = self.intent_mappings[intent_to_affirm]
            affirmation_message = f"Talvez quiso decir '{intent_description}'?"
            buttons = [
                {"title": "Si", "payload": f"/{intent_to_affirm}"},
                {"title": "No", "payload": f"/{IntentEnum.OUT_OF_SCOPE}"},
            ]
            dispatcher.utter_message(text=affirmation_message, buttons=buttons)
        else:
            # TODO: narrow a list of most probable intents?
            logger.info(f"NO DESCRIPTION FOUND for {intent_to_affirm}. Showing suggestions")
            dispatcher.utter_message(
                image="http://www.crear-meme.com/public/img/memes_users/what-7.jpg"
            )
            dispatcher.utter_message(template=UtteranceEnum.OUT_OF_SCOPE)
            dispatcher.utter_message(template=UtteranceEnum.SUGGEST)

        return []
