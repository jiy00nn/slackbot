import requests
import json
import random
from datetime import date

class UserInfo():
    def __init__(self):

    def make_github_query(self):
        headers = {
        "Authorization": "Bearer {}".format(self.git_token),
        "Content-Type": "application/json", 
        "Accept": "application/vnd.github.inertia-preview+json"
        }

        # Graphql query 엑세스 값
        query = """
        query{{
        user(login: "{0}") {{
            contributionsCollection(from: "{1}", to: "{2}") {{
            totalCommitContributions
            }}
        }}
        }}
        """.format(self.git_user_name, date.today().strftime("%Y-%m-%dT%H:%M:%S"), date.today().strftime("%Y-%m-%dT%H:%M:%S"))

        return headers, query

    def request_github(self):
        # GitHub Request
        headers, query = self.make_github_query()
        git_response = requests.post("https://api.github.com/graphql", json={'query':query}, headers=headers)
        if git_response.status_code == 200: # Request code 200 means ok.
            return git_response.json()
        else:
            raise Exception("Query failed to run by returning code of {}. {}".format(git_response.status_code, query))

    def request_slack(self, msg):
        # 슬랙 전송
        headers = {"Content-Type": "application/json"}
        data = f"{{'text':'{msg}', 'token':'{self.slack_token}'}}"
        data = data.encode(encoding='utf-8')
        requests.post(self.slack_hook_token, data=data, headers=headers)

    def commit_fairy(self):
        git_data =  self.request_github()
        self.request_slack(git_data['data']['user']['contributionsCollection']['totalCommitContributions'])

if __name__ == "__main__":
    u = UserInfo()
    u.commit_fairy()