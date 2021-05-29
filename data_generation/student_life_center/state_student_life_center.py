from typing import Any, Dict, List, Set

from rasa.shared.nlu.state_machine.state_machine_models import (
    Intent,
    Utterance,
    TextSlot,
)

from rasa.shared.nlu.state_machine.state_machine_state import (
    Action,
    Response,
    StateMachineState,
    Transition,
)

from rasa.shared.nlu.state_machine.conditions import (
    AndCondition,
    IntentCondition,
    OnEntryCondition,
    SlotEqualsCondition,
)

import state_machine_generation

# class SpaceEntity(Enum, Entity):
#     person = "PERSON"
#     geopolitical_entity = "GPE"
#     location = "LOC"

#     def name(self) -> str:
#         return self.value


want_to_leave_intent = Intent(
    name="want_to_leave", examples=["I want to leave"]
)
intent_where_are_you_from = Intent(
    name="where_are_you_from", examples=["Where are you from?"]
)
wheres_the_washroom_intent = Intent(
    name="wheres_the_washroom",
    examples=[
        "Where's the washroom?",
        "Where is the restroom?",
        "What is the location of the washroom?",
        "I need to find the toilet",
    ],
)
how_are_you_doing_intent = Intent(
    name="how_are_you_doing", examples=["How are you doing?"]
)

slotName = TextSlot(
    name="name",
    entities=["PERSON"],
    prompt_actions=[
        Utterance(
            text="Can I get your name?",
            name="utter_can_i_get_your_name",
        ),
        Utterance(
            text="What about your name?",
            name="utter_what_about_your_name",
        ),
    ],
)

slotHometown = TextSlot(
    name="hometown",
    entities=["GPE", "LOC"],
    prompt_actions=[
        Utterance(
            text="What is your hometown?", name="utter_what_is_your_hometown"
        )
    ],
)

generalResponses: List[Response] = [
    Response(
        condition=IntentCondition(intent_where_are_you_from),
        actions=[
            Utterance(text="I'm from Canada", name="utter_where_from_response")
        ],
    ),
    Response(
        condition=IntentCondition(wheres_the_washroom_intent),
        actions=[
            Utterance(
                text="It's in the cafeteria",
                name="utter_washroom_response",
            )
        ],
    ),
    Response(
        condition=IntentCondition(how_are_you_doing_intent),
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
                name="what_are_hours",
                examples=[
                    "What are your hours?",
                    "When do you close?",
                    "What time do you open until?",
                    "What time do you close?",
                    "Are you still open?",
                ],
            )
        ),
        actions=[
            Utterance(
                text="We're open from 9 to 5, Mondays to Fridays.",
                name="utter_hours",
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
    Response(
        condition=IntentCondition(
            Intent(
                name="what_school_mascot",
                examples=[
                    "What's the school mascot?",
                ],
            )
        ),
        actions=[
            Utterance(
                text="Why, the stag of course",
            ),
            Utterance(
                text="The school mascot? You must mean the stag",
            ),
        ],
    ),
]

student_life_state_machine = StateMachineState(
    name="student_form",
    slots=[slotName, slotHometown],
    slot_fill_utterances=[
        Utterance(
            text="Nice to meet you {name}", name="utter_greeting_response"
        ),
        Utterance(
            text="I'd love to visit {hometown} someday",
            name="utter_hometown_slot_filled_response",
        ),
    ],
    transitions=[
        Transition(
            name="exit_form",
            condition=IntentCondition(want_to_leave_intent),
            transition_utterances=[
                Utterance(
                    text="Sure, let's go back to what we were talking about.",
                    name="utter_leave_response",
                )
            ],
            destination_state_name=None,
        )
    ],
    responses=[
        Response(
            condition=OnEntryCondition(),
            actions=[
                Utterance(
                    text="I'll need some more info from you",
                    name="utter_need_more_info",
                )
            ],
        )
    ]
    + generalResponses,
)

state_machine_generation.persist(
    student_life_state_machine,
    domain_filename="domain/student_life_state_machine.yaml",
    nlu_filename="data/student_life_state_machine.yaml",
)
