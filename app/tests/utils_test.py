import pytest
from app.utils import (
    _get_base_url,
    dns_resolution,
    is_json,
    calculate_execution_time,
)


def test_get_base_url():
    assert (
        _get_base_url(
            " https://ems.digitaledge.net/service4/cmon/TaskController.aspx"
        )
        == "ems.digitaledge.net"
    )
    assert (
        _get_base_url("https://www.digitaledge.net/")
        == "www.digitaledge.net"
    )

    with pytest.raises(ValueError):
        _get_base_url(None)


def test_dns_resolution():
    assert dns_resolution("https://ems.digitaledge.net") is True
    assert dns_resolution("http://test1214314141.com") is False


def test_is_json():
    assert is_json('{"key": "value"}') is True
    assert is_json('{"key": "value",}') is False  # trailing comma
    assert is_json("not json") is False


def test_calculate_execution_time():
    logs = "2023-07-25 13:30:00,000 - INFO - Start\n2023-07-25 13:30:01,500 - INFO - End"
    assert calculate_execution_time(logs) == 1.5
