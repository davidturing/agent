# 手把手教你部署 OpenClaw：打通飞书，构建你的私人 AI 助理 (Windows/Ubuntu 双版)

![OpenClaw Feishu Integration](https://image.pollinations.ai/prompt/A%20cyberpunk%20terminal%20screen%20running%20OpenClaw%20code,%20connected%20to%20a%20glowing%20Feishu%20Lark%20logo,%20neon%20blue%20and%20purple%20tech%20background,%20highly%20detailed?width=1024&height=576&nologo=true)

**发布时间**：2026年2月4日
**作者**：OpenClaw 实战实验室

---

## 🚀 为什么是 OpenClaw？

最近在推特上看到大佬 [@xiaohuiai666](https://x.com/xiaohuiai666) 分享的 OpenClaw 玩法，确实让人眼前一亮。不同于普通的 Chatbot，OpenClaw 更像是一个**有手有脚的 AI 操作系统**。它不仅能陪你聊天，还能帮你操作终端、管理文件、甚至写代码。

今天我们就来复刻大佬的实战路径，把这个强大的 AI 装进你的电脑，并通过飞书随时随地指挥它。

---

## 🛠️ 第一步：把地基打好 (安装篇)

无论你是 Windows 党还是 Linux 极客，只需三步即可起飞。

### 💻 Windows 用户看这里
1.  **下载 Node.js**：去 [官网](https://nodejs.org/) 下载 v20 或 v22 LTS 版本，一路 Next 安装。
2.  **一键安装**：打开 PowerShell（管理员模式），输入：
    ```powershell
    npm install -g openclaw
    ```
3.  **初始化**：
    ```powershell
    openclaw init
    ```
    *建议：工作目录选个空间大的盘，别塞 C 盘里。*

### 🐧 Ubuntu/Linux 用户看这里
Linux 部署更适合服务器长期运行。

```bash
# 1. 安装 Node.js (使用 NodeSource 源)
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs

# 2. 安装 OpenClaw
sudo npm install -g openclaw

# 3. 启动并保活 (使用 pm2)
sudo npm install -g pm2
pm2 start openclaw -- gateway run
pm2 save
```

---

## 🔗 第二步：打通任督二脉 (飞书集成)

这是最关键的一步。我们要让 OpenClaw 住进飞书里，成为你的 24 小时在线助理。

### 1. 申请“身份证” (飞书开放平台)
登录 [飞书开放平台](https://open.feishu.cn/)，创建一个**“企业自建应用”**。
*   **名称**：超级助理 OpenClaw
*   **图标**：选个帅气的

### 2. 拿到“钥匙” (凭证)
在应用详情页左侧，找到 **“凭证与基础信息”**，复制以下两个码：
*   `App ID`
*   `App Secret`

### 3. 赋予“权力” (权限管理)
在 **“开发配置” -> “权限管理”** 里，搜索并开通：
*   ✅ `im:message` (读取/发送消息)
*   ✅ `im:resource` (图片文件上传)
*   *记得发布一个版本，权限才会生效！*

### 4. 建立“连接” (配置 OpenClaw)
回到你的电脑终端，运行：
```bash
openclaw configure --section channel
```
选择 `feishu`，填入刚才的 App ID 和 Secret。

### 5. 开启“听觉” (事件订阅)
OpenClaw 启动后会显示一个 Webhook 地址（如 `http://公网IP:3000/webhook/feishu`）。
*   回到飞书后台 **“事件订阅”**。
*   填入这个 URL。
*   添加事件：`接收消息 (im.message.receive_v1)`。

---

## 💡 避坑指南 (参考大佬经验)

1.  **网络问题**：如果你的服务器在内网，飞书回调不过来。推荐使用 `cpolar` 或 `frp` 做内网穿透。
2.  **权限报错**：如果机器人不回话，99% 是因为飞书后台的**“权限管理”**里没点**“批量开通”**或者没**“发布版本”**。
3.  **Docker 部署**：如果你喜欢容器化，OpenClaw 也支持 Docker 一键拉起，更干净卫生。

---

## 🎉 完工

现在，打开飞书，给你的机器人发一句“**系统状态**”，如果它回复了当前的 CPU 和内存信息，恭喜你，你已经拥有了最硬核的 AI 助理！

*参考链接：[GitHub Spec Kit 使用指南](https://dvspace5.wordpress.com/?p=19)*
