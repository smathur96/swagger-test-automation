import logging
from petstore import BaseClass, Pet
from utils.validations import validate_response
from petstore.pet_service import urls

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class PetService(BaseClass):
    
    def __init__(self, pet: Pet) -> None:
        self.pet = pet
        self.base_url = self.pet.base_url + '/pet'
        self.headers = self.pet.headers
        self.urls = urls.urls
        self.log = self.pet.log
    
    def create_pet(self, pet: dict) -> dict:
        result = {}
        response = self.query(
            "POST", data=pet, url=self.base_url, headers=self.headers, log=self.log
        )
        if response.get("status") != 200:
            error_response = response.get("data")
            if type(error_response) is str:
                error_response = error_response.replace("\r\n", "")
            logger.error(f"{self.log.execution_id} Pet not created {error_response}.")
            result.update(
                {self.create_pet.__name__: f"Test case has Failed. Reason : {error_response}"}
            )
            return result
        if validate_response(pet, response["data"]):
            result.update(
                {self.create_pet.__name__ + "_response_validation": "Response Validated"}
            )
        else:
            result.update(
                {self.create_pet.__name__ + "_response_validation": "Response not matched"}
            )
            result.update({self.create_pet.__name__: "Response validation unsuccessful"})
            return result
        logger.info(
            f"{self.log.execution_id} Pet created successfully"
        )
        result.update({self.create_pet.__name__: "Test Case Passed"})
        return result
    
    def update_pet(self, pet: dict) -> dict:
        result = {}
        
        response = self.query(
            "PUT", url=self.base_url, data=pet, headers=self.headers, log=self.log
        )
        if response.get("status") != 200:
            logger.error(
                f"{self.log.execution_id} Pet is not updated.{response.get('data').replace('/r/n', '')}"
            )
            result.update(
                {
                    self.update_pet.__name__: f"Test case has Failed. Reason : "
                                              f"{response.get('data').replace('/r/n', '')} "
                }
            )
            return result
        if validate_response(pet, response["data"]):
            result.update(
                {self.update_pet.__name__ + "_response_validation": "Response Validated"}
            )
        else:
            result.update(
                {self.update_pet.__name__ + "_response_validation": "Response not matched"}
            )
            result.update({self.update_pet.__name__: "Test Case Failed"})
            return result
        logger.info(f"{self.log.execution_id} Pet updated")
        result.update({self.update_pet.__name__: "Test Case Passed"})
        return result
        
    def get_pet(self, status: list) -> dict:
        result = {}
        url = self.base_url + self.urls["get_pet"]
        params = dict(status=status)
        
        response = self.query(
            "GET", url=url, params=params, headers=self.headers, log=self.log
        )
        
        if response.get("status") != 200:
            logger.error(
                f"{self.log.execution_id} Unable to find pet with status {status}."
                f"{response.get('data').replace('/r/n', '')}"
            )
            result.update(
                {
                    self.get_pet.__name__: f"Test case has Failed. Reason : "
                                              f"{response.get('data').replace('/r/n', '')} "
                }
            )
            return result
        # if validate_response(pet, response["data"]):
        #     result.update(
        #         {self.update_pet.__name__ + "_response_validation": "Response Validated"}
        #     )
        # else:
        #     result.update(
        #         {self.update_pet.__name__ + "_response_validation": "Response not matched"}
        #     )
        #     result.update({self.update_pet.__name__: "Test Case Failed"})
        #     return result
        result.update({self.get_pet.__name__: "Test Case Passed"})
        return result
    