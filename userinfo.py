import os
import json
import pytz
import random
import requests
from datetime import datetime

class UserInfo():
    def __init__(self, git_token, git_user_name, slack_user_name):
        self.git_token = git_token
        self.git_user_name = git_user_name
        self.slack_bot_token = os.environ['SLACK_BOT_TOKEN']
        self.slack_user_name = slack_user_name
        # Slack Bot List는 기존에 만들어둔 Slack Bot에게는 DM을 보내지 않도록 미리 제외하기 위해 사용
        self.slack_bot = []
        bots = os.environ['SLACK_BOT']
        for bot in bots.split(', '):
            self.slack_bot.append(bot)

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
    
    def make_message(self, count, user_id):
        # 커밋을 하나 이상 했을 경우의 메시지
        if count > 0:
            commitList = [
                ["https://user-images.githubusercontent.com/52561966/76221930-2e826700-625d-11ea-87b0-a72a577de6ef.jpg","여어~ 오늘도 무사히 커밋했구만~"],
                ["https://user-images.githubusercontent.com/52561966/76221945-30e4c100-625d-11ea-83ee-3ddc3c426bdd.jpg","오늘도 무사히 커밋해줘서 기쁘다~"],
                ["https://user-images.githubusercontent.com/52561966/76221927-2d513a00-625d-11ea-89d8-3a82bba13aa1.jpg","커밋한 당신! 멋져!"],
                ["https://user-images.githubusercontent.com/52561966/76221911-2a564980-625d-11ea-8a15-d77a7a75297d.jpg",f"{count}만큼 커밋했다!!! 대단해!!"],
                ["https://user-images.githubusercontent.com/52561966/76221941-30e4c100-625d-11ea-95f7-729509012fb2.jpg",f"<@{user_id}>!! 커밋했구나!!"],
                ["https://user-images.githubusercontent.com/52561966/76221924-2c200d00-625d-11ea-9156-ae2c2f5ca13e.jpg",f"<@{user_id}>야!! 커밋을 했다니!! 훌륭해!!"],
                ["https://user-images.githubusercontent.com/52561966/76221918-2b877680-625d-11ea-9e88-a9d48baa9ff3.jpg","크으~ 커밋하느라 수고했어~"]
            ]
        else:
            # 커밋 안했을 경우의 메시지
            commitList = [
                ["https://user-images.githubusercontent.com/52561966/76221923-2c200d00-625d-11ea-9a7b-62217a365e8b.jpg","내..내일은... 커밋해주세요.."],
                ["https://user-images.githubusercontent.com/52561966/76221932-2e826700-625d-11ea-9482-e55d04300096.jpg",f"<@{user_id}>... 커밋을 안해준다..."],
                ["https://user-images.githubusercontent.com/52561966/76221934-2f1afd80-625d-11ea-831a-7e29f74ba0d0.jpg","잔다고 커밋 까먹은거 아니지..?"],
                ["https://user-images.githubusercontent.com/52561966/76221936-2fb39400-625d-11ea-8775-55cc5abc6fe3.jpg",f"여보세욧!!! <@{user_id}>커밋하세욧!!"],
                ["https://user-images.githubusercontent.com/52561966/76221926-2d513a00-625d-11ea-9ca4-df6b88199a3f.jpg","싸늘하다... 커밋이 없다..."],
                ["https://user-images.githubusercontent.com/52561966/76221929-2de9d080-625d-11ea-8958-4c7407823c25.jpg","커밋도 안했고 아무것도 하기싫다..."],
                ["https://user-images.githubusercontent.com/52561966/76221918-2b877680-625d-11ea-9e88-a9d48baa9ff3.jpg",f"커밋이 {count}인게 사실이여?!?!"]
            ]

        message = random.choice(commitList)
        data = """ 
        [
            {{
                "type": "image",
                "title": {{
                    "type": "plain_text",
                    "text": "커밋요정이 왔다!",
                    "emoji": true
                }},
                "image_url": "{0}",
                "alt_text": "Commit Fairy"
            }},
            {{
                "type": "context",
                "elements": [
                    {{
                        "type": "mrkdwn",
                        "text": "{1}"
                    }}
                ]
            }}
        ]
        """.format(message[0], message[1]) 
        

        return data

    # 슬랙 user id 받기
    def get_user_id(self):
        user_id = ""

        headers = {
            "Authorization": "Bearer {}".format(self.slack_bot_token),
            "Content-Type": "application/x-www-form-urlencoded"
            }
        users_data = requests.get("https://slack.com/api/users.list", headers=headers)
        
        if users_data.status_code == 200: # Request code 200 means ok.
            datas = users_data.json()
            for data in datas["members"]:
                if data["id"] not in self.slack_bot and data["real_name"] == self.slack_user_name:
                    user_id = data["id"]
        else:
            raise Exception("Query failed to run by returning code of {}. {}".format(users_data.status_code, users_data.json()))
        
        return user_id

    # 대화 오픈 확인하기
    def slack_conversation_open(self, id):
        headers = {
            "Authorization": "Bearer {}".format(self.slack_bot_token),
            "Content-Type": "application/x-www-form-urlencoded"
            }
        data = {"users": id }

        open_status = requests.post("https://slack.com/api/conversations.open", headers=headers, data=data)
        
        if open_status.status_code == 200: # Request code 200 means ok.
            data = open_status.json()
            return data["channel"]["id"]
        else:
            raise Exception("Query failed to run by returning code of {}. {}".format(open_status.status_code, open_status.json()))

    def send_dm(self, count):
        id = self.get_user_id()
        headers = {
            "Authorization": "Bearer {}".format(self.slack_bot_token),
            "Content-Type": "application/json; charset=utf-8"
            }
        data = {
            "channel": f"{self.slack_conversation_open(id)}",
            "blocks": f"{self.make_message(count, id)}"
            }

        result = requests.post("https://slack.com/api/chat.postMessage", headers=headers, data=json.dumps(data))
        print(result.json())