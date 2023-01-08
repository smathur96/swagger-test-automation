import json
from unittest import mock

import pytest
from flask import Flask

from swagger import create_app, response_call_on_close, validate_testcases
from utils.result_formatter import get_final_verdict
from tests import e2e


@pytest.fixture
def api_payload():
    return {
        "swagger": {
            "api_key": "special-key",
            "url": "https://petstore.swagger.io/v2"
        }
    }


@pytest.mark.unit_test
def test_create_app():
    response = create_app()
    assert isinstance(response, Flask)


@pytest.mark.unit_test
def test_validate_testcases():
    testcases = [{"unique_id": 1, "description": "xyz", "tag_list": ["xyz"], "case": ["case1"]}]
    validate_testcases(testcases)


@pytest.mark.unit_test
def test_run_tests(api_payload):
    app = create_app()
    params = api_payload
    with app.test_client() as c:
        response = c.post(path="/swagger/run_tests", data=json.dumps(params))
        print(response)
        assert response.status_code == 200


@pytest.mark.unit_test
def test_get_final_verdict():
    test_report = "test           test1           test2\ntest           test2"
    res = get_final_verdict(
        test_report=test_report,
    )
    assert res

    test_report = "test           test1           Passed"
    res = get_final_verdict(
        test_report=test_report,
    )
    assert res
    test_report = "test           test1           Passed\ntest           Passed"
    res = get_final_verdict(
        test_report=test_report,
    )
    assert res


@pytest.mark.unit_test
def test_response_call_on_close(api_payload):
    e2e.test_e2e = mock.Mock(return_value="result")
    payload = api_payload
    report = response_call_on_close(
        payload, "unique_id", ["vt"]
    )
    assert report
