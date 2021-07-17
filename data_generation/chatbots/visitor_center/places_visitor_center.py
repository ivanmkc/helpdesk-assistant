from typing import List

from rasa.shared.nlu.state_machine.state_machine_models import (
    IntentWithExamples,
)
import data_generation.chatbots.visitor_center.concepts_visitor_center as concepts_visitor_center

from data_generation.models.object_models import Place, BuyInfo
from data_generation.common_nlu.things import Thing
from data_generation.common_nlu.types import Type
from data_generation.common_nlu import common_intent_creators

places: List[Place] = []

city_boat_tour = Place(
    name="City Boat Tour",
    synonyms=["boat tour", "river tour"],
    intro="We have a boat tour of Bath on the River Avon at 3:00 PM.",
    types=[Type.ticket, Type.tour],
    buy_info=BuyInfo(
        slot_name="tour_type",
        number_slot_name="tour_num_tickets",
        trigger_name="action_trigger_book_tour",
    ),
    hours="The City Boat Tour is available from 9:00 AM to 5:00 PM. The first City Boat Tour starts at 9:00 AM. The last City Boat Tour starts at 4:30 PM.",
    details=None,
    price="The City Boat Tour costs 12 pounds per person.",
    directions="The pickup location for the City Boat Tour is right outside the Visitor’s Center.",
    opinion="I think it's the best way to see the city.",
    things_provided=[Thing.sightseeing],
)

city_bus_tour = Place(
    name="City Bus Tour",
    synonyms=["bus tour"],
    intro="The City Bus Tour stops at famous historical monuments, such as the Bath Abbey, the River Avon and the Great Pulteney Bridge.",
    types=[Type.ticket, Type.tour],
    buy_info=BuyInfo(
        slot_name="tour_type",
        number_slot_name="tour_num_tickets",
        trigger_name="action_trigger_book_tour",
    ),
    hours="The City Bus Tour is available from 10:00 AM to 9:00 PM. The first City Bus Tour starts at 10:00 AM. Then, it starts every 30 minutes. The last City Bus Tour starts at 8:00 PM.",
    details=None,
    price="The City Bus Tour costs 20 pounds per person.",
    duration="The City Bus Tour takes one hour.",
    directions="The pickup location for the City Bus Tour is right outside the Visitor’s Center.",
    opinion="Not a bad way to spend an hour.",
    things_provided=[Thing.sightseeing],
)

city_pass = Place(
    name="CityPass",
    synonyms=["City Pass"],
    intro="The CityPass let's you see all of the city's attractions, including museums and galleries over 3 days. There are over 10 locations.",
    types=[Type.ticket],
    buy_info=BuyInfo(
        slot_name="tour_type",
        number_slot_name="citypass_num_tickets",
        trigger_name="action_trigger_buy_citypass",
    ),
    hours="You can use the CityPass over the course of 3 days. Your time begins when you use it at the first attraction.",
    details=None,
    price="You can buy the CityPass here for 50 pounds per person.",
    duration="You can use the CityPass over the course of 3 days. Your time begins when you use it at the first attraction.",
    directions="You can buy the CityPass right here!",
    opinion="It's a great deal if you plan to see several attractions.",
    things_provided=[],
)

