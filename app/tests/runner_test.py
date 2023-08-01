import pytest
from unittest.mock import patch, Mock
from app.task_runner import (
    set_driver,
    element_go_to_url,
    element_accept_alert,
    element_delay,
    element_find,
    finish_task,
)


def test_set_driver_chrome(mocker):
    mocker.patch("webdriver_manager.chrome.ChromeDriverManager")
    mocker.patch("selenium.webdriver.chrome.service.Service")
    mocker.patch("selenium.webdriver.Chrome")
    mock_logger = mocker.patch(
        "app.task_runner.logger", autospec=True
    )

    set_driver(1)
    mock_logger.info.assert_called_with("Creating Chrome driver")


def test_set_driver_firefox(mocker):
    mocker.patch("webdriver_manager.microsoft.IEDriverManager")
    mocker.patch("selenium.webdriver.ie.service.Service")
    mocker.patch("selenium.webdriver.Ie")
    mock_logger = mocker.patch(
        "app.task_runner.logger", autospec=True
    )

    set_driver(2)
    mock_logger.info.assert_called_with(
        "Creating Internet Explorer driver"
    )


def test_set_driver_invalid(mocker):
    mock_logger = mocker.patch(
        "app.task_runner.logger", autospec=True
    )
    result = set_driver(4)
    mock_logger.error.assert_called_with("Invalid browser")
    assert result is None


def test_element_delay(mocker):
    mocker_time = mocker.patch("app.task_runner.time.sleep")
    element_delay(Mock(), 5)
    mocker_time.assert_called_with(5)


def test_element_accept_alert(mocker):
    mock_driver = Mock()
    mock_alert = Mock()
    mock_driver.switch_to.alert = mock_alert
    element_accept_alert(mock_driver)
    mock_alert.accept.assert_called_once()


@patch("app.task_runner.element_find_internal", return_value=Mock())
@patch("app.task_runner.time.sleep")  # Mock sleep to avoid delay
def test_element_find_found(mock_sleep, mock_element_find_internal):
    mock_driver = Mock()
    result = element_find(
        mock_driver, "lookfor", "method", 0, False, "task_id"
    )
    assert result is not None
    mock_element_find_internal.assert_called_once()


@patch("app.task_runner.element_find_internal", return_value=None)
@patch("app.task_runner.time.sleep")
@patch("app.task_runner.finish_task")
def test_element_find_not_found(
    mock_finish_task, mock_sleep, mock_element_find_internal
):
    mock_driver = Mock()
    # with pytest.raises(
    #     SystemExit
    # ):  # finish_task should call sys.exit()
    result = element_find(
        mock_driver, "lookfor", "method", 0, False, "task_id"
    )
    assert result is None
    assert (
        mock_element_find_internal.call_count == 3
    )  # Tried to find the element 3 times
    mock_finish_task.assert_called_once()


@patch("app.task_runner.logger.info")
def test_element_go_to_url(mock_info):
    mock_driver = Mock()
    element_go_to_url(mock_driver, "https://www.example.com")
    mock_info.assert_called_once_with(
        "Navigating to https://www.example.com"
    )
    mock_driver.get.assert_called_once_with("https://www.example.com")


@patch("app.task_runner.task_api")
@patch("app.task_runner.calculate_execution_time")
@patch("app.task_runner.log_stream.getvalue")
@patch("app.task_runner.take_screenshot")
@patch("app.task_runner.logger")
def test_finish_task(
    mock_logger,
    mock_screenshot,
    mock_getvalue,
    mock_calculate_execution_time,
    mock_task_api,
):
    mock_driver = Mock()
    task_id = "123"
    result_id = 4
    mock_getvalue.return_value = "logs"
    mock_calculate_execution_time.return_value = 2.0
    finish_task(mock_driver, task_id, result_id)

    assert mock_logger.info.call_count == 3
    assert mock_screenshot.called_once_with(
        driver=mock_driver, task_id=task_id
    )
    assert mock_getvalue.called_once()
    assert mock_calculate_execution_time.called_once_with("logs")
    mock_task_api.assert_called_once_with(
        "spFinishTask",
        {
            "task_id": task_id,
            "task_result_id": result_id,
            "task_exec_time": 2.0,
            "task_dump": "logs",
        },
    )
