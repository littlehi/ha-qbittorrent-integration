# Home Assistant qBittorrent Tasks

[![hacs_badge](https://img.shields.io/badge/HACS-Default-41BDF5.svg?style=for-the-badge)](https://github.com/hacs/integration)

这个 Home Assistant 集成组件可以显示 qBittorrent 的下载任务列表和进度信息。

## 功能特点

- 显示所有正在下载的种子任务
- 实时更新下载进度
- 显示详细信息包括：
  - 下载进度
  - 任务状态
  - 已下载大小
  - 文件总大小
  - 下载速度
  - 上传速度
  - 分享率
  - 预计完成时间

## 安装

### HACS 安装（推荐）

1. 确保已经安装了 [HACS](https://hacs.xyz/)
2. 在 HACS 中搜索 "qBittorrent Tasks"
3. 点击安装
4. 重启 Home Assistant

### 手动安装

1. 下载此仓库
2. 将 `custom_components/qbittorrent_tasks` 文件夹复制到你的 Home Assistant 配置目录下的 `custom_components` 文件夹中
3. 重启 Home Assistant

## 配置

1. 进入 Home Assistant 配置界面
2. 点击 "配置" -> "设备与服务"
3. 点击右下角的 "添加集成"
4. 搜索 "qBittorrent Tasks"
5. 输入以下信息：
   - 主机地址：qBittorrent Web UI 的 IP 地址
   - 端口：qBittorrent Web UI 的端口（默认 8080）
   - 用户名：Web UI 登录用户名（默认 admin）
   - 密码：Web UI 登录密码

## 使用

安装完成后，每个种子任务都会创建一个传感器实体。你可以：

1. 在仪表板中添加这些传感器
2. 创建自动化基于下载状态
3. 在 Lovelace 卡片中显示下载进度

## 故障排除

如果遇到问题：

1. 确保 qBittorrent Web UI 可以正常访问
2. 检查用户名和密码是否正确
3. 确认 Home Assistant 可以访问 qBittorrent 的网络

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可

MIT License