from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import re
from datetime import date
import smtplib
from email.message import EmailMessage

## configure options for the browser driver
options = Options()
options.headless = True
driver = webdriver.Firefox(options=options)

## an example job site
amz = 'https://www.amazon.jobs/en/locations/london?category=software-development'
target_btn = 'Sort by: Most relevant'

## send GET request
driver.get(amz)
#driver.page_source


## find "Sort by: Most relevant" button => then find "Most recent" anchor tag => then click it
## get all anchor tags
anchors = driver.find_elements_by_xpath("//a[@href]")

## get the element that has this text
sort_btns = driver.find_elements_by_xpath("//*[contains(text(), target_btn)]")
for btn in sort_btns:
	if btn.text == target_btn:
		btn.click()
		break


## get the button with this text
for anch in anchors:
	if anch.text == 'Most recent':
		anch.click()


## create 2 lists of job links and job posting date
date_list = []
jobs_list = []

# get the h2 header with this class
posting_dates = driver.find_elements_by_xpath("//h2[@class='posting-date']")
for elem in posting_dates:
    date_list.append(elem.text)

## find the job links using the job ID link pattern
job_anchors = driver.find_elements_by_xpath("//a[@href]")
for job in job_anchors:
	job_link = job.get_attribute("href")
	if re.search('https://www.amazon.jobs/en/jobs/\d+', job_link):
		jobs_list.append(job_link)


## get the jobs that were posted today
new_jobs = []
today = date.today()
target_date = today.strftime("%B %d, %Y")
for indx,item in enumerate(date_list):
    if re.search(target_date, item):
            new_jobs.append(jobs_list[indx])


## close all browser windows gracefully
driver.quit()

## the email function
def send_email(**kwargs):
	msg = EmailMessage()
	msg.set_content(kwargs['email_msg'])
	msg['Subject'] = kwargs['Subject']
	msg['From'] = kwargs['From']
	msg['To'] = kwargs['To']
	s = smtplib.SMTP('localhost')
	s.send_message(msg)
	s.quit()
	return

## send user notification
if new_jobs:
	email_msg = 'New jobs:\n{0}'.format('\n'.join(new_jobs))
	email = {
	'Subject': 'New Jobs',
	'From': 'you@localhost',
	'To': 'emai@gmail.com',
	'email_msg': email_msg
	}
	send_email(**email)

