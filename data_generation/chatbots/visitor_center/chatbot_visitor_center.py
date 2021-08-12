import data_generation.chatbots.visitor_center.book_tour.state_book_tour as state_book_tour
import data_generation.chatbots.visitor_center.buy_citypass.state_buy_citypass as state_buy_citypass
import data_generation.chatbots.visitor_center.state_visitor_center as state_visitor_center
import data_generation.chatbots.visitor_center.stories_visitor_center as stories_visitor_center
import data_generation.common_nlu.object_stories as object_stories
import data_generation.common_nlu.common_stories as common_stories
from data_generation.models import input_response_service
from data_generation.models.state_machine import StateMachine
from data_generation.models.chatbot import Chatbot
import data_generation.chatbots.visitor_center.places_visitor_center as places


state_machine = StateMachine(
    initial_state=state_visitor_center.start_state,
    other_states=[
        state_buy_citypass.buy_citypass_state,
        state_book_tour.book_tour_state,
    ],
)

stories = (
    stories_visitor_center.stories_tell_me_more
    # + stories_book_tour.stories_tours
    # + stories_visitor_center.stories_what_time
    + stories_visitor_center.stories_chitchat
    + object_stories.stories
    + common_stories.stories_chitchat
    + input_response_service.get_stories(worksheet_filter=["visitor_center"])
)

chatbot = Chatbot(
    state_machine=state_machine,
    stories=stories,
    objects=places.places,
    additional_intents=places.intents,
)
