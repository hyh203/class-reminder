from dotenv import load_dotenv
load_dotenv()  # 加载 .env 文件中的环境变量
import os
import requests
# 从环境变量中获取 Webhook URL
import requests
WECOM_WEBHOOK_URL = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=7f6adbe8-3783-43fe-b11a-b4e80cfff92d"
FEISHU_WEBHOOK_URL = "https://open.feishu.cn/open-apis/bot/v2/hook/69c5955d-05c1-4d62-9a0a-308e53bf86ee"
def send_wecom_message(message):
    """企业微信消息发送"""
    data = {
        "msgtype": "text",
        "text": {
            "content": message
        }
    }
    response = requests.post(WECOM_WEBHOOK_URL, json=data)
    result = response.json()
    print(f"企业微信消息发送结果: {result}")
    return result.get("errcode") == 0

def send_feishu_message(message):
    if"提醒" not in message:
        message = "提醒：" + message
    data = {
        "msg_type": "text",
        "content": {
            "text": message
        }
    }
    response= requests.post(FEISHU_WEBHOOK_URL, json=data)
    print(f"飞书返回：{response.json()}")
    return response.json().get("code") == 0
def send_both_messages(message):
    """双通道推送"""
    wecom_ok = send_wecom_message(message)
    feishu_ok = send_feishu_message(message)
    print(f"\n结果：")
    print(f"企业微信", "成功" if wecom_ok else "失败")
    print(f"飞书", "成功" if feishu_ok else "失败")
if __name__ == "__main__":
        test_message = "测试消息：test message"
        send_both_messages(test_message)