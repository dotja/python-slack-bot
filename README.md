# Software Development jobs bot
A python bot that provides software development job notifications. The bot is configured to run daily at 5pm.

## Dependencies
* Firefox binary
* Geckodriver
* Cron
* Python modules: Selenium / email / smtplib
* A linux instance (Bionic) with Python3 installed

## Workflow
1. send a request to a job site
2. parse the response with selenium
3. determine if there are any jobs posted today
4. send email to user of new jobs

## Cron setup
```
0 17 * * * python3 /home/ubuntu/jobs_bot.py
```
