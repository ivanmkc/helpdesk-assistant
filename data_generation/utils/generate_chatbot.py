import os
from data_generation.chatbots.visitor_center.chatbot_visitor_center import (
    chatbot as visitor_center_chatbot,
)
from data_generation.chatbots.input_response.chatbot import (
    chatbot as input_response_chatbot,
)

target_chatbot_id = os.getenv("CHATBOT_ID")

if not target_chatbot_id:
    raise RuntimeError("CHATBOT_ID environment variable was not set.")

CHATBOT_DICT = {
    "visitor-center": visitor_center_chatbot,
    "input-response": input_response_chatbot,
}

chatbot = CHATBOT_DICT.get(target_chatbot_id)

if chatbot:
    chatbot.persist(
        domain_folder=f"domain/{target_chatbot_id}",
        nlu_folder=f"data/{target_chatbot_id}",
    )
else:
    raise RuntimeError(f"No chatbot found for id = {target_chatbot_id}.")
