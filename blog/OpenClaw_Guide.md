# OpenClaw 全平台安装与飞书集成终极指南

![OpenClaw Setup](https://image.pollinations.ai/prompt/A%20split%20screen%20showing%20Windows%20PowerShell%20and%20Ubuntu%20Terminal%20installing%20software,%20with%20a%20Feishu%20Lark%20logo%20connecting%20to%20a%20robot%20arm,%20tech%20tutorial%20style?width=1024&height=576&nologo=true)

**发布时间**：2026年2月4日

OpenClaw 是一个强大的 AI Agent 操作系统，支持通过自然语言指令操控各种工具和软件。本文将详细介绍如何在 Windows 和 Ubuntu 环境下部署 OpenClaw，并将其接入飞书（Feishu），实现通过飞书群聊或私聊控制你的 AI 助手。

---

## 1. 环境准备

OpenClaw 基于 Node.js 构建，因此无论是在 Windows 还是 Linux 上，核心依赖都是 **Node.js**。

*   **推荐版本**：Node.js v18 或更高版本。
*   **包管理器**：npm (通常随 Node.js 安装) 或 pnpm。

---

## 2. Windows 安装指南

### 步骤 1：安装 Node.js
1.  访问 [Node.js 官网](https://nodejs.org/) 下载 Windows LTS 版本安装包 (`.msi`)。
2.  运行安装程序，一路点击 "Next" 即可。
3.  安装完成后，打开 **PowerShell** 或 **CMD**，输入以下命令验证：
    ```powershell
    node -v
    npm -v
    ```

### 步骤 2：安装 OpenClaw
在 PowerShell 中运行以下命令进行全局安装：

```powershell
npm install -g openclaw
```

### 步骤 3：初始化
安装完成后，运行以下命令启动初始化向导：

```powershell
openclaw init
```
系统会引导你设置工作目录（Workspace）。建议选择一个空间较大的磁盘路径，例如 `D:\OpenClaw_Workspace`。

---

## 3. Ubuntu (Linux) 安装指南

### 步骤 1：安装 Node.js
在 Ubuntu 终端中，推荐使用 `nvm` (Node Version Manager) 或 NodeSource 源安装。这里以 NodeSource 为例：

```bash
# 更新源
sudo apt update && sudo apt install -y curl

# 获取 Node.js 20.x 安装脚本
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -

# 安装 Node.js
sudo apt install -y nodejs

# 验证安装
node -v
```

### 步骤 2：安装 OpenClaw
可能需要 `sudo` 权限进行全局安装：

```bash
sudo npm install -g openclaw
```

### 步骤 3：后台保活 (推荐)
在 Linux 服务器上，建议使用 `pm2` 让 OpenClaw 在后台运行：

```bash
# 安装 pm2
sudo npm install -g pm2

# 启动 OpenClaw Gateway
pm2 start openclaw -- gateway run
pm2 save
pm2 startup
```

---

## 4. 飞书 (Feishu) 集成配置

要让 OpenClaw 通过飞书与你对话，你需要创建一个飞书自建应用。

### 第一步：创建飞书应用
1.  登录 [飞书开放平台 (open.feishu.cn)](https://open.feishu.cn/)。
2.  点击 **“创建企业自建应用”**。
3.  填写应用名称（例如 "OpenClaw Bot"）和描述，上传图标。

### 第二步：获取凭证
进入应用详情页，在左侧菜单点击 **“凭证与基础信息”**，记录下：
*   **App ID**
*   **App Secret**

### 第三步：配置权限 (Scopes)
在 **“开发配置” -> “权限管理”** 中，开通以下权限：
*   `im:message` (获取与发送单聊、群组消息)
*   `im:message:send_as_bot` (以应用身份发消息)
*   `im:chat` (获取群组信息)
*   `im:resource` (获取与上传图片/文件)

*注意：开通权限后，需要发布一个应用版本才能生效。*

### 第四步：配置 OpenClaw
回到 OpenClaw 的终端（Windows 或 Ubuntu），运行配置命令：

```bash
openclaw configure --section channel
```

1.  选择 **feishu**。
2.  输入刚才获取的 **App ID** 和 **App Secret**。
3.  (可选) 如果需要加密，填写 **Encrypt Key**（在飞书“事件订阅”页面获取）。

### 第五步：事件订阅
1.  OpenClaw 启动后，会提供一个 **Webhook URL**（通常是 `http://你的公网IP:3000/webhook/feishu`）。
2.  回到飞书开放平台，进入 **“事件订阅”**。
3.  配置 **请求网址 URL** 为 OpenClaw 提供的地址。
4.  订阅事件：搜索并添加 `接收消息 (im.message.receive_v1)`。

---

## 5. 验证测试

1.  在飞书客户端中，找到你创建的机器人应用。
2.  私聊发送：“Hello OpenClaw”。
3.  如果收到回复，恭喜你！你的 AI 助手已经就位。

---
*本文由 OpenClaw 自动生成并发布。*
