import os
import datetime
from pathlib import Path

class ChatLogger:
    def __init__(self, log_directory="chat_log"):
        self.log_directory = Path(log_directory)
        self.log_directory.mkdir(exist_ok=True)
        self.current_date = None
        self.log_file_path = None
        self.conversation_count = 0

    def get_today_log_file(self):
        """오늘 날짜의 로그 파일 경로를 반환"""
        today = datetime.date.today()
        if self.current_date != today:
            self.current_date = today
            date_str = today.strftime("%Y-%m-%d")
            self.log_file_path = self.log_directory / f"copilot_chat_log_{date_str}.txt"

            # 새 날짜면 대화 카운트 리셋
            if not self.log_file_path.exists():
                self.conversation_count = 0
                self.create_new_log_file()

        return self.log_file_path

    def create_new_log_file(self):
        """새로운 로그 파일 생성"""
        with open(self.log_file_path, 'w', encoding='utf-8') as f:
            f.write(f"=== GitHub Copilot Chat Log - {self.current_date.strftime('%Y년 %m월 %d일')} ===\n\n")

    def log_conversation(self, user_message, copilot_response):
        """대화를 로그 파일에 저장"""
        log_file = self.get_today_log_file()
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")

        with open(log_file, 'a', encoding='utf-8') as f:
            if self.conversation_count > 0:
                f.write("\n---\n\n")

            f.write(f"[{timestamp}] 사용자: {user_message}\n\n")
            f.write(f"GitHub Copilot: {copilot_response}\n")

            self.conversation_count += 1

    def log_user_message(self, message):
        """사용자 메시지만 먼저 로그"""
        log_file = self.get_today_log_file()
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")

        with open(log_file, 'a', encoding='utf-8') as f:
            if self.conversation_count > 0:
                f.write("\n---\n\n")
            f.write(f"[{timestamp}] 사용자: {message}\n\n")

    def log_copilot_response(self, response):
        """Copilot 응답 추가"""
        log_file = self.get_today_log_file()

        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(f"GitHub Copilot: {response}\n")
            self.conversation_count += 1

# 전역 로거 인스턴스
chat_logger = ChatLogger()

# 간편 사용 함수들
def log_chat(user_msg, copilot_response):
    """대화 전체를 한 번에 로그"""
    chat_logger.log_conversation(user_msg, copilot_response)

def log_user(message):
    """사용자 메시지만 로그"""
    chat_logger.log_user_message(message)

def log_copilot(response):
    """Copilot 응답만 로그"""
    chat_logger.log_copilot_response(response)

# 테스트 함수
def test_logger():
    """로거 테스트"""
    print("Chat Logger 테스트 시작...")

    log_chat(
        "안녕하세요! 로거 테스트입니다.",
        "안녕하세요! 로거가 정상적으로 작동하고 있습니다."
    )

    log_chat(
        "파일이 제대로 생성되었나요?",
        "네, 오늘 날짜로 로그 파일이 생성되었습니다!"
    )

    print(f"로그 파일 경로: {chat_logger.get_today_log_file()}")
    print("테스트 완료!")

if __name__ == "__main__":
    test_logger()
