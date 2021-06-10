from data_generation.models import Place, Concept

# class Activities:
#     antiques = Concept(
#         name="antiques",
#         synonyms=["old things", "history", "mummy", "ruins", "sword"],
#     )


class Thing:
    antiques = Concept(
        name="antiques",
        synonyms=["old things", "history", "mummy", "ruins", "sword"],
    )

    sightseeing = Concept(
        "sightseeing",
        synonyms=[
            "sightsee",
            "sightseeing",
            "see the city",
            "tour",
            "take photos",
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
            "church",
            "abbey",
            "altar",
            "cathedral",
            "monastery",
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
            "souvenirs",
            "postcard",
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
        ],
    )
