import logging
from petstore import BaseClass, User
from utils.validations import validate_response
from petstore.user_service import urls

logger = logging.getLogger(__name__)


class UserService(BaseClass):
    
    def __init__(self, user: User) -> None:
        self.user = user
        self.base_url = self.user.base_url + '/pet'
        self.headers = self.user.headers
        self.urls = urls.urls
        self.log = self.user.log
