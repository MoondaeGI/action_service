import os
import requests

class NotionService:
    def __init__(self):
        self.notion_key = os.getenv("NOTION_API_KEY")
        self.notion_db_id = os.getenv("NOTION_DB_ID")

        self.notion_insert_url = "https://api.notion.com/v1/pages"
        self.notion_select_url = f"https://api.notion.com/v1/databases/{self.notion_db_id}/query"
        self.headers = {
            "Authorization": f"Bearer {self.notion_key}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }

    def update_commit(self, commit_message, commit_hash, changed_files, commit_date, ai_summary):
        data = {
            "parent": {
                "database_id": self.notion_db_id
            },
            "properties": {
                "커밋 메세지": {"title": [{"text": {"content": commit_message}}]},
                "커밋 해시": {"rich_text": [{"text": {"content": commit_hash}}]},
                "작성일": {"date": {"start": commit_date}},
                "변경된 파일": {"rich_text": [{"text": {"content": ", ".join(changed_files)}}]},
                "AI 요약": {"rich_text": [{"text": {"content": ai_summary}}]},
                "요약": {"rich_text": [{"text": {"content": f"커밋된 변경 사항: {', '.join(changed_files)}"}}]}
            }
        }

        response = requests.post(self.notion_insert_url, headers=self.headers, json=data)

        if response.status_code == 200:
            print("Notion 페이지 생성 성공!")
            print(f"페이지 URL: https://notion.so/{response.json()['id'].replace('-', '')}")
            return True
        else:
            print(f"Error: {response.status_code}, {response.text}")
            return False

    def select_last_commit_hash(self):
        data = {
            "page_size": 1,
            "sorts": [
                {
                    "property": "작성일",
                    "direction": "descending"
                }
            ]
        }

        response = requests.post(self.notion_select_url, headers=self.headers, json=data)

        if response.status_code == 200:
            print("Notion 마지막 커밋 가져오기 성공")
            response_data = response.json()

            # results가 비어있지 않은지 확인
            if response_data["results"]:
                # 커밋 해시 가져오기
                commit_hash = response_data["results"][0]["properties"]["커밋 해시"]["rich_text"][0]["text"]["content"]
                return commit_hash
            else:
                print("데이터베이스에 커밋 기록이 없습니다.")
                return None
        else:
            print(f"Error: {response.status_code}, {response.text}")
            return None