# Class Reminder Test Version
## Development Notes/声明
This is a personal learning project developed with substantial assistance from AI coding tools.I initiated the project, defined its intended functionality, and used AI-assisted workflows to implement and test the initial version. I am continuing to learn the underlying code and implementation details.The current version has passed the tests I have run, but this does not necessarily mean that all functionality is bug-free or production-ready. 
请留意，此项目为个人学习作品，在开发过程中使用了大量人工智能协助。我本人定义其预期能达到的效果，并使用人工智能辅助我进行上述测试，我仍在学习相关底层代码与逻辑此版本为测试版，取得了我认为满意的效果，但仍未达到完美状态，敬请留意
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