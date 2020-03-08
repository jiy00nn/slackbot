import requests
import json
import random
from datetime import date

class UserInfo():
    def __init__(self, git_token, git_user_name, slack_user_name):
        self.git_token = git_token
        self.git_user_name = git_user_name
        self.slack_bot_toekn = 
        self.slack_user_name = slack_user_name

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
    
    def make_message(self, count):
        # 커밋을 하나 이상 했을 경우의 메시지
        commitList = [
            "커밋은 하고 가야지?",
            "커밋 안하냐?",
            "커밋 좀 하지 그래?",
            "커밋 요정이 부릅니다. 커밋 하나무라",
            "커밋 좀 하고 자야지?",
            "이봐 커밋은?",
            "크아ㅏㅏㅏㅏㅏㅏㅏ 커밋해라ㅏㅏㅏㅏ"
        ]

        # 커밋 안했을 경우의 메시지
        commitList = [
            "커밋은 하고 가야지?",
            "커밋 안하냐?",
            "커밋 좀 하지 그래?",
            "커밋 요정이 부릅니다. 커밋 하나무라",
            "커밋 좀 하고 자야지?",
            "이봐 커밋은?",
            "크아ㅏㅏㅏㅏㅏㅏㅏ 커밋해라ㅏㅏㅏㅏ"
        ]

        if count > 0:
            data = f"{{'text':'오늘도 커밋을 {count}개나 했구나! 닝갠아 훗'}}"
        else:
            data = f"{{'text':'{random.choice(commitList)}'}}"

        return data.encode('utf-8')

    # 슬랙 user id 받기
    def get_user_id(self):
        user_id = ""

        slack_bot = []

        headers = {
            "Authorization": "Bearer {}".format(self.slack_bot_toekn),
            "Content-Type": "application/x-www-form-urlencoded"
            }
        users_data = requests.get("https://slack.com/api/users.list", headers=headers)
        
        if users_data.status_code == 200: # Request code 200 means ok.
            datas = users_data.json()
            for data in datas["members"]:
                if data["id"] not in slack_bot and data["real_name"] == self.slack_user_name:
                    user_id = data["id"]
        else:
            raise Exception("Query failed to run by returning code of {}. {}".format(users_data.status_code, users_data.json()))
        
        return user_id

    # 대화 오픈 확인하기
    def slack_conversation_open(self, id):
        headers = {
            "Authorization": "Bearer {}".format(self.slack_bot_toekn),
            "Content-Type": "application/x-www-form-urlencoded"
            }
        data = {"users": id }

        open_status = requests.post("https://slack.com/api/conversations.open", headers=headers, data=data)
        
        if open_status.status_code == 200: # Request code 200 means ok.
            data = open_status.json()
            return data["channel"]["id"]
        else:
            raise Exception("Query failed to run by returning code of {}. {}".format(open_status.status_code, open_status.json()))

    def send_dm(self, msg):
        headers = {
            "Authorization": "Bearer {}".format(self.slack_bot_toekn),
            "Content-Type": "application/json; charset=utf-8"
            }
        data = {
            "channel": f"{self.slack_conversation_open(self.get_user_id())}",
            "text": f"{msg}"
        }
        
        requests.post("https://slack.com/api/chat.postMessage", headers=headers, data=json.dumps(data))

if __name__ == "__main__":
    u = UserInfo()
    u.send_dm("Code test")