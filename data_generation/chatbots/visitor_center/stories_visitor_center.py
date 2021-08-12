from rasa.shared.nlu.state_machine.state_machine_models import (
    IntentWithExamples,
    Utterance,
)

import data_generation.common_nlu.common_intents as common
from data_generation.models.story_models import (
    Intent,
    Or,
    Story,
)

# Tell me more
stories_tell_me_more = [
    Story(
        [
            IntentWithExamples(examples=["What's there to do around here?"]),
            Utterance(
                "The Roman Baths are my favorite thing to see in Bath. You could also check out the Museum of Bath Architecture or the Bath Abbey."
            ),
        ]
    ),
    Story(
        [
            Or(common.intent_what_do_you_do, Intent("help")),
            Utterance(
                "I help visitors who want to explore the town by giving them information about the places around here. I can also help with booking tours. You can also buy the CityPass here which lets you go to attractions at a discount."
            ),
        ]
    ),
    Story(
        [
            IntentWithExamples(
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
    Story(
        [
            common.intent_ask_weather,
            Utterance(
                "It's a fine day in Bath. We don't get too much rain here so you nothing to worry about."
            ),
        ]
    ),
]

# What time?
# stories_what_time = [
#     Story(
#         [
#             IntentWithExamples(
#                 examples=[
#                     "What are your hours?",
#                     "When do you open?",
#                     "When do you close?",
#                     "What time do you open until?",
#                     "What time do you close?",
#                     "Are you still open?",
#                 ]
#             ),
#             Utterance("We're open from 11am to 9pm, every day."),
#         ]
#     ),
# ]

intent_select_boat_tour = IntentWithExamples(
    examples=[
        "The boat tour",
        "The city tour",
        "The first one",
        "The former",
        "First",
        "boat",
        "I would prefer the boat one",
        "The 3pm",
        "The one at 3 o clock",
        "The tour at 3",
        "3 sounds good",
    ]
)

intent_select_bus_tour = IntentWithExamples(
    examples=[
        "The bus tour",
        "bus",
        "I would prefer the bus one",
        "The last one",
        "The latter",
        "The second",
        "The second one",
        "The 4pm",
        "The one at 4 o clock",
        "The tour at 4",
        "4 sounds good",
        "Four",
    ]
)

# stories_tours = [
#     Story(
#         name="tours",
#         elements=[
#             # IntentWithExamples(
#             #     examples=[
#             #         "I want to buy a ticket",
#             #         "Can I have a ticket?",
#             #         "I buy tickets",
#             #         "Give me a ticket",
#             #     ]
#             # ),
#             Intent(common_creators.intent_i_want_to_buy_creator.name),
#             SlotWasSet(
#                 [{find_objects_action.SLOT_OBJECT_NAME_OR_TYPE: "ticket"}]
#             ),
#             Utterance("Which one? The bus tour, boat tour or the CityPass?"),
#             Fork(
#                 [
#                     intent_select_boat_tour,
#                     stories_book_tour.utter_put_down_boat_tour,
#                     ActionName("action_set_tour_boat"),
#                     # TODO: StateMachineTransition
#                 ],
#                 [
#                     intent_select_bus_tour,
#                     stories_book_tour.utter_put_down_bus_tour,
#                     ActionName("action_set_tour_bus"),
#                     # TODO: StateMachineTransition
#                 ],
#                 [
#                     state_visitor_center.intent_buy_citypass,
#                     # TODO: StateMachineTransition
#                 ],
#                 [
#                     Or(
#                         common.intent_what_do_you_recommend,
#                         common.intent_not_sure,
#                         Intent("help"),
#                     ),
#                     Utterance(
#                         "I'd personally go with the CityPass as I love museums."
#                     ),
#                     Fork(
#                         [
#                             Or(
#                                 common.intent_sure_ill_get_that,
#                                 Intent("affirm"),
#                             ),
#                             # TODO: StateMachineTransition
#                         ],
#                         [Intent("deny"), Utterance("It's up to you."),],
#                         # TODO: Handle "nothing" condition
#                     ),
#                 ],
#             ),
#         ],
#     ),
# ]

# What time?
stories_chitchat = [
    Story(
        [
            Or(Intent("greet"), common.intent_ask_name),
            Utterance(
                "Nice to meet you, I'm Patrick. I help visitors with questions about Bath.",
                name="utter_nice_to_meet_you",
            ),
        ]
    ),
    # Story(
    #     [
    #         IntentWithExamples(
    #             examples=[
    #                 "Do you like it here?",
    #                 "Do you like Bath?",
    #                 "What do you think about the city?",
    #                 "What's your opinion of Bath?",
    #             ]
    #         ),
    #         Utterance(
    #             "Nice to meet you, I'm Patrick. I help visitors with questions about Bath.",
    #             name="utter_nice_to_meet_you",
    #         ),
    #     ]
    # ),
]
