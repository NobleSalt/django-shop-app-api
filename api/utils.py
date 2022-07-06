from api.models import *


def generate_category():
    cat_sub_cat = [
        {"name": "fish & meat", "sub_cat": ["fish", "meat"], "img": "Fish"},
        {
            "name": "fruits & vegetable",
            "sub_cat": ["dry fruits", "fresh fruits", "fresh vegetable"],
            "img": "Fruit",
        },
        {
            "name": "breakfast",
            "sub_cat": ["bread", "cereal", "drinks"],
            "img": "Breakfast",
        },
        {
            "name": "milk & dairy",
            "sub_cat": ["dairy", "ice cream", "butter & ghee"],
            "img": "MilkDiary",
        },
        {
            "name": "organic food",
            "sub_cat": [
                "organic food",
            ],
            "img": "OrganicFood",
        },
        {
            "name": "honey",
            "sub_cat": [
                "honey",
            ],
            "img": "Honey",
        },
        {
            "name": "sauses & pickles",
            "sub_cat": [
                "sauses",
                "pickles & condiments",
            ],
            "img": "Pickle",
        },
        {
            "name": "jam & jelly",
            "sub_cat": [
                "jam",
                "jelly",
            ],
            "img": "JamJelly",
        },
        {
            "name": "snacks & instant",
            "sub_cat": ["chocolate", "chips & nuts", "canned food"],
            "img": "SnacksInstant",
        },
        {
            "name": "biscuits & cakes",
            "sub_cat": ["biscuits", "cakes"],
            "img": "BiscuitsCakes",
        },
        {
            "name": "household tools",
            "sub_cat": ["cleaner", "laundry", "air freshener"],
            "img": "HouseHold",
        },
        {
            "name": "baby care",
            "sub_cat": [
                "baby food",
                "baby accessories",
            ],
            "img": "BabyCare",
        },
        {
            "name": "fresh seafood",
            "sub_cat": [
                "fresh seafood",
            ],
            "img": "FreshSeaFood",
        },
        {
            "name": "cooking essentials",
            "sub_cat": ["oil", "rice", "flour"],
            "img": "CookingEssentials",
        },
        {"name": "drinks", "sub_cat": ["tea", "water", "juice"], "img": "Drinks"},
        {
            "name": "pet & care",
            "sub_cat": ["dry fruits", "fresh fruits", "fresh vegetable"],
            "img": "PetCare",
        },
        {
            "name": "beauty & health",
            "sub_cat": ["bath", "cosmetics", "oral care"],
            "img": "BeautyHealth",
        },
        {
            "name": "sports & fitness",
            "sub_cat": [
                "sports",
                "fitness",
            ],
            "img": "SportsFitness",
        },
    ]

    for cat in cat_sub_cat:
        cat_name = cat["name"]
        sub_cats = cat["sub_cat"]
        instance, created = Category.objects.get_or_create(name=cat_name)
        if created:
            for sub in sub_cats:
                SubCategory.objects.get_or_create(category=instance, name=sub)

generate_category()