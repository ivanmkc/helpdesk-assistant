from enum import Enum

from typing import List

from state_machine_models import (
    Intent,
    Utterance,
    Slot,
)

from state_machine_state import Response, StateMachineState, Transition

from conditions import (
    AndCondition,
    IntentCondition,
    OnEntryCondition,
    SlotEqualsCondition,
)


# class SpaceEntity(Enum, Entity):
#     person = "PERSON"
#     geopolitical_entity = "GPE"
#     location = "LOC"

#     def name(self) -> str:
#         return self.value


wantToLeaveIntent = Intent(name="want_to_leave", examples=["I want to leave"])
whereAreYouFromIntent = Intent(
    name="where_are_you_from", examples=["Where are you from?"]
)
wheresTheWashroomIntent = Intent(
    name="wheres_the_washroom", examples=["Where's the washroom?"]
)
howAreYouDoingIntent = Intent(
    name="how_are_you_doing", examples=["How are you doing?"]
)

slotName = Slot(
    name="name",
    entities=["PERSON"],
    promptActions=[
        Utterance(
            text="Can I get your name?",
            name="can_i_get_your_name",
        ),
        Utterance(
            text="What about your name?",
            name="what_about_your_name",
        ),
    ],
)

slotHometown = Slot(
    name="hometown",
    entities=["GPE", "LOC"],
)

generalResponses: List[Response] = [
    Response(
        condition=IntentCondition([whereAreYouFromIntent]),
        actions=[
            Utterance(text="I'm from Canada", name="utter_where_from_response")
        ],
    ),
    Response(
        condition=IntentCondition([wheresTheWashroomIntent]),
        actions=[
            Utterance(
                text="It's in the cafeteria",
                name="utter_washroom_response",
            )
        ],
    ),
    Response(
        condition=AndCondition(
            [
                IntentCondition([howAreYouDoingIntent]),
                SlotEqualsCondition(slotName, "Alice"),
                SlotEqualsCondition(slotHometown, "Austin"),
            ]
        ),
        actions=[
            Utterance(
                text="I'm doing great",
                name="utter_how_are_you_response",
            )
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
            condition=IntentCondition(wantToLeaveIntent),
            transition_utterances=[
                Utterance(
                    "utter_leave_response",
                    "Sure, let's go back to what we were talking about.",
                )
            ],
            destination_state=None,
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

# Write NLU