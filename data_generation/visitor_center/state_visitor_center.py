from typing import Any, Dict, List, Set

from rasa.shared.nlu.state_machine.conditions import (
    IntentCondition,
    OnEntryCondition,
)
from rasa.shared.nlu.state_machine.state_machine_models import (
    Intent,
    Utterance,
)
from rasa.shared.nlu.state_machine.state_machine_state import (
    Response,
    StateMachineState,
    Transition,
)

import data_generation.common_intents as common
import data_generation.visitor_center.book_tour.state_book_tour as book_tour
import data_generation.visitor_center.buy_citypass.state_buy_citypass as buy_citypass
from data_generation import state_machine_generation

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
                text="I'm doing great",
                name="utter_how_are_you_response",
            )
        ],
    ),
    Response(
        condition=IntentCondition(
            Intent(
                examples=[
                    "Are you busy?",
                    "How busy are you?",
                    "Do you have a lot of work?",
                ],
            )
        ),
        actions=[
            Utterance(
                text="It's not too busy around here as you can see.",
            )
        ],
    ),
]

intent_book_tour = Intent(
    examples=[
        "I’d like to book a tour",
        "I want to book a tour.",
        "Can I ask you about tours?",
        "Can I book a tour?",
        "Give me a tour",
    ]
)

intent_buy_citypass = Intent(
    examples=[
        "I want to buy a CityPass",
        "Can I have a CityPass?",
        "I'll take one CityPass please?",
        "I want the CityPass ticket",
    ]
)

utter_i_can_help = Utterance(
    text="Sure, I can help you with that.",
    name="utter_i_can_help_you",
)

start_state = StateMachineState(
    name="start_state",
    slots=[],
    slot_fill_utterances=[],
    transitions=[
        Transition(
            condition=IntentCondition(intent_book_tour),
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
                    "Welcome to the Bath Visitor Center! How can I help you?"
                ),
            ],
        ),
    ]
    + generalResponses,
)

state_machine_generation.persist(
    state=start_state,
    is_initial_state=True,
    domain_folder="domain/visitor_center/",
    nlu_folder="data/visitor_center/",
)
