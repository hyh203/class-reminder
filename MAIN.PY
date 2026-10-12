from dotenv import load_dotenv
load_dotenv()

import os
import tempfile
import requests
from datetime import datetime, timedelta
from google.oauth2 import service_account
from googleapiclient.discovery import build

# 从环境变量创建临时密钥文件
google_creds = os.getenv('GOOGLE_CREDENTIALS')
if google_creds:
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        f.write(google_creds)
        creds_path = f.name
else:
     creds_path = 'class-reminder.json'  # 本地测试用

WECOM_WEBHOOK_URL = os.getenv('WECOM_WEBHOOK_URL')
FEISHU_WEBHOOK_URL = os.getenv('FEISHU_WEBHOOK_URL')
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def get_calendar_service():
    """获取日历服务（服务账号，无需浏览器）"""
    creds = service_account.Credentials.from_service_account_file(
        creds_path, scopes=SCOPES
    )
    return build('calendar', 'v3', credentials=creds)


def get_tomorrow_events(service):
    """获取明天的所有日程"""
    now = datetime.now()
    tomorrow = now + timedelta(days=1)
    start_of_day = tomorrow.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_day = tomorrow.replace(hour=23, minute=59, second=59)
    
    time_min = start_of_day.isoformat() + '+08:00'
    time_max = end_of_day.isoformat() + '+08:00'
    
    calendar_id = 'hyh20030404@gmail.com'  # 你的邮箱
    
    print(f"正在查询日历：{calendar_id}")  # 加这行
    print(f"时间范围：{time_min} 到 {time_max}")  # 加这行
    
    events_result = service.events().list(
        calendarId=calendar_id,
        timeMin=time_min,
        timeMax=time_max,
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    
    events = events_result.get('items', [])
    print(f"找到 {len(events)} 个事件")  # 加这行
    
    return events


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
    if "提醒" not in message:
        message = "提醒：" + message

    data = {
        "msg_type": "text",
        "content": {
            "text": message
        }
    }
    response = requests.post(FEISHU_WEBHOOK_URL, json=data)
    result = response.json()
    print(f"飞书返回：{result}")
    return result.get("code") == 0


def send_both_messages(message):
    wecom_ok = send_wecom_message(message)
    feishu_ok = send_feishu_message(message)
    print("\n结果：")
    print(f"企业微信：{'成功' if wecom_ok else '失败'}")
    print(f"飞书：{'成功' if feishu_ok else '失败'}")


def check_and_remind():
    """检查明天的课程并提醒"""
    now = datetime.now()
    print("正在获取明天日历...")
    service = get_calendar_service()
    events = get_tomorrow_events(service)

    if not events:
        print("明天没有课")
        return

    tomorrow = now + timedelta(days=1)
    tomorrow_str = tomorrow.strftime("%Y-%m-%d %A")

    print(f"明天是：{tomorrow_str}")
    print(f"明天有 {len(events)} 门课：\n")

    course_list = []
    for event in events:
        start_str = event['start'].get('dateTime', event['start'].get('date'))

        if 'T' in start_str:
            event_time = datetime.fromisoformat(start_str.replace('Z', '+08:00'))
            event_time = event_time.replace(tzinfo=None)

            summary = event.get('summary', '未命名')
            location = event.get('location', '地点未设置')

            course_list.append({
                'name': summary,
                'time': event_time.strftime('%H:%M'),
                'location': location
            })

            print(f"{summary} | {event_time.strftime('%H:%M')} | {location}")

    if course_list:
        msg = f"📅 明日课程提醒（{tomorrow_str}）\n\n"

        for i, course in enumerate(course_list, 1):
            msg += f"{i}. {course['name']}\n"
            msg += f"   时间：{course['time']}\n"
            msg += f"   地点：{course['location']}\n\n"

        msg += "请提前做好准备！"

        print("\n发送汇总提醒...")
        send_both_messages(msg)


if __name__ == "__main__":
    check_and_remind()  
