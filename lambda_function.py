import csv
from userinfo import UserInfo

def lambda_handler(event, context):
    f = open('userinfo.csv', 'r', newline='')
    rdf = csv.reader(f)

    for line in rdf:
        u = UserInfo(line[0], line[1], line[2])
        count = u.request_github()
        u.send_dm(count['data']['user']['contributionsCollection']['totalCommitContributions'])




