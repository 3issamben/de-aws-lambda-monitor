import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

def lambda_handler(event, context):

    # setup headless because lambda is serverless
    options = Options()
    options.binary_location = "/opt/python/bin/headless-chromium"
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--single-process')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome("/opt/python/bin/chromedriver", chrome_options=options)

    url = "https://www.google.com"
    driver.get(url)

    page_title = driver.title

    driver.close()
    driver.quit()

    response = {
        "statusCode": 200,
        "body": json.dumps({
            "message": page_title,
        }),
    }

    return response