from logger_config import logger
from utils import dns_resolution
from task_runner import (
    set_driver,
    element_go_to_url,
    element_delay,
    element_fill,
    element_accept_alert,
    element_look_for_pattern,
    element_click,
    finish_task,
)
from task_api import task_api


def main(puller_id):
    # Create tasks
    params = {"puller_id": puller_id}
    create_task = task_api("spCreateDueTasksForPuller", params)
    logger.info(f"create task response: {create_task}")

    created_tasks = task_api("spGetTasksQueuePuller", params)
    logger.info(f"created tasks: {created_tasks}")

    # Process Tasks
    logger.info("processing tasks")
    if created_tasks is None or len(created_tasks) == 0:
        logger.info("No tasks to process.")
        return "No tasks to process."
    else:
        for task in created_tasks:
            logger.info(f"processing task {task}")
            task_main(task=task)
    return f"task processing completed. tasks processed: {len(created_tasks)}"


def execute_task(
    driver, task_elements, task_url, task_id, task_pattern
):
    driver.maximize_window()
    driver.implicitly_wait(10)
    driver.set_page_load_timeout(30)
    element_go_to_url(url=task_url, driver=driver)
    i = 1
    for el in task_elements:
        print(f"{i} ---------------------------------------")
        i += 1

        if el["element_type_name"] == "delay":
            element_delay(driver, el["element_value"])
        elif el["element_type_name"] == "fill":
            element_fill(
                driver=driver,
                lookfor=el["element_name"],
                method=el["element_lookupmethod_name"],
                index=el["element_lookup_index"],
                value=el["element_value"],
                skipClick=el["element_skip_click"],
                skip_scroll=el["element_skip_scroll"],
                task_id=task_id,
            )
        elif el["element_type_name"] == "click_element":
            element_click(
                driver=driver,
                look_for=el["element_name"],
                method=el["element_lookupmethod_name"],
                index=el["element_lookup_index"],
                skip_scroll=el["element_skip_scroll"],
                task_id=task_id,
            )
        elif el["element_type_name"] == "look_for_pattern":
            element_look_for_pattern(
                driver=driver,
                lookfor=el["element_name"],
                method=el["element_lookupmethod_name"],
                index=el["element_lookup_index"],
                pattern=el["element_check_pattern"],
                skipScroll=el["element_skip_scroll"],
                task_id=task_id,
            )
        elif el["element_type_name"] == "goto_url":
            element_go_to_url(driver, el["element_value"])
        elif el["element_type_name"] == "accept_alert":
            element_accept_alert(driver)
        else:
            logger.error(
                f"Unknown element type {el['element_type_name']}\
                     task_id {task_id}"
            )
    logger.info("---------------------------------------")
    element_look_for_pattern(
        driver=driver,
        lookfor="",
        method="",
        index=0,
        pattern=task_pattern,
        skipScroll="",
        task_id=task_id,
    )
    finish_task(driver=None, task_id=task_id, result_id=2)


def process_task(task_info, task_elements):
    driver_list = {1, 2, 3}
    if "driver_id" in task_info:
        driver_id = task_info["driver_id"]
        if driver_id == 4:
            if "content" in task_info:
                task_pattern = task_info["task_pattern"]
                task_content = task_info["content"]
                if task_pattern in task_content:
                    logger.info(f"Pattern ({task_pattern}) found")
                    finish_task(
                        driver=None,
                        task_id=task_info["task_id"],
                        result_id=2,
                    )
                else:
                    logger.info(
                        f"({task_pattern}) Not Found in {task_content}"
                    )
                    finish_task(
                        driver=None,
                        task_id=task_info["task_id"],
                        result_id=4,
                    )
            else:
                logger.error(
                    f"'content' attribute not found in task {task_info} "
                )
                finish_task(result_id=4)
        elif driver_id in driver_list:
            driver = set_driver(driver_id)
            execute_task(
                driver=driver,
                task_elements=task_elements,
                task_url=task_info["task_url"],
                task_id=task_info["task_id"],
                task_pattern=task_info["task_pattern"],
            )
        else:
            # finish task
            finish_task(
                driver=None, task_id=task_info["task_id"], result_id=4
            )
            logger.error("driver id not supported")
    else:
        # finish task
        logger.error(f"driver id not found in task {task_info}")
        finish_task(
            driver=None, task_id=task_info["task_id"], result_id=4
        )


def task_main(task):
    task = {"task_id": 127838500}
    task_id = task["task_id"]

    try:
        logger.info(f"getting task {task}")
        task_api("spTakeTask", task)

        # TODO assume only one task is available ?
        task_info = task_api("spGetTask", task)[0]
        logger.info(f"getting task {task}")

        logger.info(f"received task info <{task_info}>")

        logger.info(f"get task elements of {task}")
        task_elements = task_api("spGetTaskElements", task)

        logger.info(
            f"received task {task} with elements {task_elements}"
        )

        if "task_url" in task_info:
            task_info = task_info
            if dns_resolution(task_info["task_url"]):
                process_task(task_info, task_elements)
            else:
                logger.error(f"finish task with id {task_id}")
                # TODO enable after done
                finish_task(driver=None, result_id=4, task_id=task_id)
        else:
            logger.error("task_url not in task {task_info}")
    except Exception as e:
        logger.error(f"Something went wrong {e}")
        # Call finish task
        finish_task(driver=None, result_id=4, task_id=task_id)
