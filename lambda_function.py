import csv
import time
from slack_dm import SlackDM

def lambda_handler(event, context):
    context.callbackWaitsForEmptyEventLoop = False
    f = open('userinfo.csv', 'r', newline='')
    rdf = csv.reader(f)
 
    for line in rdf:
        u = SlackDM(line[0], line[1], line[2])
        count = u.request_github()
        u.send_dm(count['data']['user']['contributionsCollection']['contributionCalendar']['totalContributions'])