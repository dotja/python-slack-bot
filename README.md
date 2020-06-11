# Python Slack Bot
A python bot that checks for new jobs and sends Slack notifications about them. It is configured to run daily using Cron.

## Dependencies
* A Linux instance (Bionic)
* Python (v. 3.6.9)
* Firefox binary (v. 77.0.1)
* Geckodriver (v. 0.24.0)
* Cron
* Python modules: Selenium (v. 3.141.0) / slack

## Workflow
1. send a request to a job site
2. parse the response with selenium
3. determine if there are any jobs posted today
4. send slack notification

## Cron setup
```
crontab -u ubuntu -e
0 17 * * * /home/ubuntu/bot.sh
```
