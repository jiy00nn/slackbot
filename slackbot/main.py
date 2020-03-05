import requests
import json
import random
from datetime import date




def make_query(user_info):
    headers = {
    "Authorization": "Bearer ",
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

def run_query(query):
    # GitHub Request
    git_response = requests.post("https://api.github.com/graphql", json={'query':query}, headers=headers)
    if git_response.status_code == 200: # Request code 200 means ok.
        return git_response.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(git_response.status_code, query))

def send_slack(msg):
    # 슬랙 전송
    slack_url = ""
    headers = {"Content-Type": "application/json"}
    data = f"{{'text':'{msg}', 'token':''}}"
    data = data.encode(encoding='utf-8')

    requests.post(slack_url, data=data, headers=headers)

if __name__ == "__main__":
    git_data =  run_query(query)
    print(git_data['data']['user']['contributionsCollection']['totalCommitContributions'])
    send_slack(git_data['data']['user']['contributionsCollection']['totalCommitContributions'])