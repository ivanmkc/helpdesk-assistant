from typing import List

from rasa.shared.nlu.state_machine.state_machine_models import (
    IntentWithExamples,
)

import data_generation.parameterized_intents as parameterized_intents

from data_generation.models import Place
import data_generation.object_stories as object_stories
from data_generation.story_generation import (
    Story,
)

from actions import find_objects_action

places: List[Place] = []

places += [
    Place(
        name="The Holburne Museum",
        synonyms=[
            "museum",
            "antique museum",
            "art gallery",
            "art museum",
            "the museum",
        ],
        intro="The Holburne Museum has a great art collection. It has both modern and antique art.",
        hours="The Holburne museum is open right now. It's open from 10:00 AM to 5:00 PM on weekdays. On weekends, it's open from 11:00 AM to 7:00 PM.",
        more_details=None,
        price="Tickets for the Holburne Museum cost 12.50 euros for adults and 7.50 euros for children under 12.",
        directions=None,
        activities_provided=[],
        things_provided=[],
    ),
    Place(
        name="Museum of Bath Architecture",
        synonyms=["museum of architecture", "architecture museum"],
        intro="The Museum of Bath Architecture is great if you love architecture and design!",
        hours="The Museum of Bath Architecture is open from 12:00 PM to 6:00 PM on weekdays.",
        more_details="The Museum of Bath Architecture shows a history of Bath’s buildings.",
        price="Tickets for the Museum of Bath Architecture are 15 euros for adults and children under 12.",
        directions=None,
        activities_provided=[],
        things_provided=[],
    ),
    Place(
        name="Bath Abbey",
        synonyms=["abbey", "monastery", "church"],
        intro="The Bath Abbey is a famous medieval church in England.",
        hours="The Bath Abbey is open on Monday to Saturday from 10:00 AM to 3:45 PM.",
        more_details=None,
        price="The Bath Abbey tickets are 5 euros per person.",
        directions=None,
        activities_provided=[],
        things_provided=[],
    ),
    Place(
        name="Great Pultaney Bridge",
        synonyms=["bridge", "pultaney bridge"],
        intro="The Great Pulteney Bridge is a popular place for tourists.",
        hours="The Great Pulteney Bridge is open all day.",
        more_details=None,
        price="It is free to walk on the Great Pulteney Bridge.",
        directions=None,
        activities_provided=[],
        things_provided=[],
    ),
    Place(
        name="Roman Baths",
        synonyms=["baths", "roman ruins", "ruins"],
        intro="The Roman Baths are a very old historical monument.",
        hours="The Roman Baths are open from 10:00 AM to 6:00 PM everyday.",
        more_details="The Roman Baths are very popular for tourists!",
        price="On weekdays, tickets for the Roman Baths are 10 euros per person and 8 euros per person on weekends.",
        directions=None,
        activities_provided=[],
        things_provided=[],
    ),
    Place(
        name="Sally O's",
        synonyms=[
            "restaurant",
            "italian place",
            "the restaurant",
            "somewhere to eat",
            "place to eat",
            "cafe",
            "diner",
            "place with drinks",
            "place with food",
        ],
        question_intent=IntentWithExamples(
            examples=[
                "What about restaurants?",
                "I'm hungry",
                "I'd like to eat something",
                "I'd like to drink something",
                "Any idea where I can get some food?",
                "What's there to eat?",
                "I want to eat something",
                "What is there to eat around here?",
                "What do you recommend I eat?",
                "Any food recommendations?",
                "Is there a restaurant?",
            ]
        ),
        intro="There is a great restaurant around the corner. It’s called “Sally O’s”. You should go there!",
        hours="It's open for lunch and dinner. I'm not sure about the exact times",
        more_details="The restaurant is a cozy, family-run Italian restaurant.",
        price="I think it's fairly affordable. You can probably get a lunch for 10 euros.",
        directions=None,
        activities_provided=[],
        things_provided=[],
    ),
    Place(
        name="City Boat Tour",
        synonyms=["boat tour", "river tour"],
        intro="The boat tour is the most popular tour we have.",
        hours="The city boat tour is available from 9:00 AM to 5:00 PM. The first city boat tour starts at 9:00 AM. The last city boat tour starts at 4:30 PM.",
        more_details=None,
        price="The city boat tour costs 12 euros per person.",
        directions="The city boat tour takes 25 minutes.",
        activities_provided=[],
        things_provided=[],
    ),
    Place(
        name="City Bus Tour",
        synonyms=["bus tour"],
        intro="The city bus tour stops at famous historical monuments, such as the bath Abbey, the River Avon and the Great Pulteney Bridge.",
        hours="The city bus tour is available from 10:00 AM to 9:00 PM. The first city bus tour starts at 10:00 AM. Then, it starts every 30 minutes. The last city bus tour starts at 8:00 PM.",
        more_details=None,
        price="The city bus tour costs 20 euros per person.",
        duration="The city bus tour takes one hour.",
        directions=None,
        activities_provided=[],
        things_provided=[],
    ),
]


# Write place intents
parameterized_intent_creators = [
    parameterized_intents.intent_what_price_creator,
    parameterized_intents.intent_what_is_context_creator,
    parameterized_intents.intent_directions_creator,
    parameterized_intents.intent_is_there_a_context_creator,
    parameterized_intents.intent_is_there_a_place_to_verb_creator,
    parameterized_intents.intent_when_is_that_creator,
    parameterized_intents.intent_what_price_creator,
    parameterized_intents.intent_what_duration_creator,
    parameterized_intents.intent_ill_have_context_creator,
]

intents = [
    parameterized_intent_creator.create_parameterized_intent(
        context_name=find_objects_action.SLOT_OBJECT_NAME,
        context_value=place.name,
        context_value_synonyms=place.synonyms,
    )
    for place in places
    for parameterized_intent_creator in parameterized_intent_creators
]

# intents: List[IntentWithExamples] = []
# stories: List[Story] = []
# for place in places:
#     for parameterized_intent_creator in parameterized_intent_creators:
#         IntentWithExamples = parameterized_intent_creator.create_parameterized_intent(
#             context_name=object_stories.OBJECT_NAME_SLOT_NAME,
#             context_value=place.name,
#             context_value_synonyms=place.synonyms,
#         )
