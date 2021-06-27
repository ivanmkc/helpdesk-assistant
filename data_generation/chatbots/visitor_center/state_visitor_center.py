from typing import List

from rasa.shared.nlu.state_machine.conditions import (
    IntentCondition,
    OnEntryCondition,
    OrCondition,
)
from rasa.shared.nlu.state_machine.state_machine_models import (
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
from data_generation.utils import state_machine_generation

generalResponses: List[Response] = [
    Response(
        condition=IntentCondition(common.intent_where_are_you_from),
        actions=[
            Utterance(text="I'm from Canada", name="utter_where_from_response")
        ],
    ),
    Response(
        condition=IntentCondition(common.how_are_you_doing_intent),
        actions=[
            Utterance(
                text="I'm doing great", name="utter_how_are_you_response",
            )
        ],
    ),
    Response(
        condition=IntentCondition(
            IntentWithExamples(
                examples=[
                    "Are you busy?",
                    "How busy are you?",
                    "Do you have a lot of work?",
                ],
            )
        ),
        actions=[
            Utterance(text="It's not too busy around here as you can see.",)
        ],
    ),
]

intent_book_tour = IntentWithExamples(
    examples=[
        "I’d like to book a tour",
        "I want to book a tour.",
        "Can I ask you about tours?",
        "Can I book a tour?",
        "Give me a tour",
    ]
)

intent_buy_citypass = IntentWithExamples(
    examples=[
        "I want to buy a CityPass",
        "Can I have a CityPass?",
        "I'll take one CityPass please?",
        "I want the CityPass ticket",
    ]
)

utter_i_can_help = Utterance(
    text="Sure, I can help you with that.", name="utter_i_can_help_you",
)

start_state = StateMachineState(
    name="start_state",
    slots=[],
    slot_fill_utterances=[],
    transitions=[
        Transition(
            condition=OrCondition(
                [
                    IntentCondition(intent_book_tour),
                    IntentCondition(book_tour.intent_select_bus_tour),
                    IntentCondition(book_tour.intent_select_boat_tour),
                ]
            ),
            transition_utterances=[utter_i_can_help],
            destination_state_name=book_tour.book_tour_state.name,
        ),
        Transition(
            condition=IntentCondition(intent_buy_citypass),
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
    ]
    + generalResponses,
)
