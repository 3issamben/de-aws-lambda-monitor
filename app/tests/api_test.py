import pytest
import requests_mock
from app import task_api


def test_make_request_success():
    with requests_mock.Mocker() as m:
        m.post("http://test.com", text='{"key": "value"}')
        assert task_api.make_request(
            "http://test.com", {"data": "test_data"}
        ) == {"key": "value"}


def test_make_request_fail_not_json():
    with requests_mock.Mocker() as m:
        m.post("http://test.com", text="not json")
        assert (
            task_api.make_request(
                "http://test.com", {"data": "test_data"}
            )
            is None
        )


def test_task_api_success():
    with requests_mock.Mocker() as m:
        m.post(
            "https://ems.digitaledge.net/service4/cmon/TaskController.aspx?sp=test_action",
            text='{"key": "value"}',
        )
        assert task_api.task_api(
            "test_action", {"data": "test_data"}
        ) == {"key": "value"}


def test_task_api_fail_empty_response():
    with requests_mock.Mocker() as m:
        m.post(
            "https://ems.digitaledge.net/service4/cmon/TaskController.aspx?sp=test_action",
            status_code=500,
        )
        assert (
            task_api.task_api("test_action", {"data": "test_data"})
            is None
        )
