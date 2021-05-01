from rasa.shared.nlu.state_machine.state_machine_models import (
    Intent,
    Utterance,
)

from data_generation.story_generation import Story, Fork, Or

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
                        Intent(
                            examples=[
                                "I just don't like them",
                                "I've been bitten by a dog",
                            ]
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
