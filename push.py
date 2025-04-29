from git import Repo, GitCommandError
from gitdb.exc import BadName
from service.notion_service import NotionService
from service.slack_service import SlackService
from service.git_service import GitService

def update_commit(git_service, notion_service, commit):
    commit_message, commit_hash, changed_files, commit_date, ai_summary = git_service.get_commit_info(commit)
    notion_service.update_commit(commit_message, commit_hash, changed_files, commit_date, ai_summary)

def update_all_new_commits():
    git_service = GitService()
    notion_service = NotionService()
    repo = Repo(search_parent_directories=True)

    try:
        last_hash = notion_service.select_last_commit_hash()
        current_head = repo.head.commit
        print("test")

        if not last_hash or last_hash is None:
            commit = repo.head.commit
            update_commit(git_service, notion_service, commit)
            return

        try:
            repo.commit(last_hash)
            for commit in repo.iter_commits(f"{last_hash}..{current_head}"):
                update_commit(git_service, notion_service, commit)
        except (BadName, GitCommandError) as e:
            print(f"커밋을 찾을 수 없음: {str(e)}")
            commit = repo.head.commit
            update_commit(git_service, notion_service, commit)
    except Exception as e:
        print(f"예상치 못한 에러 발생: {str(e)}")

# 메인 실행
if __name__ == "__main__":
    slack_service = SlackService()

    update_all_new_commits()
    slack_service.send_alarm("push가 완료되었습니다.")


