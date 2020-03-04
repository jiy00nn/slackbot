import requests
import json
import random
from datetime import date

headers = {
    "Authorization": "",
    "Content-Type": "application/json", 
    "Accept": "application/vnd.github.inertia-preview+json"
    }

# Graphql query 엑세스 값
query = """
query{
  user(login: "jiyoonbak") {
    contributionsCollection(from: "2020-03-02T00:00:00.000+00:00", to: "2020-03-02T00:00:00.000+00:00") {
      totalCommitContributions
    }
  }
}
"""

def make_query(user_info):
    pass
    


def run_query(query):    # GitHub Request
    git_req = requests.post("https://api.github.com/graphql", json={'query':query}, headers=headers)
    return git_req.json()
    # if git_req.status_codes == 200: # Request code 200 means ok.
    #     return git_req.json()
    # else:
    #     raise Exception("Query failed to run by returning code of {}. {}".format(git_req.status_codes, query))

def send_slack(msg):
    # 슬랙 전송
    slack_url = ""
    headers = {"Content-Type": "application/json"}
    data = f"{{'text':'test', 'token':''}}"
    data = data.encode(encoding='utf-8')

    slack_req = requests.post(slack_url, data=json.dumps(data), headers=headers)
    slack_data = slack_req.json()

if __name__ == "__main__":
    git_data =  run_query(query)
    print(git_data)
    #send_slack(git_data['data']['user']['contributionsCollection']['totalCommitContributions'])