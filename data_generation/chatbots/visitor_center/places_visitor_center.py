from typing import List

from rasa.shared.nlu.state_machine.state_machine_models import (
    IntentWithExamples,
)
import data_generation.chatbots.visitor_center.concepts_visitor_center as concepts_visitor_center

from data_generation.models.object_models import Place
from data_generation.common_nlu.things import Thing
from data_generation.common_nlu.types import Type
from data_generation.common_nlu import (
    common_intent_creators,
)

places: List[Place] = []

places += [
    Place(
        name="Holburne Museum",
        synonyms=[
            "Holburne Museum",
            "Holburn Museum",
            "Holburn",
        ],
        intro="The Holburne Museum has a great art collection. It has both modern and antique art.",
        types=[
            Type.place,
            Type.museum,
            Type.art_gallery,
        ],
        hours="The Holburne museum is open right now. It's open from 10:00 AM to 5:00 PM on weekdays. On weekends, it's open from 11:00 AM to 7:00 PM.",
        details=None,
        price="Tickets for the Holburne Museum cost 12.50 euros for adults and 7.50 euros for children under 12.",
        directions="The Holburne Museum is on the East side of the River Avon. You can take the A31 bus to get there.",
        activities_provided=[],
        things_provided=[
            Type.place,
            Thing.art,
            Thing.history,
            Thing.natural_history,
            Thing.sightseeing,
        ],
    ),
    Place(
        name="Museum of Bath Architecture",
        synonyms=["museum of architecture", "architecture museum"],
        intro="The Museum of Bath Architecture is great if you love architecture and design!",
        types=[Type.museum, Thing.sightseeing],
        hours="The Museum of Bath Architecture is open from 12:00 PM to 6:00 PM on weekdays.",
        details="The Museum of Bath Architecture shows a history of Bath’s buildings.",
        price="Tickets for the Museum of Bath Architecture are 15 euros for adults and children under 12.",
        directions="The Museum of Bath Architecture is along the River Avon. From here, it takes ten minutes on foot to get to the Museum of Bath Architecture.",
        activities_provided=[],
        things_provided=[
            Thing.art,
            Thing.history,
            Thing.natural_history,
            Thing.sightseeing,
        ],
    ),
    Place(
        name="Bath Abbey",
        synonyms=["the abbey"],
        intro="The Bath Abbey is a famous medieval church in England.",
        types=[Type.place, Type.place_of_worship],
        hours="The Bath Abbey is open on Monday to Saturday from 10:00 AM to 3:45 PM.",
        details=None,
        price="The Bath Abbey tickets are 5 euros per person.",
        directions="The Bath Abbey is a five minute walk from here. Go straight into the center of town. The Bath Abbey is on the left!",
        activities_provided=[],
        things_provided=[
            Thing.art,
            Thing.history,
            Thing.religion,
            Thing.sightseeing,
        ],
    ),
    Place(
        name="Great Pultaney Bridge",
        synonyms=["bridge", "pultaney bridge"],
        intro="The Great Pulteney Bridge is a popular place for tourists.",
        types=[
            Type.place,
        ],
        hours="The Great Pulteney Bridge is open all day.",
        details=None,
        price="It is free to walk on the Great Pulteney Bridge.",
        directions="We are on the left side of the Great Pulteney Bridge. You can go right outside and see the bridge!",
        activities_provided=[],
        things_provided=[
            Thing.shopping,
            Thing.sightseeing,
            Thing.history,
            concepts_visitor_center.river,
        ],
    ),
    Place(
        name="Roman Baths",
        synonyms=["baths"],
        intro="The Roman Baths are a very old historical monument.",
        types=[
            Type.place,
        ],
        hours="The Roman Baths are open from 10:00 AM to 6:00 PM everyday.",
        details="The Roman Baths are very popular for tourists!",
        price="On weekdays, tickets for the Roman Baths are 10 euros per person and 8 euros per person on weekends.",
        directions="You should walk to the Roman Baths. You can see many cool shops! Walk south along the River Avon and then make a right.",
        activities_provided=[],
        things_provided=[Thing.history, Thing.sightseeing, Thing.history],
    ),
    Place(
        name="Circle Diner",
        synonyms=[],
        question_intent=IntentWithExamples(
            examples=[
                "I'm hungry",
                "I'd like to eat something",
                "I'd like to drink something",
                "What's there to eat?",
                "I want to eat something",
                "What is there to eat around here?",
                "What do you recommend I eat?",
                "Any food recommendations?",
            ]
        ),
        intro="Circle Diner has great prices and excellent food.",
        types=[Type.place, Type.restaurant],
        hours="The Circle Diner is open all day!",
        details="Circle Diner is perfect for families.",
        price="Everything on the menu is half off from 2:00 PM to 5:00 PM.",
        directions="The Circle Diner is a bit far. You should take a taxi or car sharing service.",
        activities_provided=[],
        things_provided=[Thing.food, Thing.sightseeing],
    ),
    Place(
        name="City Boat Tour",
        synonyms=["boat tour", "river tour"],
        intro="The boat tour is the most popular tour we have.",
        hours="The city boat tour is available from 9:00 AM to 5:00 PM. The first city boat tour starts at 9:00 AM. The last city boat tour starts at 4:30 PM.",
        details=None,
        price="The city boat tour costs 12 euros per person.",
        directions="The pickup location for the city boat tour is right outside the Visitor’s Center.",
        activities_provided=[],
        things_provided=[Thing.sightseeing],
    ),
    Place(
        name="City Bus Tour",
        synonyms=["bus tour"],
        intro="The city bus tour stops at famous historical monuments, such as the bath Abbey, the River Avon and the Great Pulteney Bridge.",
        hours="The city bus tour is available from 10:00 AM to 9:00 PM. The first city bus tour starts at 10:00 AM. Then, it starts every 30 minutes. The last city bus tour starts at 8:00 PM.",
        details=None,
        price="The city bus tour costs 20 euros per person.",
        duration="The city bus tour takes one hour.",
        directions="The pickup location for the city bus tour is right outside the Visitor’s Center.",
        activities_provided=[],
        things_provided=[Thing.sightseeing],
    ),
]


# Write place intents
intents = [
    parameterized_intents.create_parameterized_intent(
        entity_value=place.name,
        entity_synonyms=place.synonyms,
    )
    for place in places
    for parameterized_intents in common_intent_creators.intent_creators
]

# Write place with things intents
intents += [
    common_intent_creators.intent_is_there_a_place_with_thing_creator.create_parameterized_intent(
        entity_value=thing.name,
        entity_synonyms=thing.synonyms,
    )
    for place in places
    for thing in place.things_provided
]

# Write place with intents
intents += [
    common_intent_creators.intent_is_there_a_type_creator.create_parameterized_intent(
        entity_value=place.name,
        entity_synonyms=place.synonyms,
    )
    for place in places
]

# Write place with type intents
intents += [
    common_intent_creators.intent_is_there_a_type_creator.create_parameterized_intent(
        entity_value=type.name,
        entity_synonyms=type.synonyms,
    )
    for place in places
    for type in place.types
]

# intents: List[IntentWithExamples] = []
# stories: List[Story] = []
# for place in places:
#     for parameterized_intents in parameterized_intentss:
#         IntentWithExamples = parameterized_intents.create_parameterized_intent(
#             entity_name=object_stories.OBJECT_NAME_SLOT_NAME,
#             entity_value=place.name,
#             entity_synonyms=place.synonyms,
#         )
