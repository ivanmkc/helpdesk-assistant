import data_generation.chatbots.visitor_center.book_tour.state_book_tour as state_book_tour
import data_generation.chatbots.visitor_center.buy_citypass.state_buy_citypass as state_buy_citypass
import data_generation.chatbots.visitor_center.state_visitor_center as state_visitor_center
import data_generation.common_nlu.object_stories as object_stories
import data_generation.common_nlu.common_stories as common_stories
from data_generation.models import input_response_service
from data_generation.models.state_machine import StateMachine
from data_generation.models.chatbot import Chatbot
from data_generation.models.story_models import Intent, Story
from rasa.shared.nlu.state_machine.state_machine_models import (
    ActionName,
    Utterance,
)

# state_machine = StateMachine(
#     initial_state=state_visitor_center.start_state,
#     other_states=[
#         state_buy_citypass.buy_citypass_state,
#         state_book_tour.book_tour_state,
#     ],
# )

# sold_out_stories = [
#     Story(
#         [
#             ActionName("action_trigger_buy_citypass"),
#             Utterance("Sorry, we are sold out at the moment."),
#         ]
#     ),
#     Story(
#         [
#             ActionName("action_trigger_book_tour"),
#             Utterance("Sorry, we are sold out of the tours at the moment."),
#         ]
#     ),
# ]
input_response_stories = input_response_service.get_stories(
    [
        "alice",
        "chitchat",
        "personal",
        "family",
        "occupation",
    ]
)

stories = (
    object_stories.stories
    + common_stories.stories_chitchat
    + input_response_stories
)

chatbot = Chatbot(
    state_machine=None,
    stories=stories,
    objects=[],
    additional_intents=[],
    additional_slots=[],
)
