from selenium import webdriver
from selenium.webdriver.common.by import By
import os
from task_api import task_api
from logger_config import logger
from logger_config import log_stream
import time
from utils import calculate_execution_time
from selenium.webdriver.firefox.service import (
    Service as FirefoxService,
)
from selenium.webdriver.chrome.service import Service as ChromeService
from tempfile import mkdtemp
from selenium.webdriver.firefox.options import (
    Options as FirefoxOptions,
)


def finish_task(driver, task_id, result_id):
    logger.info(f"Finishing task {task_id}. Result {result_id}")

    if driver and result_id == 4:
        try:
            take_screenshot(driver=driver, task_id=task_id)
        except Exception as e:
            logger.error(f"cannot take screenshot {e}")
    # TODO call function that appends logs(update logging to output to a
    #  file then use the generated logging file)

    log_contents = log_stream.getvalue()
    execution_time = calculate_execution_time(log_contents)
    logger.info(f"execution time {execution_time}")
    params = {
        "task_id": task_id,
        "task_result_id": result_id,
        "task_exec_time": execution_time,
        "task_dump": log_contents,
    }

    logger.info("calling spFinishTask")
    task_api("spFinishTask", params)


def take_screenshot(driver, task_id):
    try:
        # Scroll up
        driver.execute_script("window.scrollTo(0,0);")
        # Take screenshot
        # TODO update point id

        # Take screenshot
        # filename = f"{scriptPath}/screenshots\
        # /point_{point_id}_task_{taskID}.png"
        # driver.save_screenshot(filename)
        file_name = f"task_{task_id}.png"
        driver.get_screenshot_as_file(
            f"{os.path.dirname(os.path.abspath('.'))}/screenshots/{file_name}"
        )
    except Exception as e:
        logger.error(f"Can't generate screenshot. {str(e)}")
    finally:
        # It's a good practice to close the browser at the end
        driver.close()


def element_delay(driver, seconds):
    # Function to sleep the script for a certain period
    time.sleep(seconds)


def element_find(
    driver, lookfor, method, index, skip_scroll, task_id
):
    for i in range(3):
        logger.info(f"Finding element {lookfor}. Try {i}")

        try:
            result = element_find_internal(
                driver=driver,
                lookfor=lookfor,
                method=method,
                index=index,
                skip_scroll=skip_scroll,
                task_id=task_id,
            )
            if result is None:
                time.sleep(5)
                continue
            return result
        except Exception as e:
            logger.error(f"Can't find element '{lookfor}'. {e}")
            time.sleep(5)

    logger.info(f"Element '{lookfor}' not found. Exiting.")
    finish_task(driver=driver, result_id=4, task_id=task_id)


def element_find_internal(
    driver, lookfor, method, index, skip_scroll, task_id
):
    logger.info(f"Looking for {lookfor} by {method} [{index}]")

    element = None

    if index > 0:
        if method == "class name":
            element = driver.find_elements(By.CLASS_NAME, lookfor)[
                index
            ]
        elif method == "name":
            element = driver.find_elements(By.NAME, lookfor)[index]
        elif method == "link text":
            element = driver.find_elements(By.LINK_TEXT, lookfor)[
                index
            ]
        elif method == "partial link text":
            element = driver.find_elements(
                By.PARTIAL_LINK_TEXT, lookfor
            )[index]
        elif method == "xpath":
            element = driver.find_elements(By.XPATH, lookfor)[index]
        else:
            element = driver.find_elements(By.ID, lookfor)[index]
    else:
        if method == "class name":
            element = driver.find_element(By.CLASS_NAME, lookfor)
        elif method == "name":
            element = driver.find_element(By.NAME, lookfor)
        elif method == "link text":
            element = driver.find_element(By.LINK_TEXT, lookfor)
        elif method == "partial link text":
            element = driver.find_element(
                By.PARTIAL_LINK_TEXT, lookfor
            )
        elif method == "xpath":
            element = driver.find_element(By.XPATH, lookfor)
        else:
            element = driver.find_element(By.ID, lookfor)

    if element is not None:
        if skip_scroll == 0:
            driver.execute_script(
                "arguments[0].scrollIntoView(true);", element
            )
        else:
            logger.info("skipping scrolling..")
        return element
    else:
        logger.info(f"!!!!!!!!!! {lookfor} not found !!!!!!!!!!!! ")
        finish_task(driver=driver, result_id=4, task_id=task_id)
        # exit if needed


def element_fill(
    driver,
    lookfor,
    method,
    index,
    value,
    skipClick,
    skip_scroll,
    task_id,
):
    logger.info(
        f"Filling {lookfor} by {method} [{index}] up with '{value}'"
    )

    element = element_find(
        driver=driver,
        lookfor=lookfor,
        method=method,
        index=index,
        skip_scroll=skip_scroll,
        task_id=task_id,
    )

    if not skipClick:
        logger.info(f"clicking on element {element}")
        element.click()

    logger.info(f"sending keys {value}")
    element.send_keys(value)


def element_click(
    driver, look_for, method, index, skip_scroll, task_id
):
    logger.info(f"Clicking {look_for} by {method} [{index}]")

    element = element_find(
        driver=driver,
        lookfor=look_for,
        method=method,
        index=index,
        skip_scroll=skip_scroll,
        task_id=task_id,
    )
    element.click()


def element_look_for_pattern(
    driver, lookfor, method, index, pattern, skipScroll, task_id
):
    logger.info(
        f"Checking pattern {pattern} inside {lookfor} by {method} [{index}]"
    )

    result_text = ""

    if lookfor == "" or lookfor == "body":
        logger.info("Checking body tag")
        result_text = driver.find_element(By.TAG_NAME, "body").text
    else:
        element = None
        element = element_find(
            driver, lookfor, method, index, skipScroll, task_id
        )
        result_text = element.text

    if pattern in result_text:
        logger.info("+++++++++++ Text found +++++++++++++++++")
    else:
        logger.info(
            "!!!!!!!!!  Text Not Found, let's end this !!!!!!"
        )
        finish_task(driver=driver, result_id=4, task_id=task_id)

        # sys.exit()


def set_driver(driver_id):
    # TOD add try catch statement ?
    logger.info(f"setting driver {driver_id}")
    driver = None
    if driver_id == 1:
        logger.info("Creating Chrome driver")
        options = webdriver.ChromeOptions()
        options.binary_location = "/opt/chrome/chrome"
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1280x1696")
        options.add_argument("--single-process")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-dev-tools")
        options.add_argument("--no-zygote")
        options.add_argument(f"--user-data-dir={mkdtemp()}")
        options.add_argument(f"--data-path={mkdtemp()}")
        options.add_argument(f"--disk-cache-dir={mkdtemp()}")
        options.add_argument("--remote-debugging-port=9222")
        driver = webdriver.Chrome(
            service=ChromeService(
                executable_path="/opt/chromedriver"
            ),
            options=options,
        )
    elif driver_id == 2:
        logger.info("Creating Internet Explorer driver")
        # TODO figure out how to handle IE
        # since docker does not support IE
        # Maybe finish task

    elif driver_id == 3:
        logger.info("Creating Firefox driver")
        options = FirefoxOptions()
        options.binary_location = "/opt/firefox/firefox"
        options.add_argument("--headless")

        driver = webdriver.Firefox(
            service=FirefoxService(
                executable_path="/opt/geckodriver"
            ),
            options=options,
        )
    else:
        logger.error("Invalid browser")

    return driver


def element_go_to_url(driver, url):
    logger.info(f"Navigating to {url} using driver {driver}")
    driver.get(url)


def element_accept_alert(driver):
    driver.switch_to.alert.accept()
