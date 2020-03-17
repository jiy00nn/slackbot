import csv
from userinfo import UserInfo

u = UserInfo()
count = u.request_github()
u.send_dm(count['data']['user']['contributionsCollection']['totalCommitContributions'])

