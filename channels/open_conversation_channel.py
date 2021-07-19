import inspect
from sanic import Blueprint, response
from sanic.request import Request
from sanic.response import HTTPResponse
from typing import Text, Dict, Any, Optional, Callable, Awaitable, NoReturn
from rasa.core.actions.action import ActionRetrieveResponse
from rasa.core.channels.channel import (
    InputChannel,
    CollectingOutputChannel,
    UserMessage,
)


class OpenConversationOutputChannel(CollectingOutputChannel):
    @classmethod
    def name(cls) -> Text:
        return "open_conversation_output"

    async def send_response(
        self, recipient_id: Text, message: Dict[Text, Any]
    ) -> None:
        """Send a message to the client."""
        if message.get("text"):
            await self.send_text_message(
                recipient_id,
                message.get("text"),
                message.get("utter_action"),  # Include the utter_action
            )
        else:
            super().send_response(recipient_id, message)

    async def send_text_message(
        self,
        recipient_id: Text,
        text: Text,
        utter_action: Optional[Text],
        **kwargs: Any
    ) -> None:
        for message_part in text.strip().split("\n\n"):
            custom = None

            if utter_action:
                custom = {
                    "utter_action": utter_action,
                    "intent": ActionRetrieveResponse.intent_name_from_action(
                        utter_action
                    ),
                }
            await self._persist_message(
                self._message(recipient_id, text=message_part, custom=custom)
            )


class OpenConversationChannel(InputChannel):
    def name(self) -> Text:
        """Name of your custom channel."""
        return "openconversation"

    def get_metadata(self, request: Request) -> Optional[Dict[Text, Any]]:
        return request.json.get("metadata")

    # def get_character_name(self, request: Request) -> Optional[str]:
    #     metadata = self.get_metadata(request)

    #     if metadata:
    #         return metadata.get("character")
    #     else:
    #         return None

    def blueprint(
        self, on_new_message: Callable[[UserMessage], Awaitable[None]]
    ) -> Blueprint:

        custom_webhook = Blueprint(
            "custom_webhook_{}".format(type(self).__name__),
            inspect.getmodule(self).__name__,
        )

        @custom_webhook.route("/", methods=["GET"])
        async def health(request: Request) -> HTTPResponse:
            return response.json({"status": "ok"})

        @custom_webhook.route("/webhook", methods=["POST"])
        async def receive(request: Request) -> HTTPResponse:
            sender_id = request.json.get("sender")  # method to get sender_id
            text = request.json.get("message")  # method to fetch text
            input_channel = self.name()  # method to fetch input channel
            metadata = self.get_metadata(request)

            collector = OpenConversationOutputChannel()

            await on_new_message(
                UserMessage(
                    text,
                    collector,
                    sender_id,
                    input_channel=input_channel,
                    metadata=metadata,
                )
            )

            return response.json(collector.messages)

        return custom_webhook
