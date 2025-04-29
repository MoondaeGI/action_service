import os
import requests

class SlackService:
    def __init__(self):
        self.slack_token = os.getenv("SLACK_BOT_USER_OAUTH_TOKEN")
        self.channel_id = os.getenv("SLACK_CHANNEL_ID")
        self.url = "https://slack.com/api/chat.postMessage"
        self.headers = {
            "Authorization": f"Bearer {self.slack_token}",
            "Content-Type": "application/json; charset=utf-8"
        }

    def send_alarm(self, state):
        text = self.makeText(state)

        data = {
            "channel": self.channel_id,
            "text": text
        }

        print(self.headers)
        print(data)
        response = requests.post(self.url, headers=self.headers, json=data)
        print(response.json())

    def makeText(self, state) -> str | None:
        if state == "push":
            return "push가 완료되었습니다."
        elif state == "merge":
            return "request가 merge되었습니다."
        elif state == "closed":
            return "request가 반려되었습니다."
        elif state == "pull_request":
            return "pull_request가 도착했습니다."
        else:
            return None