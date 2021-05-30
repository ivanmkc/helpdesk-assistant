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
from data_generation.place import Place

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

utter_tour_info = Utterance("There's a bus tour and a boat tour.")

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
            utter_tour_info,
        ]
    ),
]

# What time?
stories_what_time = [
    Story(
        [
            common.intent_when_is_that,
            Utterance("We're open from 11am to 9pm, every day except Sunday."),
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
    # Handle the case: When is my tour again?
]

holburne_museum = Place(
    name="The Holburne Museum",
    synonyms=["museum"],
    intent=Intent(
        examples=[
            "What about museums?",
            "I'd like to go to a museum",
            "Are there any museums?",
        ]
    ),
    intro=Utterance(
        "The Holburne Museum has a great art collection. It has both modern and antique art."
    ),
    hours=Utterance(
        "The Holburne museum is open right now. It's open from 10:00 AM to 5:00 PM on weekdays. On weekends, it's open from 11:00 AM to 7:00 PM."
    ),
    more_details=None,
    price=Utterance(
        "Tickets for the Holburne Museum cost 12.50 euros for adults and 7.50 euros for children under 12."
    ),
    directions=None,
)


bath_architecture_museum = Place(
    name="Museum of Bath Architecture",
    synonyms=["museum of architecture", "architecture museum"],
    intent=Intent(
        examples=[
            "What about the architecture museum?",
            "Is there a museum of architecture?",
        ]
    ),
    intro=Utterance(
        "The Museum of Bath Architecture is great if you love architecture and design!"
    ),
    hours=Utterance(
        "The Museum of Bath Architecture is open from 12:00 PM to 6:00 PM on weekdays."
    ),
    more_details=Utterance(
        "The Museum of Bath Architecture shows a history of Bath’s buildings."
    ),
    price=Utterance(
        "Tickets for the Museum of Bath Architecture are 15 euros for adults and children under 12."
    ),
    directions=None,
)

bath_abbey = Place(
    name="Bath Abbey",
    synonyms=["abbey"],
    intent=Intent(
        examples=[
            "What about the Bath Abbey?",
            "Is there an abbey around?",
            "Tell me about the abbey",
        ]
    ),
    intro=Utterance("The Bath Abbey is a famous medieval church in England."),
    hours=Utterance(
        "The Bath Abbey is open on Monday to Saturday from 10:00 AM to 3:45 PM."
    ),
    more_details=None,
    price=Utterance("The Bath Abbey tickets are 5 euros per person."),
    directions=None,
)

bridge = Place(
    name="Great Pultaney Bridge",
    synonyms=["bridge", "pultaney bridge"],
    intent=Intent(
        examples=[
            "What about the bridge?",
            "Is there a bridge around?",
            "I heard about a bridge",
        ]
    ),
    intro=Utterance(
        "The Great Pulteney Bridge is a popular place for tourists."
    ),
    hours=Utterance(
        "The Bath Abbey is open on Monday to Saturday from 10:00 AM to 3:45 PM."
    ),
    more_details=Utterance(
        "There are many shops on the Great Pulteney Bridge."
    ),
    price=Utterance("It is free to walk on the Great Pulteney Bridge."),
    directions=None,
)

roman_baths = Place(
    name="Roman Baths",
    synonyms=["baths"],
    intent=Intent(
        examples=[
            "What about Roman Baths?",
        ]
    ),
    intro=Utterance("The Roman Baths are a very old historical monument."),
    hours=Utterance(
        "The Roman Baths are open from 10:00 AM to 6:00 PM everyday."
    ),
    more_details=Utterance("The Roman Baths are very popular for tourists!"),
    price=Utterance(
        "On weekdays, tickets for the Roman Baths are 10 euros per person and 8 euros per person on weekends."
    ),
    directions=None,
)

restaurant = Place(
    name="Sally O's",
    synonyms=["restaurant"],
    intent=Intent(
        examples=[
            "What about restaurants?",
            "I'm hungry",
            "I'd like to eat something",
            "Any idea where I can get some food?",
            "What's there to eat?",
            "I want to eat something",
        ]
    ),
    intro=Utterance(
        "There is a great restaurant around the corner. It’s Called “Sally O’s”. You should go there!",
    ),
    hours=Utterance(
        "It's open for lunch and dinner. I'm not sure about the exact times"
    ),
    more_details=Utterance(
        "The restaurant is a cozy, family-run Italian restaurant."
    ),
    price=Utterance(
        "I think it's fairly affordable. You can probably get a lunch for 10 euros."
    ),
    directions=None,
)

boat_tour = Place(
    name="City Boat Tour",
    synonyms=["boat tour", "river tour"],
    intent=Intent(
        examples=[
            "Is there a boat tour?",
            "Tell me about the boat tour",
            "I heard there is a boat tour",
            "I heard there was a river tour",
        ]
    ),
    intro=Utterance(
        "The boat tour is the most popular tour we have.",
    ),
    hours=Utterance(
        "The city boat tour is available from 9:00 AM to 5:00 PM. The first city boat tour starts at 9:00 AM. The last city boat tour starts at 4:30 PM."
    ),
    more_details=None,
    price=Utterance("The city boat tour costs 12 euros per person."),
    directions=None,
    duration=Utterance("The city boat tour takes 25 minutes."),
    related_actions=[
        utter_put_down_boat_tour,
    ],
)


bus_tour = Place(
    name="City Bus Tour",
    synonyms=["bus tour"],
    intent=Intent(
        examples=[
            "Is there a bus tour?",
            "Tell me about the bus tour",
            "I heard there is a bus tour",
        ]
    ),
    intro=Utterance(
        "The city bus tour stops at famous historical monuments, such as the bath Abbey, the River Avon and the Great Pulteney Bridge."
    ),
    hours=Utterance(
        "The city bus tour is available from 10:00 AM to 9:00 PM. The first city bus tour starts at 10:00 AM. Then, it starts every 30 minutes. The last city bus tour starts at 8:00 PM."
    ),
    more_details=None,
    price=Utterance("The city bus tour costs 20 euros per person."),
    directions=None,
    duration=Utterance("The city bus tour takes one hour."),
    related_actions=[
        utter_put_down_bus_tour,
    ],
)

places = [
    holburne_museum,
    restaurant,
    bus_tour,
    boat_tour,
    bath_architecture_museum,
    bath_abbey,
    bridge,
    roman_baths,
]

# Tour and other info
story_generation.persist(
    stories_tell_me_more
    + stories_tours
    + stories_what_time
    + [story for place in places for story in place.generate_stories()],
    domain_filename="domain/visitor_center/stories.yaml",
    nlu_filename="data/visitor_center/stories.yaml",
    use_rules=False,
)
