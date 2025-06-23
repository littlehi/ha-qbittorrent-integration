# Home Assistant qBittorrent Integration

一个用于Home Assistant的qBittorrent集成，可以监控和显示下载任务。

## 功能特性

- 监控qBittorrent下载任务
- 显示任务进度、状态、速度等信息
- 自定义Lovelace卡片显示
- 支持中英文界面

## 安装

### 通过HACS安装（推荐）

1. 在HACS中添加自定义仓库：`https://github.com/littlehi/ha-qbittorrent-integration`
2. 搜索"qBittorrent Tasks"并安装
3. 重启Home Assistant

### 手动安装

1. 下载此仓库
2. 将`custom_components/qbittorrent_tasks`文件夹复制到你的Home Assistant配置目录的`custom_components`文件夹中
3. 重启Home Assistant

## 配置

1. 在Home Assistant中进入"配置" > "集成"
2. 点击"添加集成"，搜索"qBittorrent Tasks"
3. 输入qBittorrent的连接信息：
   - 主机地址
   - 端口号
   - 用户名
   - 密码

## 使用自定义卡片

安装集成后，自定义卡片会自动可用。在仪表板中添加卡片：

```yaml
type: custom:qbittorrent-tasks-card
entity: sensor.qbittorrent_tasks
```

## 实体说明

集成会创建一个sensor实体：`sensor.qbittorrent_tasks`

- **状态值**：当前活跃任务数量
- **属性**：包含所有任务的详细信息（名称、进度、状态、速度等）

## 许可证

MIT License