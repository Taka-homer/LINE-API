"""LINE Messaging API で、指定ユーザーへテキストメッセージを送る。"""

import os
import sys
from pathlib import Path

import requests
from dotenv import load_dotenv

ENV_PATH = Path(__file__).resolve().parent / ".env"
PUSH_URL = "https://api.line.me/v2/bot/message/push"


def main() -> None:
    load_dotenv(ENV_PATH)

    token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", "").strip()
    user_id = os.getenv("LINE_USER_ID", "").strip()
    if not token or not user_id:
        print(
            ".env の LINE_CHANNEL_ACCESS_TOKEN と LINE_USER_ID を記入してください。",
            file=sys.stderr,
        )
        sys.exit(1)

    text = " ".join(sys.argv[1:]).strip()
    if not text:
        text = "こんにちは。LINE Messaging API からのテスト送信です。"

    response = requests.post(
        PUSH_URL,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        json={
            "to": user_id,
            "messages": [{"type": "text", "text": text}],
        },
        timeout=30,
    )

    if response.status_code != 200:
        print(
            f"送信に失敗しました ({response.status_code}): {response.text}",
            file=sys.stderr,
        )
        sys.exit(1)

    print("メッセージを送信しました。")


if __name__ == "__main__":
    main()
