import sys
from service.slack_service import SlackService

def send_pull_request_alarm(slack_service, pr_title, pr_author):
    slack_service.send_alarm(f"{pr_author}의 pr이 도착했습니다. {pr_title}")

def merge_alarm(slack_service, pr_title, pr_author):
    slack_service.send_alarm(f"{pr_author}님의 {pr_title}이(가) merge되었습니다.")

def closed_alarm(slack_service, pr_title, pr_author):
    slack_service.send_alarm(f"{pr_author}님의 {pr_title}이(가) 반려되었습니다.")

if __name__ == "__main__":
    slack_service = SlackService()

    # 첫 번째 argument를 받아와 (ex: "merge", "closed", "pull_request")
    action = sys.argv[1]
    merged = sys.argv[2] if len(sys.argv) > 2 else None
    pr_title = sys.argv[3] if len(sys.argv) > 3 else "Unknown PR"
    pr_author = sys.argv[4] if len(sys.argv) > 4 else "Unknown Author"

    print(action, merged)
    print("test")

    if action == "opened":
        # PR 오픈
        send_pull_request_alarm(slack_service, pr_title, pr_author)

    elif action == "closed":
        # PR 닫힘: merged 여부 판단
        if merged and merged.lower() == "true":
            merge_alarm(slack_service, pr_title, pr_author)
        else:
            closed_alarm(slack_service, pr_title, pr_author)

    else:
        print(f"Unknown action: {action}")