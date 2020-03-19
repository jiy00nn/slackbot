import pytz
import requests
from datetime import datetime

class GitHub():
    def __init__(self, git_token, git_user_name):
        self.git_token = git_token
        self.git_user_name = git_user_name

    def make_github_query(self):
        time = datetime.now(pytz.timezone('Asia/Seoul')).strftime("%Y-%m-%dT%H:%M:%S")

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
        """.format(self.git_user_name, time, time)

        return headers, query

    def request_github(self):
        # GitHub Request
        headers, query = self.make_github_query()
        git_response = requests.post("https://api.github.com/graphql", json={'query':query}, headers=headers)
        if git_response.status_code == 200: # Request code 200 means ok.
            return git_response.json()
        else:
            raise Exception("Query failed to run by returning code of {}. {}".format(git_response.status_code, query))