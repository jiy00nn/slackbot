# Commit Fairy Slack Bot

매일 Github 계정의 커밋 여부를 확인해주는 Slack 봇입니다.
개인의 Github Commit 상태를 매일 조회하거나 모임에서 여러명의 Commit 상태를 확인할 때 사용하기 좋습니다.
> 이 서비스는 AWS Lambda에 최적화 되어있습니다.  
> Python 3.7을 사용했습니다.

## 1. Requirement

### **[ Github token ]**
Github의 Commit 정보를 가져오기 위해서 아래의 항목을 체크한 뒤 Token을 발행합니다.
1. [Github Setting 메뉴] Developer settings > Personal access tokens  
- [ ] repo  
    - [X] repo:status  
- [ ] user  
    - [X] read:user  

### **[ Slack token ]**
1. 새로운 Slack Bot을 생성합니다.
2. Slack Bot 설정의 Features > OAuth & Permissions를 통해 토큰을 발행합니다.
    - 추가해야할 Bot Token Scopes 목록  
    - [channels:manage, chat:write, users:read]

### **[ AWS Lambda ]**
1. 코드를 동작시키기 위한 모듈들을 AWS의 Lamda 함수의 Layers에 추가해야 합니다. 아래의 명령어를 입력하여 python 패키지를 만들고 이를 zip 파일로 압축하여 Layers에 추가합니다.
    ```
    pip install -r requirements.txt -t python
    ```

    > zip 파일의 구조는 다음과 같아야 합니다.  
    > slackbot.zip  
    >   +---python  
    >   |   +---package_name  
    >   |   +---package_name.dist-info

2. AWS Lambda 함수의 환경 변수 2가지를 추가합니다.
    |키|값|
    |------|---|
    |SLACK_BOT|봇1, 봇2, 봇3|
    |SLACK_BOT_TOKEN|슬랙봇 토큰 입력|

    - `SLACK_BOT`은 [slack_user_list]("https://slack.com/api/users.list") API를 통해 Bot 정보들을 확인할 수 있습니다.
    - `SLACK_BOT_TOKEN`은 Slack에서 사용할 봇의 토큰입니다.

## 2. GraphQL API v4 쿼리
Github의 커밋 여부를 확인하기 위해 다음과 같은 쿼리를 사용했습니다.
```
query{
    user(login: :git_user_name:) {
        contributionsCollection(from: yyyy-MM-ddT00:00:00, to: yyyy-MM-ddT00:00:00) {
        totalCommitContributions
        }
    }
}
```
> 시간은 모두 당일 같은 날을 입력하였습니다.  

쿼리의 실행 결과는 [GitHub GraphQL API v4 Explorer](https://developer.github.com/v4/explorer/)를 통해 확인할 수 있습니다.

## 3. AWS CloudWatch Event
[AWS CloudWatch Event Docs](https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/WhatIsCloudWatchEvents.html)를 참고하여 이벤트를 생성하였습니다.

1. CloudWatch > 이벤트 > 규칙 > 규칙 생성으로 규칙을 생성합니다.
2. 이벤트 소스는 일정으로 선택하고 Cron 표현식을 선택하여 규칙을 입력합니다.
3. 대상에서 Lambda를 통해 만든 함수를 추가한 뒤 세부 정보 구성을 누릅니다.
4. 세부 정보 구성에서 원하는 정보를 입력한 뒤 규칙을 생성합니다.

> Cron의 시간이 GMT 시간 기준이므로 이에 맞춰 Cron 표현식을 입력해주었습니다.