places += [
    Place(
        name="Visitor Center",
        synonyms=["you", "your center"],
        intro="Bath is the city we're in right now.",
        types=[],
        hours="We're open from 11am to 9pm, every day.",
        details=None,
        opinion="I love working here and introducing people to this beautiful city.",
        things_provided=[],
    ),
    Place(
        name="Bath",
        synonyms=["The city of Bath", "Bath city"],
        intro="Bath is the city we're in right now.",
        types=[],
        hours="Most stores close by 6pm but restaurants should be open until at least 10pm.",
        details=None,
        directions="The buses are a convenient way to get around the city.",
        opinion="I love Bath! It’s safe, beautiful, and has many interesting sights.",
        things_provided=[],
    ),
    Place(
        name="Holburne Museum",
        synonyms=["Holburne Museum", "Holburn Museum", "Holburn",],
        intro="The Holburne Museum has a great art collection. It has both modern and antique art.",
        types=[Type.place, Type.museum, Type.art_gallery,],
        hours="The Holburne museum is open right now. It's open from 10:00 AM to 5:00 PM on weekdays. On weekends, it's open from 11:00 AM to 7:00 PM.",
        details=None,
        price="Tickets for the Holburne Museum cost 12.50 pounds for adults and 7.50 pounds for children under 12.",
        directions="The Holburne Museum is on the East side of the River Avon. You can take the A31 bus to get there.",
        opinion="I love it, it's one of my favorite attractions in the city.",
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
        price="Tickets for the Museum of Bath Architecture are 15 pounds for adults and children under 12.",
        directions="The Museum of Bath Architecture is along the River Avon. From here, it takes ten minutes on foot to get to the Museum of Bath Architecture.",
        opinion="I love it, it's one of my favorite attractions in the city.",
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
        price="The Bath Abbey tickets are 5 pounds per person.",
        directions="The Bath Abbey is a five minute walk from here. Go straight into the center of town. The Bath Abbey is on the left!",
        opinion="The Bath Abbey is a great place to see some stellar historical architecture.",
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
        types=[Type.place,],
        hours="The Great Pulteney Bridge is open all day.",
        details=None,
        price="It is free to walk on the Great Pulteney Bridge.",
        directions="We are on the left side of the Great Pulteney Bridge. You can go right outside and see the bridge!",
        opinion="The shops here are a little expensive but you can take some really nice photos!",
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
        types=[Type.place,],
        hours="The Roman Baths are open from 10:00 AM to 6:00 PM everyday.",
        details="The Roman Baths are very popular for tourists!",
        price="On weekdays, tickets for the Roman Baths are 10 pounds per person and 8 pounds per person on weekends.",
        directions="You should walk to the Roman Baths. You can see many cool shops! Walk south along the River Avon and then make a right.",
        opinion="I wish I had a chance to bathe there back when it was in use.",
        things_provided=[Thing.history, Thing.sightseeing, Thing.history],
    ),
    Place(
        name="Circle Diner",
        synonyms=[],
        question_intent=IntentWithExamples(
            examples=[
                "I'm hungry",
                "I'm very hungry",
                "I'd like to eat something",
                "I'd like to drink something",
                "What's there to eat?",
                "I want to eat something",
                "What is there to eat around here?",
                "What do you recommend I eat?",
                "Any food recommendations?",
            ],
            name="intent_ask_restaurant",
        ),
        intro="Circle Diner has great prices and excellent food.",
        types=[Type.place, Type.restaurant],
        hours="The Circle Diner is open all day!",
        details="Circle Diner is perfect for families.",
        price="Everything on the menu is half off from 2:00 PM to 5:00 PM.",
        directions="The Circle Diner is a bit far. You should take a taxi or car sharing service.",
        opinion="Food is great and prices are fair. What's not to love?",
        things_provided=[Thing.food, Thing.sightseeing],
    ),
    Place(
        name="SouthGate Shopping Center",
        synonyms=["SouthGate", "Shopping Center"],
        question_intent=None,
        intro="SouthGate is a shopping center with over 50 shops and 10 restaurants. It's a great place to go shopping and relax.",
        types=[Type.place],
        hours="The SouthGate Shopping center is open Monday through Saturday from 9:00 AM to 6:00 PM. On Sunday it is open from 11:00 AM to 5:00 PM.",
        details="You can get pizza, coffee, donuts, and cafe food.",
        price="Entry is free, and the shops range from cheap to expensive.",
        directions="The SouthGate shopping center is a 10 minute walk from here.",
        opinion="You can buy almost anything there! They have clothing shops and electronics stores.",
        things_provided=[Thing.food, Thing.shopping],
    ),
    Place(
        name="Comedy Festival",
        synonyms=["Bath Comedy Festival"],
        question_intent=None,
        intro="The Bath Comedy Festival happens once every year, and it's very popular!",
        types=[Type.event],
        hours="There is a Bath Comedy Festival today and tomorrow from noon to midnight.",
        details="At the festival, over 50 British comedians have shows!",
        price="You can buy tickets at the festival. Tickets are $10 per person.",
        directions="The Bath Comedy Festival is nearby. It's at the Sydney Gardens.",
        opinion="I think the festival is perfect for the whole family! It's a great time.",
        things_provided=[Thing.entertainment],
    ),
    Place(
        name="Carnival",
        synonyms=["Royal Victoria Park Carnival"],
        question_intent=None,
        intro="There is a carnival at Royal Victoria Park this week. It has rides, games, and theatre shows.",
        types=[Type.event],
        hours="The carnival starts at 9:00 AM and finishes at midnight each day this week.",
        price="Entry to the carnival at Royal Victoria Park costs £10.00 per person.",
        directions="It's a 15 minute walk away. You can also take the 20 A Bus. It stops across the street.",
        opinion="It is a lot of fun, but you need to buy tickets there.",
        things_provided=[Thing.entertainment],
    ),
    city_boat_tour,
    city_bus_tour,
    city_pass,
]


# Write place intents
intents = [
    parameterized_intents.create_parameterized_intent(
        entity_value=place.name, entity_synonyms=place.synonyms,
    )
    for place in places
    for parameterized_intents in common_intent_creators.intent_creators
]

# Write place with things intents
intents += [
    common_intent_creators.intent_is_there_a_place_with_thing_creator.create_parameterized_intent(
        entity_value=thing.name, entity_synonyms=thing.synonyms,
    )
    for place in places
    for thing in place.things_provided
]

# Write place with intents
intents += [
    common_intent_creators.intent_is_there_a_type_creator.create_parameterized_intent(
        entity_value=place.name, entity_synonyms=place.synonyms,
    )
    for place in places
]

# Write place with type intents
intents += [
    common_intent_creators.intent_is_there_a_type_creator.create_parameterized_intent(
        entity_value=type.name, entity_synonyms=type.synonyms,
    )
    for place in places
    for type in place.types
]

# Write things to buy
intents += [
    common_intent_creators.intent_i_want_to_buy_creator.create_parameterized_intent(
        entity_value=thing_to_buy.name, entity_synonyms=thing_to_buy.synonyms,
    )
    for thing_to_buy in [city_boat_tour, city_bus_tour, city_pass]
]

# Write disambiguations
intents += [
    common_intent_creators.intent_context_only_creator.create_parameterized_intent(
        entity_value=thing_to_buy.name, entity_synonyms=thing_to_buy.synonyms,
    )
    for thing_to_buy in [city_boat_tour, city_bus_tour, city_pass]
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
