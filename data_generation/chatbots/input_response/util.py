import requests
from typing import Any, Dict, List


def get_curricula() -> List[Any]:
    response = requests.get(
        "https://xm15z6i3.api.sanity.io/v1/data/query/chatbot?query=*[_type == 'curriculum' %26%26 name == \"Staging\"]"
    )

    curriculum = response.json()

    return curriculum["result"]


def get_text_input_recursive(object: Any) -> List[str]:
    all_responses = []

    if isinstance(object, list):
        for element in object:
            all_responses.extend(get_text_input_recursive(element))
    elif isinstance(object, dict):
        if object.get("_type") == "textInputQuestion":
            all_responses.append(object)
        else:
            for value in object.values():
                all_responses.extend(get_text_input_recursive(value))

    return all_responses


def flatten_text_input(input_response: Dict) -> List[Any]:
    flattened = []
    question = input_response.get("question")
    for inputResponse in input_response.get("inputResponses", []):
        inputs = inputResponse.get("inputs")
        key = inputResponse.get("_key")
        is_correct = inputResponse.get("isCorrect")

        flattened.append(
            {
                "question_id": key,
                "question": question,
                "inputs": inputs,
                "is_correct": is_correct,
            }
        )

    return flattened


def get_input_responses() -> List[Any]:
    curricula = get_curricula()

    text_inputs = get_text_input_recursive(curricula)

    return [
        text_input_flattened
        for input_response in text_inputs
        for text_input_flattened in flatten_text_input(input_response)
    ]


# get_input_responses()
