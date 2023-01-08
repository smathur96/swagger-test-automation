import logging
import uuid

from flask.logging import default_handler


class Log:
    def __init__(self, *args, execution_id=None, user_id=None, **kwargs):
        self.execution_id = None
        execution_id and self.set_execution_id(execution_id)

        self.user_id = user_id or self.get_user_id()

    def __getattr__(self, attr):
        if attr == "execution_id":
            self.set_execution_id(str(uuid.uuid4()))
            return self.get_execution_id()

    def get_user_id(self):
        try:
            if self.user_id:
                return self.user_id
            else:
                self.user_id = "AnonymousUser"
        except Exception:
            self.user_id = "AnonymousUser"
        return self.user_id

    def get_execution_id(self):
        return self.execution_id

    def set_execution_id(self, execution_id):
        self.execution_id = execution_id or self.execution_id
        return self

    def basic_log(self):
        return " execution_id: {} user_id: {} method: {} path: {} api_name:{} data: {}".format(
            self.get_execution_id(),
            self.user_id,
            self.request.method,
            self.request.path,
            self.request or self.request.url,
            str(self.request.query_params)
            if self.request.method == "GET"
            else str(self.request.data),
        )


class Logger:
    def __init__(self):
        self.logger = logging.Logger(__name__)

    def get_logger(self):
        self.logger.addHandler(default_handler)
        return self.logger
