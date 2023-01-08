from petstore import BaseClass, User
from petstore.user_service import urls
from utils.logger import Logger
from utils.validations import validate_response

logger = Logger().get_logger()


class UserService(BaseClass):
    def __init__(self, user: User) -> None:
        self.user = user
        self.base_url = self.user.base_url + "/user"
        self.headers = self.user.headers
        self.urls = urls.urls
        self.log = self.user.log

    def create_user(self, user: list) -> dict:
        result = {}
        url = self.base_url + self.urls["create_user"]
        response = self.query(
            "POST", data=user, url=url, headers=self.headers, log=self.log
        )
        if response.get("status") != 200:
            error_response = response.get("data")
            if type(error_response) is str:
                error_response = error_response.replace("\r\n", "")
            logger.error(f"{self.log.execution_id} User not created {error_response}.")
            result.update(
                {
                    self.create_user.__name__: f"Test case has Failed. Reason : {error_response}"
                }
            )
            return result
        logger.info(f"{self.log.execution_id} User created successfully")
        result.update({self.create_user.__name__: "Test Case Passed"})
        return result

    def update_user(self, user: dict) -> dict:
        result = {}
        url = self.base_url + self.urls["get_or_update_user"].format(
            username=user["username"]
        )
        response = self.query(
            "PUT", url=url, data=user["payload"], headers=self.headers, log=self.log
        )
        if response.get("status") != 200:
            logger.error(
                f"{self.log.execution_id} User is not updated.{response.get('data').replace('/r/n', '')}"
            )
            result.update(
                {
                    self.update_user.__name__: f"Test case has Failed. Reason : "
                    f"{response.get('data').replace('/r/n', '')} "
                }
            )
            return result
        logger.info(f"{self.log.execution_id} User updated successfully")
        result.update({self.update_user.__name__: "Test Case Passed"})
        return result

    def get_user(self, user: dict) -> dict:
        result = {}
        url = self.base_url + self.urls["get_or_update_user"].format(
            username=user["name"]
        )

        response = self.query("GET", url=url, headers=self.headers, log=self.log)

        if response.get("status") != 200:
            logger.error(
                f"{self.log.execution_id} Unable to find user with username {user['name']}."
                f"{response.get('data').replace('/r/n', '')}"
            )
            result.update(
                {
                    self.get_user.__name__: f"Test case has Failed. Reason : "
                    f"{response.get('data').replace('/r/n', '')} "
                }
            )
            return result
        result.update({self.get_user.__name__: "Test Case Passed"})
        return result
