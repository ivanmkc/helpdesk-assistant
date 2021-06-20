from data_generation.models.object_models import Concept


class Thing:
    history = Concept(
        name="history",
        synonyms=[
            "old thing",
            "antique",
            "mummy",
            "ruin",
            "sword",
            "historic",
        ],
    )

    sightseeing = Concept(
        "sightseeing",
        synonyms=[
            "sightsee",
            "tour",
            # "see the city",
            # "take photos",
            "landmark",
            "attraction",
            "tourist trap",
            "tourist spot",
        ],
    )

    natural_history = Concept(
        "natural history",
        synonyms=[
            "fossils",
            "dinosaur",
        ],
    )

    religion = Concept(
        "religion",
        synonyms=[
            "cross",
            "cruxifix",
            "altar",
            "mass",
            "god",
        ],
    )

    art = Concept(
        name="art",
        synonyms=[
            "art",
            "culture",
            "painting",
            "artwork",
            "statue",
        ],
    )

    shopping = Concept(
        name="shopping",
        synonyms=[
            "shopping",
            "shop",
            "buy clothes",
            "buy",
            "clothes",
            "souvenir",
            "postcard",
            "shopping center",
            "supermarket",
            "convenience store",
            "store",
        ],
    )

    food = Concept(
        name="food",
        synonyms=[
            "burger",
            "coke",
            "coffee",
            "food",
            "taco",
            "lunch",
            "dinner",
            "breakfast",
            "eggs",
            "sushi",
            "taco",
            "hotpot",
            "dimsum",
            "salad",
            "ice cream",
            "fries",
            "sandwich",
            "drink",
            "cold drink",
            "beer",
            "wine",
            "water",
            "orange juice",
            "eat",
        ],
    )
