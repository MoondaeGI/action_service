import os
from openai import OpenAI

class GitService:
    def __init__(self):
        self.client = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))

    def get_commit_info(self, commit):
        commit_message = commit.message.strip()
        commit_hash = commit.hexsha[:7]
        changed_files = list(commit.stats.files.keys())
        commit_date = commit.committed_datetime.strftime('%Y-%m-%d %H:%M:%S')
        commit_author = commit.author.name

        diffs = []
        for diff in commit.parents[0].diff(commit):
            change_type = ""
            if diff.new_file:
                change_type = "추가된 파일"
            elif diff.deleted_file:
                change_type = "삭제된 파일"
            elif diff.renamed_file:
                change_type = "이름이 변경된 파일"
            else:
                change_type = "수정된 파일"

            file_path = diff.b_path or diff.a_path

            try:
                if hasattr(diff, 'diff_bytes') and diff.diff_bytes:
                    diff_content = diff.diff_bytes[0].decode('utf-8')

                    # 파일 변경 내용에서 추가된 줄(+)과 삭제된 줄(-) 정보 추출
                    added_lines = sum(1 for line in diff_content.split('\n') if line.startswith('+'))
                    removed_lines = sum(1 for line in diff_content.split('\n') if line.startswith('-'))

                    diffs.append(f"{change_type}: {file_path}\n"
                                 f"추가된 줄: {added_lines - 1}, 삭제된 줄: {removed_lines - 1}\n"
                                 f"변경 내용:\n{diff_content}")
                    print(added_lines)
                    print(removed_lines)
                    print(diff_content)
                else:
                    print("변경사항 보이지 않음")
                    diffs.append(f"{change_type}: {file_path}")
            except Exception as e:
                diffs.append(f"{change_type}: {file_path} (변경 내용 분석 실패: {str(e)})")

        diff_content = "\n\n---\n\n".join(diffs)
        prompt = f"""
                       다음은 Git 커밋의 내용입니다:

                       커밋 메시지: {commit_message}
                       변경된 파일들: {', '.join(changed_files)}

                       변경 내용:
                       {diff_content}

                       이 커밋의 주요 변경사항을 3-4문장으로 요약해주세요. 기술적인 내용을 포함해주세요.
                       """
        print(prompt)

        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=300
            )
            ai_summary = response.choices[0].message.content.strip()
        except Exception as e:
            ai_summary = f"요약 생성 실패: {str(e)}"

        return commit_message, commit_hash, changed_files, commit_date, ai_summary