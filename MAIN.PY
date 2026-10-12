from dotenv import load_dotenv
load_dotenv()  # 加载 .env 文件中的环境变量
import os
import tempfile
import requests
from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# 从环境变量中获取 Webhook URL
google_creds = os.getenv('GOOGLE_CREDENTIALS')
if google_creds:
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        f.write(google_creds)
        creds_path = f.name
else:
    creds_path = 'credentials.json'

WECOM_WEBHOOK_URL = os.getenv("WECOM_WEBHOOK_URL")
FEISHU_WEBHOOK_URL = os.getenv("FEISHU_WEBHOOK_URL")
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def get_calendar_service():
    flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
    creds = flow.run_local_server(port=0)
    return build('calendar', 'v3', credentials=creds)

def get_today_events(service):
    """获取今天的日程"""
    now = datetime.now()
    start_of_day = now.replace(hour=0, minute=0, second=0)
    end_of_day = now.replace(hour=23, minute=59, second=59)
    time_min = start_of_day.isoformat() + '+08:00'
    time_max = end_of_day.isoformat() + '+08:00'
    events_result = service.events().list(
        calendarId='primary',
        timeMin=time_min,
        timeMax=time_max,
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    return events_result.get('items', [])
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
    wecom_ok = send_wecom_message(message)
    feishu_ok = send_feishu_message(message)
    print(f"\n结果：")
    print(f"企业微信", "成功" if wecom_ok else "失败")
    print(f"飞书", "成功" if feishu_ok else "失败")
def check_and_send_reminders():
    """ 检查明天课程并发送提醒 """
    now = datetime.now()
    
    from dotenv import load_dotenv
load_dotenv()

import os
import requests
from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# 配置
WECOM_WEBHOOK_URL = os.getenv("WECOM_WEBHOOK_URL")
FEISHU_WEBHOOK_URL = os.getenv("FEISHU_WEBHOOK_URL")
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def get_calendar_service():
    """获取日历服务"""
    flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
    creds = flow.run_local_server(port=0)
    return build('calendar', 'v3', credentials=creds)

def get_tomorrow_events(service):
    """获取明天的所有日程"""
    now = datetime.now()
    tomorrow = now + timedelta(days=1)
    start_of_day = tomorrow.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_day = tomorrow.replace(hour=23, minute=59, second=59)
    
    time_min = start_of_day.isoformat() + '+08:00'
    time_max = end_of_day.isoformat() + '+08:00'
    
    events_result = service.events().list(
        calendarId='primary',
        timeMin=time_min,
        timeMax=time_max,
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    
    return events_result.get('items', [])

def send_wecom_message(message):
    data = {
        "msgtype": "text",
        "text": {"content": message}
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
        "content": {"text": message}
    }
    response = requests.post(FEISHU_WEBHOOK_URL, json=data)
    result = response.json()
    print(f"飞书返回：{result}")
    return result.get("code") == 0

def send_both_messages(message):
    wecom_ok = send_wecom_message(message)
    feishu_ok = send_feishu_message(message)
    
    print(f"\n结果：")
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
    
    # 汇总所有课程
    course_list = []
    
    for event in events:
        start_str = event['start'].get('dateTime', event['start'].get('date'))
        
        if 'T' in start_str:
            event_time = datetime.fromisoformat(start_str.replace('Z', '+08:00'))
            event_time = event_time.replace(tzinfo=None)
            
            summary = event['summary']
            location = event.get('location', '地点未设置')
            
            course_list.append({
                'name': summary,
                'time': event_time.strftime('%H:%M'),
                'location': location
            })
            
            print(f"{summary} | {event_time.strftime('%H:%M')} | {location}")
    
    # 生成汇总消息
    if course_list:
        msg = f"📅 明日课程提醒（{tomorrow_str}）\n\n"
        
        for i, course in enumerate(course_list, 1):
            msg += f"{i}. {course['name']}\n"
            msg += f"   时间：{course['time']}\n"
            msg += f"   地点：{course['location']}\n\n"
        
        msg += "请提前做好准备！"
        
        print(f"\n发送汇总提醒...")
        send_both_messages(msg)

if __name__ == "__main__":
    check_and_remind()  
