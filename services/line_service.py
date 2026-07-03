import os
import requests
from dotenv import load_dotenv

load_dotenv()

def send_line_message(message):
    token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")

    if not token:
        print("❌ 找不到 LINE Token")
        return

    url = "https://api.line.me/v2/bot/message/broadcast"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    data = {
        "messages": [
            {
                "type": "text",
                "text": message[:4900]
            }
        ]
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        print("✅ LINE 文字推播成功")
    else:
        print("❌ LINE 文字推播失敗")
        print(response.status_code)
        print(response.text)


def send_line_image(image_url):
    token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")

    if not token:
        print("❌ 找不到 LINE Token")
        return

    url = "https://api.line.me/v2/bot/message/broadcast"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    data = {
        "messages": [
            {
                "type": "image",
                "originalContentUrl": image_url,
                "previewImageUrl": image_url
            }
        ]
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        print("✅ LINE 圖片推播成功")
    else:
        print("❌ LINE 圖片推播失敗")
        print(response.status_code)
        print(response.text)
