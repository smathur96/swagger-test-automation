import logging
import requests
from urllib import parse
from utils.logger import Log

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BaseClass:
    @staticmethod
    def query(
            method: str,
            url: str,
            log: Log,
            headers: dict = None,
            data: dict = None,
            params: dict = None,
            **kwargs
    ) -> dict:
        """
        Wrapper function to send requests and handle responses.
        """
        
        logger.info(
            " execution_id: {} user_id: {} method: {} path: {}  data: {}".format(
                log.execution_id,
                log.user_id,
                method,
                url,
                str("Get request") if method == "GET" else str(data),
            )
        )
        if len(kwargs) > 0 and kwargs["open_api"] and len(kwargs["parameters"]) > 0:
            headers = None
            url = url + "?" + parse.urlencode(kwargs["parameters"])
        elif "file" in kwargs.keys():
            data.update(kwargs)
        if method == "GET":
            resp = requests.get(url, headers=headers, params=params)
            status_code = resp.status_code
            try:
                json_data = resp.json()
                response = {"data": json_data, "status": status_code}
                logger.info(response)
                return response
            except Exception as e:
                logging.exception(str(e))
                response = {"data": resp.text, "status": status_code}
                logger.info(response)
                return response
        elif method == "POST":
            resp = requests.post(url, json=data, headers=headers)
            status_code = resp.status_code
            try:
                json_data = resp.json()
                response = {"data": json_data, "status": status_code}
                logger.info(response)
                return response
            except Exception as e:
                logging.exception(str(e))
                response = {"data": resp.text, "status": status_code}
                logger.info(response)
                return response
        elif method == "DELETE":
            resp = requests.delete(url, json=data, headers=headers)
            status_code = resp.status_code
            try:
                json_data = resp.json()
                response = {"data": json_data, "status": status_code}
                logger.info(response)
                return response
            except Exception as e:
                logging.exception(str(e))
                response = {"data": resp.text, "status": status_code}
                logger.info(response)
                return response
        elif method == "PUT":
            resp = requests.put(url, json=data, headers=headers)
            status_code = resp.status_code
            try:
                json_data = resp.json()
                response = {"data": json_data, "status": status_code}
                logger.info(response)
                return response
            except Exception as e:
                logging.exception(str(e))
                response = {"data": resp.text, "status": status_code}
                logger.info(response)
                return response
        else:
            return {"data": "Method not found", "status": 404}


class Pet(BaseClass):
    
    def __init__(
            self,
            base_url,
            api_key,
            log: Log
    ) -> None:
        self.base_url = base_url
        self.api_key = api_key
        self.headers = {}
        self.log = log
        
    def login(self) -> dict:
        url = self.base_url + '/login'
        self.headers.update(dict(api_key=self.api_key))
        response = self.query("POST", log=self.log, url=url)
        return response


class User(BaseClass):
    
    def __init__(
            self,
            base_url,
            api_key,
            log: Log
    ) -> None:
        self.base_url = base_url
        self.api_key = api_key
        self.headers = {}
        self.log = log
    
    def login(self) -> dict:
        url = self.base_url + '/login'
        self.headers.update(dict(api_key=self.api_key))
        response = self.query("POST", log=self.log, url=url)
        return response
