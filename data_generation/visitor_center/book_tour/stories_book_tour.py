from rasa.shared.nlu.state_machine.state_machine_models import (
    Utterance,
    ActionName,
)

from data_generation.story_generation import IntentName

import data_generation.common_intents as common
import data_generation.visitor_center.book_tour.state_book_tour as book_tour

from data_generation.story_generation import Story, Fork, Or, OrActions

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
]
