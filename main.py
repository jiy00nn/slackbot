from botocore.vendored import requests
import json
import random
from datetime import date

# 깃헙 graphql
git_url = "https://api.github.com/graphql"
headers = {
    "Content-Type": "application/json", 
    "Accept": "application/vnd.github.inertia-preview+json",
    "Authorization": "af4e68fdefc8ed75643ff3604bde4f1de54c77ce"
    }

# 오늘 날짜
t_day = date.today()
years = str(t_day.year)
months = str(t_day.month)

if len(months) == 1:
    months = "0" + months
days = str(t_day.day)
if len(days) == 1:
    days = "0" + days

# Graphql query 엑세스 값
data = {
    "query":""
}

# GitHub Request
git_req = requests.post(git_url, data=json.dumps(data), headers=headers)
# Get GitHub Data
git_data = git_req.json()

print(git_data)