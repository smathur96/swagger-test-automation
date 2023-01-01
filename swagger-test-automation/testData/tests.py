from petstore.pet_service.pets import pets
from petstore.pet_service.constants import status_sold

test_cases = [
    {
        "case": {
            "create_pet": [pets["cat"]],
            "update_pet": [pets["dog"]],
            "get_pet": [[status_sold]]
        },
        "description": "Creating a pet, updating it and then fetching the updated details.",
        "tag_list": ["pet"],
        "unique_id": "pet_flow"
    }
]