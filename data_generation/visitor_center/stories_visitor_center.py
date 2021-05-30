from typing import Any, Dict, List, Set
from rasa.shared.nlu.state_machine.state_machine_models import (
    Intent,
    Utterance,
    ActionName,
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

from data_generation import story_generation
from data_generation.story_generation import IntentName

import data_generation.common_intents as common
import data_generation.visitor_center.state_book_tour as book_tour

from data_generation.story_generation import Story, Fork, Or, OrActions

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
    "The Holburne Museum has a great art collection. It has both modern and antique art."
)

utter_museum_hours = Utterance(
    "The Holburne museum is open right now. It's open from 10:00 AM to 5:00 PM on weekdays. On weekends, it's open from 11:00 AM to 7:00 PM."
)

utter_great_restaurant_nearby = Utterance(
    "TThere is a great restaurant around the corner. It’s Called “Sally O’s”. You should go there!",
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
            Intent(examples=["What's there to do around here?"]),
            Utterance(
                "The Roman Baths are my favorite thing to see in Bath. You could also check out the Museum of Bath Architecture or the Bath Abbey."
            ),
        ]
    ),
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
                "The city bus tour stops at famous historical monuments, such as the bath Abbey, the River Avon and the Great Pulteney Bridge."
            ),
        ]
    ),
    Story(
        [
            OrActions(*restaurant_utterances),
            Or(common.intent_what_is_that),
            Utterance(
                "The restaurant is a cozy, family-run Italian restaurant."
            ),
        ]
    ),
    Story(
        [
            Or(common.intent_what_do_you_do, IntentName("help")),
            Utterance(
                "I help visitors who want to explore the town by giving them information about the places around here. I can also help with booking tours. You can also buy the CityPass here which lets you go to attractions at a discount."
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
                "The city boat tour is available from 9:00 AM to 5:00 PM. The first city boat tour starts at 9:00 AM. The last city boat tour starts at 4:30 PM."
            ),
        ]
    ),
    Story(
        [
            OrActions(*bus_utterances),
            common.intent_when_is_that,
            Utterance(
                "The city bus tour is available from 10:00 AM to 9:00 PM. The first city bus tour starts at 10:00 AM. Then, it starts every 30 minutes. The last city bus tour starts at 8:00 PM."
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
    Story(
        [
            common.intent_when_is_that,
            Utterance("We're open from 11am to 9pm, every day except Sunday."),
        ]
    ),
]

# What length
stories_lengths = [
    Story(
        elements=[
            OrActions(*boat_utterances),
            common.intent_how_long,
            Utterance("The city boat tour takes 25 minutes."),
        ],
    ),
    Story(
        elements=[
            OrActions(*bus_utterances),
            common.intent_how_long,
            Utterance("The city bus tour takes one hour."),
        ],
    ),
]

# Stories price
stories_price = [
    Story(
        elements=[
            OrActions(*boat_utterances),
            common.intent_what_price,
            Utterance("The city boat tour costs 12 euros per person."),
        ],
    ),
    Story(
        elements=[
            OrActions(*bus_utterances),
            common.intent_what_price,
            Utterance("The city bus tour costs 20 euros per person."),
        ],
    ),
    Story(
        [
            OrActions(*museum_utterances),
            common.intent_what_price,
            Utterance(
                "Tickets for the Holburne Museum cost 12.50 euros for adults and 7.50 euros for children under 12."
            ),
        ]
    ),
    Story(
        [
            OrActions(*restaurant_utterances),
            common.intent_what_price,
            Utterance(
                "I think it's fairly affordable. You can probably get a lunch for 10 euros."
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
