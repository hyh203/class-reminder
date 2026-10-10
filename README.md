# Class Reminder Test Version
## 效果
企微和飞书同步收到提醒
## 使用
1. 克隆项目
```bash
get clone https://github.com/hyh203/class-reminder
```
2. 安装依赖
```bash
pip install requests python-dotenv
```
3. 配置环境变量
创建'.env'文件
```
WECOM_WEBHOOK_URL=你的企微webhook
FEISHU_WEBHOOK_URL=你的飞书webhook
```
4. 运行
```bash
python MAIN.PY
```
## 配置机器人
### 企业微信
"团队"→消息推送→添加→复制 webhook URL
### 飞书
群设置（桌面版）→群机器人→自定义机器人→复制 webhook URL