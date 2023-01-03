from petstore.pet_service.constants import status_sold
from petstore.pet_service.pets import pets
from petstore.user_service.users import users

test_cases = [
    {
        "case": {
            "create_pet": [pets["cat"]],
            "update_pet": [pets["dog"]],
            "get_pet": [[status_sold]],
        },
        "description": "Creating a pet, updating it and then fetching the updated details.",
        "tag_list": ["pet"],
        "unique_id": "pet_flow",
    },
    {
        "case": {
            "create_user": [[users["matthew"]]],
            "update_user": [{"payload": users["albert"], "username": "matthew"}],
            "get_user": [{"name": "albert"}],
        },
        "description": "Creating an user, updating it and then fetching the updated details.",
        "tag_list": ["user"],
        "unique_id": "user_flow",
    },
]
