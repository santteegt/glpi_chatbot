# -*- coding: utf-8 -*-

import logging

from rasa_sdk import Action

logger = logging.getLogger(__name__)


class ActionDefaultAskAffirmation(Action):
    """Asks for an affirmation of the intent if NLU threshold is not met."""

    def name(self):
        return "action_default_ask_affirmation"

    def __init__(self):
        self.intent_mappings = {
            "solicitar_opciones": "Opciones disponibles",
            "creacion_usuarios": "Crear un usuario",
            "recuperar_contrasena": "Recuperar contaseña",
            "peticion_recurso_computacional": "Solicitud de Recursos Computacionales",
        }
        # read the mapping from a csv and store it in a dictionary
        # with open('intent_mapping.csv', newline='', encoding='utf-8') as file:
        #     csv_reader = csv.reader(file)
        #     for row in csv_reader:
        #         self.intent_mappings[row[0]] = row[1]

    def run(self, dispatcher, tracker, domain):
        # get the most likely intent
        last_intent_name = tracker.latest_message['intent']['name']

        mapping_exists = True if last_intent_name in self.intent_mappings.keys() else False

        if mapping_exists:
            # get the prompt for the intent
            intent_prompt = self.intent_mappings[last_intent_name]

            # Create the affirmation message and add two buttons to it.
            # Use '/<intent_name>' as payload to directly trigger '<intent_name>'
            # when the button is clicked.
            message = "Tal vez quiso decir '{}'?".format(intent_prompt)
            buttons = [{'title': 'Si',
                       'payload': '/{}'.format(last_intent_name)},
                      {'title': 'No',
                       'payload': '/chitchat'}]
            dispatcher.utter_button_message(message, buttons=buttons)
        else:
            # TODO: narrow a list of most probable intents?
            pass

        return []