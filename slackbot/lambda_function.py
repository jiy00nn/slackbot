from main import UserInfo

u = UserInfo("6c2c51fc680e9e6ff670f51be4bc7633510990ba","jiyoonbak","박지윤")
count = u.request_github()
u.send_dm(count['data']['user']['contributionsCollection']['totalCommitContributions'])