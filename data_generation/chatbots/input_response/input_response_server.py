from fastapi import Depends, FastAPI
import requests
import os
from typing import List
from pydantic import BaseModel
import json

app = FastAPI()

# os.getenv("RASA_NLU_SERVER_URI")
RASA_NLU_SERVER_URI = "http://localhost:4444/model/parse"

# TODO: Download the input_response from Sanity


class InputResponseRequest(BaseModel):
    input_response_ids: List[str]
    text: str


class InputResponseResponse(BaseModel):
    intent_name: str
    confidence: float


IS_DEBUG = os.getenv("IS_DEBUG")


@app.post("/predict/intent_response", response_model=InputResponseResponse)
def predict(request: InputResponseRequest):
    response = requests.post(
        RASA_NLU_SERVER_URI, data=json.dumps({"text": request.text})
    )

    input_responses = response.json()

    if IS_DEBUG:
        print(input_responses)

    # Filter response IDs that matter
    intents = [
        input_response
        for input_response in input_responses["intent_ranking"]
        if input_response["name"] in request.input_response_ids
        or not input_response["name"].startswith("input")
    ]

    # Scale confidences
    intentConfidenceSum = 0
    for intent in intents:
        intentConfidenceSum += intent["confidence"]
    for intent in intents:
        intent["confidence"] /= intentConfidenceSum

    # Filter
    intent = max(intents, key=lambda intent: intent["confidence"])

    return InputResponseResponse(
        intent_name=intent["name"], confidence=intent["confidence"]
    )
