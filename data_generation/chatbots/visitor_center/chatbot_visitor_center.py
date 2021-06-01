import data_generation.chatbots.visitor_center.book_tour.state_book_tour as state_book_tour
import data_generation.chatbots.visitor_center.book_tour.stories_book_tour as stories_book_tour
import data_generation.chatbots.visitor_center.buy_citypass.state_buy_citypass as state_buy_citypass
import data_generation.chatbots.visitor_center.places_visitor_center as places_visitor_center
import data_generation.chatbots.visitor_center.state_visitor_center as state_visitor_center
import data_generation.chatbots.visitor_center.stories_visitor_center as stories_visitor_center
from data_generation.state_machine import StateMachine
from data_generation.chatbot import Chatbot

state_machine = StateMachine(
    initial_state=state_visitor_center.start_state,
    other_states=[
        state_buy_citypass.buy_citypass_state,
        state_book_tour.book_tour_state,
    ],
)

stories = (
    stories_visitor_center.stories_tell_me_more
    + stories_book_tour.stories_tours
    + stories_visitor_center.stories_what_time
    + [
        story
        for place in places_visitor_center.places
        for story in place.generate_stories()
    ]
)

chatbot = Chatbot(
    state_machine=state_machine,
    stories=stories,
    question_answer_context_file_path="./data_generation/chatbots/visitor_center/context.txt",
)
