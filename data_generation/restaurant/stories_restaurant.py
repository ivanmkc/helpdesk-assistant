from rasa.shared.nlu.state_machine.state_machine_models import (
    Intent,
    Utterance,
)

from data_generation.story_generation import Fork, Or, Story

i_like_dogs = (
    Intent(
        examples=[
            "I hate dogs",
            "I love dogs",
            "Dogs are the best, don't you think?",
        ]
    ),
)

dog_story = Story(
    name="dog_story",
    elements=[
        Or(
            i_like_dogs,
            Intent(
                examples=[
                    "Do you have a dog?",
                    "Are you a dog lover?",
                    "Do you like dogs?",
                    "What do you think about dogs?",
                    "Do you like puppies?",
                ]
            ),
        ),
        Utterance(
            text="Dogs are great. I have a cockerspaniel. Are you a dog lover too?"
        ),
        Fork(
            [
                Or(
                    i_like_dogs,
                    "affirm",
                ),
                Utterance(text="Great, we can be friends then."),
            ],
            [
                Or(
                    Intent(
                        examples=[
                            "I love cats",
                            "I prefer cats",
                            "I'm more of a cat person",
                        ]
                    ),
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
