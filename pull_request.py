import sys
from service.slack_service import SlackService

def send_pull_request_alarm(slack_service):
    slack_service.send_alarm("pull_request")

def merge_alarm(slack_service):
    slack_service.send_alarm("merge")

def closed_alarm(slack_service):
    slack_service.send_alarm("closed")

if __name__ == "__main__":
    slack_service = SlackService()

    # 첫 번째 argument를 받아와 (ex: "merge", "closed", "pull_request")
    action = sys.argv[1]
    merged = sys.argv[2] if len(sys.argv) > 2 else None

    print(action, merged)
    print("test")

    if action == "opened":
        # PR 오픈
        send_pull_request_alarm(slack_service)

    elif action == "closed":
        # PR 닫힘: merged 여부 판단
        if merged and merged.lower() == "true":
            merge_alarm(slack_service)
        else:
            closed_alarm(slack_service)

    else:
        print(f"Unknown action: {action}")