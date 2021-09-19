import os
from data_generation.chatbots.visitor_center.chatbot_visitor_center import (
    chatbot as visitor_center_chatbot,
)
from data_generation.chatbots.text_input.chatbot import (
    chatbot as text_input_chatbot,
)

target_chatbot_id = os.getenv("CHATBOT_ID")

CHATBOT_DICT = {
    "visitor_center": visitor_center_chatbot,
    "text_input": text_input_chatbot,
}

chatbot = CHATBOT_DICT.get(target_chatbot_id)

if chatbot:
    chatbot.persist(
        domain_folder=f"domain/{target_chatbot_id}",
        nlu_folder=f"data/{target_chatbot_id}",
    )
