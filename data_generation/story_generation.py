from typing import List, Dict, Optional, Set, Tuple, Union
from pydantic import BaseModel

from rasa.shared.nlu.state_machine.state_machine_models import (
    Intent,
    Utterance,
)

from rasa.shared.nlu.state_machine.state_machine_state import (
    Action,
)

from rasa.shared.nlu.state_machine.yaml_convertible import StoryYAMLConvertable

from rasa.shared.core.domain import Domain

from rasa.shared.utils.io import dump_obj_as_yaml_to_string, write_text_file

from rasa.shared.nlu.training_data.formats import RasaYAMLReader

import rasa.shared.utils.validation

import rasa.shared.constants


class Or(StoryYAMLConvertable):
    intents: List[Union[Intent, str]]

    def __init__(self, *args: Union["Or", Intent, Utterance, str]) -> None:
        self.intents = list(args)

    def as_nlu_yaml(self):
        pass


class Fork(StoryYAMLConvertable):
    paths: List[List[Union["Or", Intent, Utterance, str, "Fork"]]]

    def __init__(
        self, *args: List[Union["Or", Intent, Utterance, str, "Fork"]]
    ) -> None:
        self.paths = list(args)

    def as_nlu_yaml(self):
        pass


class IntentName(BaseModel):
    name: str


class ActionName(BaseModel):
    name: str


class Story:
    paths: List[Union["Or", Intent, Utterance, IntentName, ActionName]]
    name: str

    def __init__(
        self,
        name: str,
        elements: Union["Or", Intent, Utterance, str, Fork],
    ) -> None:
        self.paths = elements
        self.name = name

        # Only the last element may be a fork
        for element in elements[:-1]:
            assert not isinstance(element, Fork)

    def get_domain_nlu(self) -> Tuple[Domain, List[Dict], Set[Intent]]:
        story_nlu_steps: List[str] = []
        last_element: Optional[Intent] = None

        sub_domains: List[Domain] = []
        sub_nlus: List[Dict] = []

        all_intents: Set[Intent] = set()
        all_utterances: Set[Utterance] = set()
        all_actions: Set[Action] = set()
        # all_slots: Set[Slot] = []

        for element in self.paths:
            if isinstance(element, Intent):
                all_intents.add(element)

                # Add to current story
                story_nlu_steps.append({"intent": element.name})
            elif isinstance(element, str):
                # Add to current storry
                story_nlu_steps.append({"intent": element})
            elif isinstance(element, Utterance):
                all_utterances.add(element)

                # Add to current story
                story_nlu_steps.append({"action": element.name})
            elif isinstance(element, Or):
                intents_nlu: List[Dict[str, str]] = []
                # Write NLU for each intent
                for intent in element.intents:
                    if isinstance(intent, str):
                        intents_nlu.append({"intent": intent})
                    elif isinstance(intent, Intent):
                        all_intents.add(intent)
                        intents_nlu.append({"intent": intent.name})

                # Write NLU
                story_nlu_steps.append({"or": intents_nlu})
            elif isinstance(element, Fork):
                if last_element:
                    assert isinstance(last_element, Utterance)

                # Start a new story for every fork
                for index, path in enumerate(element.paths):
                    story = Story(
                        name=f"{self.name}_fork_{index}",
                        elements=[last_element] + path,
                    )

                    sub_domain, sub_nlu, sub_intents = story.get_domain_nlu()
                    sub_domains.append(sub_domain)
                    sub_nlus += sub_nlu
                    all_intents.update(sub_intents)
            else:
                raise RuntimeError(f"Unknown element type found: {element}")

            last_element = element

        # Persist domain
        domain = Domain(
            intents=[intent.name for intent in all_intents],
            entities=[],  # List of entity names
            slots=[],
            responses={
                utterance.name: [{"text": utterance.text}]
                for utterance in all_utterances
            },
            action_names=[action.name for action in all_actions],
            forms={},
            action_texts=[],
        )

        # Merge sub-domains
        for sub_domain in sub_domains:
            domain = domain.merge(sub_domain)

        # Save current story
        story_nlu = [{"story": self.name, "steps": story_nlu_steps}] + sub_nlus

        return (domain, story_nlu, all_intents)


def persist(stories: List[Story], domain_filename: str, nlu_filename: str):
    all_domain = Domain.empty()
    all_intents: Set[Intent] = set()
    all_stories: List[Story] = []

    for story in stories:
        domain, stories, intents = story.get_domain_nlu()

        all_domain = all_domain.merge(domain)
        all_intents.update(intents)
        all_stories.extend(stories)

    # Persist domain
    rasa.shared.utils.validation.validate_yaml_schema(
        domain.as_nlu_yaml(), rasa.shared.constants.DOMAIN_SCHEMA_FILE
    )

    # Write domain
    all_domain.persist(domain_filename)

    # Write NLU
    nlu_data = {
        "version": "2.0",
        "nlu": [intent.as_nlu_yaml() for intent in all_intents],
        "stories": all_stories,
    }

    nlu_data_yaml = dump_obj_as_yaml_to_string(
        nlu_data, should_preserve_key_order=True
    )

    RasaYAMLReader().validate(nlu_data_yaml)

    write_text_file(nlu_data_yaml, nlu_filename)
