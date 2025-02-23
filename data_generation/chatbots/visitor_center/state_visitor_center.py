from typing import List

from rasa.shared.nlu.state_machine.conditions import (
    IntentCondition,
    OnEntryCondition,
    ActionCondition,
)
from rasa.shared.nlu.state_machine.state_machine_models import (
    ActionName,
    IntentWithExamples,
    Utterance,
)
from rasa.shared.nlu.state_machine.state_machine_state import (
    Response,
    StateMachineState,
    Transition,
)

import data_generation.common_nlu.common_intents as common
import data_generation.chatbots.visitor_center.book_tour.state_book_tour as book_tour
import data_generation.chatbots.visitor_center.buy_citypass.state_buy_citypass as buy_citypass

# intent_book_tour = IntentWithExamples(
#     examples=[
#         "I’d like to book a tour",
#         "I want to book a tour.",
#         "Can I ask you about tours?",
#         "Can I book a tour?",
#         "Give me a tour",
#     ]
# )

# intent_buy_citypass = IntentWithExamples(
#     examples=[
#         "I want to buy a CityPass",
#         "Can I have a CityPass?",
#         "I'll take one CityPass please?",
#         "I want the CityPass ticket",
#     ]
# )

utter_i_can_help = Utterance(
    text="Sure, I can help you with that.", name="utter_i_can_help_you",
)

start_state = StateMachineState(
    name="start_state",
    slots=[],
    slot_fill_utterances=[],
    transitions=[
        Transition(
            condition=ActionCondition(
                action=ActionName("action_trigger_book_tour")
            ),
            transition_utterances=[utter_i_can_help],
            destination_state_name=book_tour.book_tour_state.name,
        ),
        Transition(
            condition=ActionCondition(
                action=ActionName("action_trigger_buy_citypass")
            ),
            transition_utterances=[utter_i_can_help],
            destination_state_name=buy_citypass.buy_citypass_state.name,
        ),
    ],
    responses=[
        Response(
            condition=OnEntryCondition(),
            actions=[
                Utterance(
                    text="Welcome to the Bath Visitor Center! How can I help you?",
                    name="utter_intro",
                ),
            ],
        ),
    ],
)
