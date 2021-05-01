from typing import List, Dict, Optional, Set, Union

from rasa.shared.nlu.state_machine.state_machine_models import (
    Intent,
    Utterance,
)

from rasa.shared.nlu.state_machine.state_machine_state import (
    Action,
)

from rasa.shared.nlu.state_machine.yaml_convertible import YAMLConvertable

from rasa.shared.core.domain import Domain

from rasa.shared.utils.io import dump_obj_as_yaml_to_string, write_text_file

from rasa.shared.nlu.training_data.formats import RasaYAMLReader
import os


class Or(YAMLConvertable):
    intents: List[Union[Intent, str]]

    def __init__(self, *args: Union["Or", Intent, Utterance, str]) -> None:
        self.intents = list(args)

    def as_yaml(self):
        pass


class Fork(YAMLConvertable):
    paths: List[List[Union["Or", Intent, Utterance, str, "Fork"]]]

    def __init__(
        self, *args: List[Union["Or", Intent, Utterance, str, "Fork"]]
    ) -> None:
        self.paths = list(args)

    def as_yaml(self):
        pass


class Story:
    paths: List[Union["Or", Intent, Utterance, str]]
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

    def persist(self, domain_filename: str, nlu_filename: str):
        story_nlu_steps: List[str] = []
        last_element: Optional[Intent] = None

        all_intents: Set[Intent] = []
        all_utterances: Set[Utterance] = []
        all_actions: Set[Action] = []
        # all_slots: Set[Slot] = []

        for element in self.paths:
            if isinstance(element, Intent):
                all_intents.append(element)

                # Add to current story
                story_nlu_steps.append({"intent": element.name})

            elif isinstance(element, Utterance):
                all_utterances.append(element)

                # Add to current story
                story_nlu_steps.append({"action": element.name})
            elif isinstance(element, str):
                # Add to current storry
                story_nlu_steps.append({"intent": element})
            elif isinstance(element, Or):
                intents_nlu: List[Dict[str, str]] = []
                # Write NLU for each intent
                for intent in element.intents:
                    if isinstance(intent, str):
                        intents_nlu.append({"intent": intent})
                    elif isinstance(intent, Intent):
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

                    # Get filename stem
                    domain_stem = os.path.splitext(
                        os.path.basename(domain_filename)
                    )[0]

                    domain_folder = os.path.dirname(
                        os.path.abspath(domain_filename)
                    )

                    nlu_stem = os.path.splitext(
                        os.path.basename(nlu_filename)
                    )[0]

                    nlu_folder = os.path.dirname(os.path.abspath(nlu_filename))

                    story.persist(
                        domain_filename=os.path.join(
                            domain_folder, f"{domain_stem}_fork_{index}.yaml"
                        ),
                        nlu_filename=os.path.join(
                            nlu_folder, f"{nlu_stem}_fork_{index}.yaml"
                        ),
                    )

            last_element = element

        # Save current story
        story_nlu = [{"story": self.name, "steps": story_nlu_steps}]

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
        domain.persist(domain_filename)

        # Write NLU
        nlu_data = {
            "version": "2.0",
            "nlu": [intent.as_yaml() for intent in all_intents],
            "stories": story_nlu,
        }

        nlu_data_yaml = dump_obj_as_yaml_to_string(
            nlu_data, should_preserve_key_order=True
        )

        RasaYAMLReader().validate(nlu_data_yaml)

        write_text_file(nlu_data_yaml, nlu_filename)


dog_story = Story(
    name="dog_story",
    elements=[
        Intent(examples="Do you have a dog?"),
        Utterance(
            text="Yes, I have a cockerspaniel. Are you a dog lover too?"
        ),
        Fork(
            [
                Or(Intent(examples="I love dogs"), "affirm"),
                Utterance(text="Great, we can be friends then."),
            ],
            [
                Or(
                    Intent(examples="I hate dogs"),
                    Intent(examples=["I love cats", "I prefer cats"]),
                    "deny",
                ),
                Utterance(
                    text="Why? Dogs are man's best friend."
                ),  # A new rule/story will split off of here
                Fork(
                    [
                        Intent(
                            examples=[
                                "I'm actually allergic",
                                "I'm allergic to dogs",
                            ]
                        ),
                        Utterance(text="There's medicine for that"),
                    ],
                    [
                        Or(
                            Intent(
                                examples=[
                                    "I just don't like them",
                                    "I've been bitten by a dog",
                                ]
                            ),
                            "fallback",
                        ),
                        Utterance(text="Aw that's a shame."),
                    ],
                ),
            ],
        ),
    ],
)

dog_story.persist(
    domain_filename="domain/dog_domain.yaml", nlu_filename="data/dog_nlu.yaml"
)
