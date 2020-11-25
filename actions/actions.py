# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
import main
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import AllSlotsReset
import utils


class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "user_defined"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user_input = tracker.latest_message['text']
        print(user_input)
        name = tracker.get_slot("name")
        # character = tracker.get_slot("character")
        attribute = tracker.get_slot("attributes")
        aggregate = tracker.get_slot("aggregates")
        subject = tracker.get_slot("subject")

        if not name:
            name = ""
        else:
            name = utils.approved_name_string_finder(name)
        print("name", name)
        if not attribute:
            attribute = ""
        else:
            attribute = utils.approved_string_finder(attribute)
        print("attribute", attribute)
        if not aggregate:
            aggregate = ""
        else:
            aggregate = utils.approved_string_finder(aggregate)
        print("aggregate", aggregate)
        if not subject:
            subject = ""
        else:
            subject = utils.approved_string_finder(subject)
        print("subject", subject)
        # print("Subject: " + subject + ", attribute: " + attribute + ", aggregate: " + aggregate)
        return_string = ""
        if name== "":
            if aggregate != "":
                return_string = main.generate_query_and_fetch_results(subject, attribute, aggregate_boolean=True,
                                                                      aggregate_string=aggregate)
            else:
                return_string = main.generate_query_and_fetch_results(subject, attribute)
        else:
            if aggregate != "":
                return_string = main.generate_query_and_fetch_results_v1(name, attribute, aggregate_boolean=True,
                                                                      aggregate_string=aggregate, is_name=True)
            else:
                return_string = main.generate_query_and_fetch_results_v1(name, attribute, is_name=True)
        if return_string == "":
            return_string = "Hey, I am just a bot, you know. Please rephrase the sentence in a way I can understand!"
        print("return", return_string)
        dispatcher.utter_message(text=return_string)

        return [AllSlotsReset()]
