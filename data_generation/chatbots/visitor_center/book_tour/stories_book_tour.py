import actions
from actions import find_objects_action
from rasa.shared.nlu.state_machine.state_machine_models import (
    ActionName,
    Utterance,
)

import data_generation.common_nlu.common_intents as common
import data_generation.common_nlu.common_intent_creators as common_creators
import data_generation.chatbots.visitor_center.book_tour.state_book_tour as book_tour
from data_generation.chatbots.visitor_center import places_visitor_center
from data_generation.models.story_models import (
    Intent,
    SlotWasSet,
    Story,
    Fork,
    Or,
)

utter_put_down_boat_tour = Utterance(
    "Sure, I'll put you down for the 3pm boat tour then."
)

utter_put_down_bus_tour = Utterance(
    "Sure, I'll put you down for the 4pm bus tour then."
)

utter_recommend_boat = Utterance(
    "May I recommend the boat tour? It's a refreshing way to see the city."
)

stories_tours = [
    Story(
        name="tours",
        elements=[
            book_tour.action_ask_tour,
            Fork(
                [
                    Intent(common_creators.intent_i_want_to_buy_creator.name),
                    SlotWasSet(
                        [
                            {
                                find_objects_action.SLOT_OBJECT_NAME_OR_TYPE: places_visitor_center.city_boat_tour.name
                            }
                        ]
                    ),
                    utter_put_down_boat_tour,
                    ActionName("action_set_tour_boat"),
                ],
                [
                    Intent(common_creators.intent_i_want_to_buy_creator.name),
                    SlotWasSet(
                        [
                            {
                                find_objects_action.SLOT_OBJECT_NAME_OR_TYPE: places_visitor_center.city_bus_tour.name
                            }
                        ]
                    ),
                    utter_put_down_bus_tour,
                    ActionName("action_set_tour_bus"),
                ],
                [
                    Or(
                        common.intent_what_do_you_recommend,
                        common.intent_not_sure,
                        Intent("help"),
                    ),
                    utter_recommend_boat,
                    Fork(
                        [
                            Or(
                                common.intent_sure_ill_get_that,
                                common.intent_affirm,
                            ),
                            Utterance("Great, the boat tour then."),
                            # TODO: Set slot
                            ActionName("action_set_tour_boat"),
                        ],
                        [Intent("deny"), Utterance("It's up to you."),],
                        # TODO: Handle "nothing" condition
                    ),
                ],
            ),
        ],
    ),
]
