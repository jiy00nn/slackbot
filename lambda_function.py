from userinfo import UserInfo

def lambda_handler(event, context):
    u = UserInfo(GITHUB_TOKEN,GIT_HUB_USER_NAME,SLACK_NAME)
    count = u.request_github()
    u.send_dm(count['data']['user']['contributionsCollection']['totalCommitContributions'])
