import os
import re
import logging
from datetime import date
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from slack import WebClient
from slack.errors import SlackApiError

## firefox options: interface usage not required
options = Options()
options.headless = True
driver = webdriver.Firefox(options=options)

## the job website URL
amz = 'https://www.amazon.jobs/en/locations/london?category=software-development'
target_btn = 'Sort by: Most relevant'

## send the GET request
driver.get(amz)
#driver.page_source

## look for all anchors
anchors = driver.find_elements_by_xpath("//a[@href]")

## look for the target button and click it
sort_btns = driver.find_elements_by_xpath("//*[contains(text(), target_btn)]")
for btn in sort_btns:
    if btn.text == target_btn:
        btn.click()
        break


for anch in anchors:
    if anch.text == 'Most recent':
        anch.click()


## we will store job URLs and their dates
date_list = []
jobs_list = []

## collect all the dates when the jobs were posted
posting_dates = driver.find_elements_by_xpath("//h2[@class='posting-date']")
for elem in posting_dates:
    date_list.append(elem.text)


## collect the job URLs
job_anchors = driver.find_elements_by_xpath("//a[@href]")
for job in job_anchors:
    job_link = job.get_attribute("href")
    if re.search('https://www.amazon.jobs/en/jobs/\d+', job_link):
        jobs_list.append(job_link)


## determine if there are any jobs posted today
new_jobs = []
today = date.today()
target_date = today.strftime("%B %d, %Y")
for indx,item in enumerate(date_list):
    if re.search(target_date, item):
        new_jobs.append(jobs_list[indx])


## gracefully close firefox
driver.quit()

## use env variables for Slack credentials
token = os.environ['SLACK_API_TOKEN']
channel_id = os.environ['SLACK_CHANNEL_ID']
## log file that catches errors
log_file = os.environ['BOT_LOG_FILE']

client = WebClient(token=token)
logging.basicConfig(filename=log_file, filemode='a', format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

## send a Slack notification about new jobs or catch error using the log file
if new_jobs:
    job_links = '\n'.join(new_jobs)
    try:
        response = client.chat_postMessage(channel=channel_id, text=job_links)
    except SlackApiError as e:
        logging.error(response["error"])


