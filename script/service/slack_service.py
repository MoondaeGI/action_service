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

    def send_alarm(self, message):
        data = {
            "channel": self.channel_id,
            "text": message
        }
        requests.post(self.url, headers=self.headers, json=data)