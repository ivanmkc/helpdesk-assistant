from rasa.shared.nlu.state_machine.state_machine_models import (
    Intent,
    Utterance,
    TextSlot,
    BooleanSlot,
)

from rasa.shared.nlu.state_machine.state_machine_state import (
    Response,
    StateMachineState,
    Transition,
)

from rasa.shared.nlu.state_machine.conditions import (
    IntentCondition,
    OnEntryCondition,
    SlotEqualsCondition,
    SlotsFilledCondition,
)

from data_generation import state_machine_generation, story_generation
from data_generation.story_generation import ActionName, IntentName

import data_generation.common_intents as common

# class SpaceEntity(Enum, Entity):
#     person = "PERSON"
#     geopolitical_entity = "GPE"
#     location = "LOC"

#     def name(self) -> str:
#         return self.value

intent_select_boat_tour = Intent(
    examples=[
        "The boat tour",
        "boat",
        "I would prefer the boat one",
        "The 3pm",
        "The one at 3 o clock",
        "The tour at 3",
        "3 sounds good",
    ]
)

intent_select_bus_tour = Intent(
    examples=[
        "The bus tour",
        "bus",
        "I would prefer the bus one",
        "The 4pm",
        "The one at 4 o clock",
        "The tour at 4",
        "4 sounds good",
        "Four",
    ]
)

action_ask_tour = Utterance(
    "We have a boat tour of the city at 3:00pm. We also have a bus tour of the city at 4:00pm. Which one would you prefer?"
)

slot_tour = TextSlot(
    name="tour_type",
    intents={
        intent_select_bus_tour: "bus",
        intent_select_boat_tour: "boat",
    },
    prompt_actions=[
        action_ask_tour,
    ],
)

slot_number_tickets = TextSlot(
    name="tour_num_tickets",
    entities=["number"],
    prompt_actions=[
        Utterance("How many tickets do you need for the {tour_type} tour?")
    ],
    only_fill_when_prompted=True,
)

slot_tour_confirmed = BooleanSlot(
    name="tour_confirmed",
    intents={
        "affirm": True,
        "deny": False,
    },
    prompt_actions=[
        Utterance(
            "Okay, just to confirm. I've booked you for the {tour_type} tour for {tour_num_tickets} persons. Is that correct?"
        ),
    ],
    only_fill_when_prompted=True,
)

slots = [
    slot_tour,
    slot_number_tickets,
    slot_tour_confirmed,
]

book_tour_state = StateMachineState(
    name="book_tour",
    slots=slots,
    slot_fill_utterances=[
        Utterance("Great. Booked you for the {tour_type} tour."),
        Utterance("Okay, {tour_num_tickets} tickets"),
    ],
    transitions=[
        Transition(
            condition=IntentCondition(common.intent_changed_my_mind),
            transition_utterances=[
                Utterance(
                    text="Sure, not a problem.",
                )
            ],
            destination_state_name=None,
        ),
        Transition(
            condition=SlotsFilledCondition(slots),
            transition_utterances=[],
            destination_state_name=None,
        ),
    ],
    responses=[
        Response(
            condition=OnEntryCondition(),
            actions=[
                Utterance("Let's book your tour."),
            ],
        ),
        Response(
            condition=SlotEqualsCondition(
                slot=slot_tour_confirmed, value=False
            ),
            actions=[
                Utterance("No? Okay, what would you like then?"),
                ActionName("action_reset_tour_slots"),
            ],
        ),
        Response(
            condition=SlotEqualsCondition(
                slot=slot_tour_confirmed, value=True
            ),
            actions=[
                Utterance(
                    "Okay great, please make sure you're here 15 min before departure."
                ),
            ],
        ),
    ],
)

state_machine_generation.persist(
    state=book_tour_state,
    is_initial_state=True,
    domain_folder="domain/visitor_center/",
    nlu_folder="data/visitor_center/",
)
