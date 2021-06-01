from rasa.shared.nlu.state_machine.conditions import (
    AndCondition,
    IntentCondition,
    OnEntryCondition,
    SlotEqualsCondition,
    SlotsFilledCondition,
)
from rasa.shared.nlu.state_machine.state_machine_models import (
    ActionName,
    BooleanSlot,
    Intent,
    TextSlot,
    Utterance,
)
from rasa.shared.nlu.state_machine.state_machine_state import (
    Response,
    StateMachineState,
    Transition,
)

import data_generation.common_intents as common
from data_generation import state_machine_generation, story_generation
from data_generation.story_generation import IntentName

slot_number_tickets = TextSlot(
    name="citypass_num_tickets",
    entities=["number"],
    intents={Intent(examples=["Just me", "Myself", "Just the one"]): 1},
    prompt_actions=[Utterance("How many tickets do you need?")],
    only_fill_when_prompted=True,
)

slot_citypass_confirmed = BooleanSlot(
    name="citypass_confirmed",
    intents={
        "affirm": True,
        "deny": False,
    },
    prompt_actions=[
        Utterance(
            "Okay, just to confirm. You want {citypass_num_tickets} of the CityPass. Is that correct?"
        ),
    ],
    only_fill_when_prompted=True,
)

slots = [
    slot_number_tickets,
    slot_citypass_confirmed,
]

buy_citypass_state = StateMachineState(
    name="buy_citypass",
    slots=slots,
    slot_fill_utterances=[
        Utterance("Okay, {citypass_num_tickets} tickets"),
    ],
    transitions=[
        Transition(
            condition=IntentCondition(common.intent_changed_my_mind),
            transition_utterances=[
                # TODO: Reset slots
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
                Utterance("The CityPass is a great deal."),
            ],
        ),
        Response(
            condition=SlotEqualsCondition(
                slot=slot_citypass_confirmed, value=False
            ),
            actions=[
                Utterance("No? Okay, what would you like then?"),
                ActionName("action_reset_citypass_slots"),
            ],
        ),
        Response(
            condition=SlotEqualsCondition(
                slot=slot_citypass_confirmed, value=True
            ),
            actions=[
                Utterance(
                    "Okay great, here you go. Thanks for your business."
                ),
            ],
        ),
    ],
)

state_machine_generation.persist(
    state=buy_citypass_state,
    is_initial_state=False,
    domain_folder="domain/visitor_center/",
    nlu_folder="data/visitor_center/",
)
