# Class Reminder Test Version
## Development Notes/声明
This is a personal learning project developed with substantial assistance from AI coding tools.I initiated the project, defined its intended functionality, and used AI-assisted workflows to implement and test the initial version. I am continuing to learn the underlying code and implementation details.The current version has passed the tests I have run, but this does not necessarily mean that all functionality is bug-free or production-ready. 
请留意，此项目为个人学习作品，在开发过程中使用了大量人工智能协助。我本人定义其预期能达到的效果，并使用人工智能辅助我进行上述测试，我仍在学习相关底层代码与逻辑此版本为测试版，取得了我认为满意的效果，但仍未达到完美状态，敬请留意

自动课程提醒，支持企业微信和飞书双通道推送。

## 效果

- 每天 **北京时间 21:00** 自动推送明天的课程安排
- 同时推送到企业微信和飞书
- 支持 Lecture（每周）和 Tutorial（特定日期）两种课程类型

## 快速开始（Fork 使用）

### 第一步：Fork 这个仓库

点击右上角 **Fork**，复制到你的 GitHub 账号。

### 第二步：配置机器人（二选一或都配）

#### 企业微信
1. 下载企业微信 APP，创建群聊（只有自己也可以）
2. 群设置 → 群机器人 → 添加 → 复制 Webhook 地址

#### 飞书
1. 下载飞书 APP，创建群聊
2. 群设置 → 群机器人 → 添加机器人 → 自定义机器人
3. **安全设置**：添加关键词"提醒"（必须，否则收不到消息）
4. 复制 Webhook 地址

### 第三步：配置 Google Calendar

1. 打开 [Google Cloud Console](https://console.cloud.google.com/)
2. 创建新项目 → 启用 **Google Calendar API**
3. 凭据 → 创建凭据 → **OAuth 客户端 ID** → 桌面应用
4. 下载 `credentials.json`
5. 打开文件，复制全部内容（压缩成一行）

### 第四步：添加到 GitHub Secrets

在你的 Fork 仓库中：
**Settings** → **Secrets and variables** → **Actions** → **New repository secret**

添加三个 Secrets：

| Name | Value |
|------|-------|
| `WECOM_WEBHOOK_URL` | 你的企微 Webhook 地址 |
| `FEISHU_WEBHOOK_URL` | 你的飞书 Webhook 地址 |
| `GOOGLE_CREDENTIALS` | 刚才复制的 JSON 一行内容 |

### 第五步：添加课程到 Google Calendar

- **Lecture**：创建重复事件（每周）
- **Tutorial**：手动添加特定日期的日程

### 第六步：测试

**Actions** → **Class Reminder** → **Run workflow** 手动触发测试。

明天开始每天 21:00 自动推送。

## 本地运行（可选）

```bash
# 克隆项目
git clone https://github.com/你的用户名/class-reminder.git
cd class-reminder

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 填入你的配置

# 运行
python MAIN.PY
```
## 提醒
``` bash
| 文件                               | 说明                    |
| -------------------------------- | --------------------- |
| `MAIN.PY`                        | 主程序：读取日历 → 判断时间 → 推送  |
| `.env.example`                   | 环境变量模板（复制为 `.env` 使用） |
| `.github/workflows/reminder.yml` | GitHub Actions 定时任务配置 |
| `requirements.txt`               | Python 依赖列表           |
```
## Q&A
``` bash
常见问题
Q: 推送没收到？
检查 GitHub Actions 是否显示绿色勾（成功）
检查飞书机器人关键词是否设置为"提醒"
检查企业微信机器人是否在群里
Q: 如何修改推送时间？
修改 .github/workflows/reminder.yml 中的 cron 时间
默认 '0 13 * * *' 是 UTC 13:00（北京时间 21:00）
Q: 不想用 Google Calendar？
可以修改 MAIN.PY 读取 JSON/Excel 文件（需自行开发）
```
