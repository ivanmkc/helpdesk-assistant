from typing import Any, Dict, List, Set
from rasa.shared.nlu.state_machine.state_machine_models import (
    Intent,
    Utterance,
)

from rasa.shared.nlu.state_machine.state_machine_state import (
    Response,
    StateMachineState,
    Transition,
)

from rasa.shared.nlu.state_machine.conditions import (
    IntentCondition,
    OnEntryCondition,
)

from data_generation import state_machine_generation, story_generation
from data_generation.story_generation import ActionName, IntentName

import data_generation.common_intents as common
import data_generation.state_machines.visitor_center.book_tour as book_tour

from data_generation.story_generation import Story, Fork, Or, OrActions


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
        condition=IntentCondition(common.intent_when_is_that),
        actions=[
            Utterance(
                text="We're open from 11am to 9pm, every day except Sunday.",
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
]

intent_book_tour = Intent(
    examples=[
        "I’d like to book a tour",
        "I want to book a tour.",
        "Can I ask you about tours?",
        "Can I book a tour?",
    ]
)

# TODO: Add a drink

# student_life_state_machine = StateMachineState(
#     name="restaurant_ordering",
#     slots=[
#         SlotGroup([slot_appetizer, slot_entree])
#             .if(SlotEqualsCondition(slot_entree, "steak"), then=SlotGroup(slot_steak_doneness, slot_tour_confirmed))
#             .then(slot_tour_confirmed)
#     ]
# )


start_state = StateMachineState(
    name="start_state",
    slots=[],
    slot_fill_utterances=[],
    transitions=[
        Transition(
            condition=IntentCondition(intent_book_tour),
            transition_utterances=[
                # Utterance(
                #     text="Sure, let's book a tour.",
                # )
            ],
            destination_state_name=book_tour.book_tour_state.name,
        ),
    ],
    responses=[
        Response(
            condition=OnEntryCondition(),
            actions=[
                Utterance(
                    "Welcome to the Visitor Center! How can I help you?"
                ),
            ],
        ),
    ]
    + generalResponses,
)

# Response(
#     condition=IntentCondition(
#         Intent(
#             examples=[
#                 "When are the tours?",
#                 "What time are the tours",
#             ]
#         )
#     ),
#     actions=[ActionName("action_ask_tour")],
# ),

utter_recommend_boat = Utterance(
    "May I recommend the boat tour? It's a refreshing way to see the city."
)

utter_put_down_boat_tour = Utterance(
    "Sure, I'll put you down for the 3pm boat tour then."
)

utter_put_down_bus_tour = Utterance(
    "Sure, I'll put you down for the 4pm bus tour then."
)

utter_museum_exists = Utterance(
    "The city museum is open right now. You can take the bus."
)

utter_museum_hours = Utterance("The museum opens everyday from 8am to 6pm.")

utter_great_restaurant_nearby = Utterance(
    "There is a great restaurant around the corner.",
)

utter_tour_info = Utterance("There's a bus tour and a boat tour.")

boat_utterances = [utter_recommend_boat, utter_put_down_boat_tour]
bus_utterances = [utter_put_down_bus_tour]
museum_utterances = [utter_museum_exists]
restaurant_utterances = [utter_great_restaurant_nearby]

intent_what_tours = Intent(
    examples=[
        "What tours do you have?",
        "What tours are there?",
        "Tell me more about the tours",
        "What tours",
        "How many tours?",
        "I have some questions about tours",
    ]
)

# Tell me more
stories_tell_me_more = [
    Story(
        [
            OrActions(*boat_utterances),
            Or(common.intent_what_is_that),
            Utterance("The boat tour is the most popular tour we have."),
        ]
    ),
    Story(
        [
            OrActions(*bus_utterances),
            Or(common.intent_what_is_that),
            Utterance(
                "The bus tour is a comfortable way to traverse the city."
            ),
        ]
    ),
    Story(
        [
            OrActions(*restaurant_utterances),
            Or(common.intent_what_is_that),
            Utterance(
                "The restaurant is cozy, family-run Italian restaurant."
            ),
        ]
    ),
    Story(
        [
            Or(common.intent_what_do_you_do, IntentName("help")),
            Utterance(
                "I help visitors who want to explore the town by giving them information about the places around here. I can also help with booking tours."
            ),
            intent_what_tours,
            utter_tour_info,
        ]
    ),
    Story([intent_what_tours, utter_tour_info]),
]

# What time?
stories_what_time = [
    Story(
        [
            OrActions(*boat_utterances),
            common.intent_when_is_that,
            Utterance(
                "The boat tour open from 10am to 6pm. It runs every 30 minutes."
            ),
        ]
    ),
    Story(
        [
            OrActions(*bus_utterances),
            common.intent_when_is_that,
            Utterance(
                "The bus tour open from 10am to 6pm. It runs every 30 minutes."
            ),
        ]
    ),
    Story(
        [
            OrActions(*museum_utterances),
            common.intent_when_is_that,
            utter_museum_hours,
        ]
    ),
    Story(
        [
            OrActions(*restaurant_utterances),
            common.intent_when_is_that,
            Utterance(
                "It's open for lunch and dinner. I'm not sure about the exact times"
            ),
        ]
    ),
]

# What length
stories_lengths = [
    Story(
        elements=[
            Intent(examples=["How long is the tour?"]),
            Utterance("Both tours are 30 minutes."),
        ],
    ),
    Story(
        elements=[
            OrActions(*boat_utterances),
            common.intent_how_long,
            Utterance("It's a 30 minute boat ride."),
        ],
    ),
    Story(
        elements=[
            OrActions(*bus_utterances),
            common.intent_how_long,
            Utterance("It's a 30 minute bus ride."),
        ],
    ),
]

# Stories price
stories_price = [
    Story(
        name="tour prices",
        elements=[
            OrActions(*(boat_utterances + bus_utterances)),
            common.intent_what_price,
            Utterance("Both tours are 15 dollars"),
        ],
    ),
    Story(
        [
            OrActions(*museum_utterances),
            common.intent_what_price,
            Utterance(
                "The museum costs 10 dollars for adults and free for children under 12."
            ),
        ]
    ),
    Story(
        [
            OrActions(*restaurant_utterances),
            common.intent_what_price,
            Utterance(
                "I think it's fairly affordable. You can probably get a lunch for 10 dollars."
            ),
        ]
    ),
]

stories_tours = [
    Story(
        name="tours",
        elements=[
            book_tour.action_ask_tour,
            Fork(
                [
                    book_tour.intent_select_boat_tour,
                    utter_put_down_boat_tour,
                    ActionName("action_set_tour_boat"),
                ],
                [
                    book_tour.intent_select_bus_tour,
                    utter_put_down_bus_tour,
                    ActionName("action_set_tour_bus"),
                ],
                [
                    Or(
                        common.intent_what_do_you_recommend,
                        common.intent_not_sure,
                        IntentName("help"),
                    ),
                    utter_recommend_boat,
                    Fork(
                        [
                            Or(
                                common.intent_sure_ill_get_that,
                                IntentName("affirm"),
                            ),
                            Utterance("Great, the boat tour then."),
                            # TODO: Set slot
                            ActionName("action_set_tour_boat"),
                        ],
                        [
                            IntentName("deny"),
                            Utterance("It's up to you."),
                        ],
                        # TODO: Handle "nothing" condition
                    ),
                ],
            ),
        ],
    ),
    # TODO: Make this more specific
    Story(
        name="tour details",
        elements=[
            Intent(
                examples=["Where does the tour go?", "What's on the tour?"]
            ),
            Utterance("The tour goes all over the city."),
        ],
    ),
    Story(
        name="museums",
        elements=[
            Intent(
                examples=[
                    "What about museums?",
                    "I'd like to go to a museum",
                    "Are there any museums?",
                ]
            ),
            utter_museum_exists,
        ],
    ),
    Story(
        name="restaurants",
        elements=[
            Intent(
                examples=[
                    "What about restaurants?",
                    "I'm hungry",
                    "I'd like to eat something",
                    "Any idea where I can get some food?",
                    "What's there to eat?",
                    "I want to eat something",
                ]
            ),
            utter_great_restaurant_nearby,
        ],
    ),
    # Handle the case: When is my tour again?
]

state_machine_generation.persist(
    state=start_state,
    is_initial_state=False,
    domain_folder="domain/visitor_center/",
    nlu_folder="data/visitor_center/",
)

# Tour and other info
story_generation.persist(
    stories_lengths
    + stories_price
    + stories_tell_me_more
    + stories_tours
    + stories_what_time,
    domain_filename="domain/visitor_center/stories.yaml",
    nlu_filename="data/visitor_center/stories.yaml",
    use_rules=False,
)
