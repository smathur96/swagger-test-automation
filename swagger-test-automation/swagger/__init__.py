from utils.logger import Logger
from utils.result_formatter import get_final_verdict
from logging.config import dictConfig
import uuid

from flask import Flask, Response, json, jsonify, make_response, request, render_template

from testData import tests
from tests import e2e

logger = Logger().get_logger()


def create_app(test_config=None) -> Flask:
    app = Flask(__name__, instance_relative_config=True)
    app.debug = True

    @app.route("/swagger/status/<string:id>", methods=["GET"])
    def giving_status(identity) -> Response:
        """
        Function to return status of the test-case
        param id: uuid
        """
        data = identity
        try:
            if data.get("status") == "running":
                return make_response(jsonify(data.get("data")), 400)
            return make_response(jsonify(data), 200)
        except AttributeError as e:
            return make_response(jsonify(str(e)), 503)

    @app.route("/swagger/run_tests", methods=["POST"])
    def run_tests() -> Response:
        """
        function to run test cases
        :return:
        """
        params = request.data
        params = json.loads(params)
        tags_list = params.get("tags_list")
        unique_id = str(uuid.uuid4())
        
        validate_testcases(tests.test_cases)

        response = make_response(
            jsonify({"id": unique_id, "info": f"You can check logs for any issues."}),
            200,
        )

        @response.call_on_close
        def background_task() -> None:
            """
            :return:
            """
            with app.app_context():
                test_report = response_call_on_close(
                    params, unique_id, tags_list
                )
                result = get_final_verdict(test_report)
                print(result)
        return response
    return app


def validate_testcases(test_cases: list) -> None:
    """
    Function to validate test cases. will fail if any one of the condition fails
    :param test_cases: list of test cases
    :return:
    """
    for test_case in test_cases:
        assert (
            test_case.get("unique_id") is not None
        ), "Please provide a unique id for the testcase"
        assert (
            test_case.get("description") is not None
        ), "Please provide description for the testcase"
        assert test_case.get("tag_list") is not None, "Please provide a tag for the testcase"
        assert test_case.get("case") is not None, "Please provide a cases list for the testcase"
        assert len(test_case.get("case")) > 0, "Please provide at least 1 test case to run"


def response_call_on_close(
    payload: dict, unique_id: str, tags: list
) -> str:
    """
    It will be called when swagger/run_tests will be completed
    :param payload: The Swagger payload
    :param unique_id: unique_id generated for API call
    :param tags: tag name in list format
    :return: tuple which has test_report and time_taken
    """
    test_cases_with_tag = []
    for tag_param in tags:
        test_case_data = tests.test_cases
        for case in test_case_data:
            tag_list = case.get("tag_list")
            for tag_index in range(len(tag_list)):
                if tag_list[tag_index] == tag_param:
                    test_cases_with_tag.append(case)
    test_report = e2e.test_e2e(
        payload,
        test_cases_with_tag,
        unique_id,
    )

    data = {"id": unique_id} if unique_id is not None else {}
    data["status"] = "completed"
    data["data"] = test_report
    return test_report
