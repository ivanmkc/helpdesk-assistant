from rasa.shared.nlu.state_machine.state_machine_models import (
    ActionName,
    Intent,
    Utterance,
)

import data_generation.common_intents as common
import data_generation.visitor_center.book_tour.state_book_tour as book_tour
import data_generation.visitor_center.book_tour.stories_book_tour as stories_book_tour
import data_generation.visitor_center.places as places
import data_generation.visitor_center.state_visitor_center as state_visitor_center
from data_generation import story_generation
from data_generation.place import Place
from data_generation.story_generation import (
    Fork,
    IntentName,
    Or,
    OrActions,
    Story,
)

# Personal
stories_personal = [
    Story(
        [
            Intent(examples=["Who are you?", "What's your name?"]),
            Utterance("I'm called Patrick"),
            Utterance("I help visitors to Bath, like yourself."),
        ]
    ),
    Story(
        [
            Intent(examples=["Who are you?", "What's your name?"]),
            Utterance("I'm called Patrick"),
            Utterance("I help visitors to Bath, like yourself."),
        ]
    ),
]

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
            Or(common.intent_what_do_you_do, IntentName("help")),
            Utterance(
                "I help visitors who want to explore the town by giving them information about the places around here. I can also help with booking tours. You can also buy the CityPass here which lets you go to attractions at a discount."
            ),
        ]
    ),
    Story(
        [
            Intent(
                examples=[
                    "What tours do you have?",
                    "What tours are there?",
                    "Tell me more about the tours",
                    "What tours",
                    "How many tours?",
                    "I have some questions about tours",
                ]
            ),
            Utterance(
                "We have a bus tour and a boat tour. You can book them here."
            ),
        ]
    ),
]

# What time?
stories_what_time = [
    Story(
        [
            Intent(
                examples=[
                    "What are your hours?",
                    "When do you open?",
                    "When do you close?",
                    "What time do you open until?",
                    "What time do you close?",
                    "Are you still open?",
                ]
            ),
            Utterance("We're open from 11am to 9pm, every day except Sunday."),
        ]
    ),
]

stories_tours = [
    Story(
        name="tours",
        elements=[
            Intent(
                examples=[
                    "I want to buy a ticket",
                    "Can I have a ticket?",
                    "I buy tickets",
                    "Give me a ticket",
                ]
            ),
            Utterance("Which one? The bus tour, boat tour or the CityPass?"),
            Fork(
                [
                    book_tour.intent_select_boat_tour,
                    stories_book_tour.utter_put_down_boat_tour,
                    ActionName("action_set_tour_boat"),
                    # TODO: StateMachineTransition
                ],
                [
                    book_tour.intent_select_bus_tour,
                    stories_book_tour.utter_put_down_bus_tour,
                    ActionName("action_set_tour_bus"),
                    # TODO: StateMachineTransition
                ],
                [
                    state_visitor_center.intent_buy_citypass,
                    # TODO: StateMachineTransition
                ],
                [
                    Or(
                        common.intent_what_do_you_recommend,
                        common.intent_not_sure,
                        IntentName("help"),
                    ),
                    Utterance(
                        "I'd personally go with the CityPass as I love museums."
                    ),
                    Fork(
                        [
                            Or(
                                common.intent_sure_ill_get_that,
                                IntentName("affirm"),
                            ),
                            # TODO: StateMachineTransition
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
]

# Tour and other info
story_generation.persist(
    stories_tell_me_more
    + stories_book_tour.stories_tours
    + stories_what_time
    + [story for place in places.places for story in place.generate_stories()],
    domain_filename="domain/visitor_center/stories.yaml",
    nlu_filename="data/visitor_center/stories.yaml",
    use_rules=False,
)
