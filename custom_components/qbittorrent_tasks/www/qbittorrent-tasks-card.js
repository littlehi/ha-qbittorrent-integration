class QBittorrentTasksCard extends HTMLElement {
  setConfig(config) {
    if (!config.entity) {
      throw new Error('You need to define an entity');
    }
    this.config = config;
    this._lastUpdate = null;
    this._expanded = false;
  }

  set hass(hass) {
    this._hass = hass;
    const entity = hass.states[this.config.entity];
    if (!entity) return;
    
    const currentUpdate = entity.last_updated;
    if (this._lastUpdate !== currentUpdate) {
      this._lastUpdate = currentUpdate;
      this.render();
    }
  }

  render() {
    const entity = this._hass.states[this.config.entity];
    if (!entity) {
      this.innerHTML = `<ha-card><div class="card-content">Entity not found</div></ha-card>`;
      return;
    }

    const torrents = entity.attributes.torrents || [];
    const taskCount = entity.state;

    if (!this._card) {
      this.innerHTML = `
        <ha-card>
          <div class="card-header">
            <div class="name">qBittorrent Tasks</div>
            <div class="count"></div>
          </div>
          <div class="card-content"></div>
          <div class="expand-button" style="display: none;"></div>
        </ha-card>
        <style>
          .card-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 12px 16px;
            border-bottom: 1px solid var(--divider-color);
          }
          .name { font-weight: bold; font-size: 14px; }
          .count { color: var(--secondary-text-color); font-size: 12px; }
          .no-tasks {
            text-align: center;
            color: var(--secondary-text-color);
            padding: 16px;
            font-size: 13px;
          }
          .task-item {
            display: grid;
            grid-template-columns: 2fr 80px 60px 80px;
            align-items: center;
            padding: 6px 16px;
            border-bottom: 1px solid var(--divider-color);
            gap: 12px;
          }
          .task-item:last-child { border-bottom: none; }
          .task-name {
            font-weight: 500;
            font-size: 12px;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
            min-width: 0;
          }
          .task-progress-bar {
            width: 80px;
            height: 4px;
            background: var(--disabled-color);
            border-radius: 2px;
            position: relative;
          }
          .progress-fill {
            height: 100%;
            background: var(--primary-color);
            border-radius: 2px;
            transition: width 0.3s ease;
          }
          .task-progress {
            text-align: right;
            font-weight: bold;
            font-size: 11px;
            color: var(--primary-color);
          }
          .task-speed {
            text-align: right;
            font-size: 11px;
            color: var(--secondary-text-color);
          }
          .state {
            padding: 1px 4px;
            border-radius: 3px;
            text-transform: capitalize;
            font-size: 10px;
          }
          .state.downloading { background: var(--success-color); color: white; }
          .state.uploading { background: var(--info-color); color: white; }
          .state.completed { background: var(--primary-color); color: white; }
          .state.paused { background: var(--warning-color); color: white; }
          .speed { color: var(--secondary-text-color); }
          .expand-button {
            text-align: center;
            padding: 8px;
            border-top: 1px solid var(--divider-color);
            cursor: pointer;
            color: var(--primary-color);
            font-size: 12px;
            background: var(--card-background-color);
          }
          .expand-button:hover {
            background: var(--secondary-background-color);
          }
        </style>
      `;
      this._card = this.querySelector('ha-card');
    }
    
    // Update content without rebuilding DOM
    const countEl = this.querySelector('.count');
    const contentEl = this.querySelector('.card-content');
    const expandEl = this.querySelector('.expand-button');
    
    countEl.textContent = `${taskCount} active`;
    
    if (torrents.length === 0) {
      contentEl.innerHTML = '<div class="no-tasks">No active tasks</div>';
      expandEl.style.display = 'none';
    } else {
      // Sort by progress (ascending)
      const sortedTorrents = [...torrents].sort((a, b) => a.progress - b.progress);
      const displayTorrents = this._expanded ? sortedTorrents : sortedTorrents.slice(0, 10);
      
      contentEl.innerHTML = displayTorrents.map(torrent => `
        <div class="task-item">
          <div class="task-name">${this.cleanTaskName(torrent.name)}</div>
          <div class="task-progress-bar">
            <div class="progress-fill" style="width: ${torrent.progress}%"></div>
          </div>
          <div class="task-progress">${torrent.progress.toFixed(1)}%</div>
          <div class="task-speed">${this.formatSpeed(torrent.download_speed)}</div>
        </div>
      `).join('');
      
      if (sortedTorrents.length > 10) {
        expandEl.style.display = 'block';
        expandEl.textContent = this._expanded ? 
          `收起 (显示前10个)` : 
          `展开显示全部 (${sortedTorrents.length}个任务)`;
        expandEl.onclick = () => {
          this._expanded = !this._expanded;
          this.render();
        };
      } else {
        expandEl.style.display = 'none';
      }
    }
  }

  cleanTaskName(name) {
    // Remove file extension
    let cleaned = name.replace(/\.(torrent|zip|rar|7z)$/i, '');
    // Remove prefix like [xxx.xx] or [xxx]
    cleaned = cleaned.replace(/^\[[^\]]+\]/, '');
    return cleaned.trim();
  }

  formatSpeed(bytes) {
    if (bytes === 0) return '0 B/s';
    const k = 1024;
    const sizes = ['B/s', 'KB/s', 'MB/s', 'GB/s'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i];
  }

  getCardSize() {
    return 1;
  }
}

// 确保在DOM加载完成后注册自定义元素
if (!customElements.get('qbittorrent-tasks-card')) {
  customElements.define('qbittorrent-tasks-card', QBittorrentTasksCard);
  console.log('qBittorrent Tasks Card registered successfully');
}

// 注册到window.customCards
window.customCards = window.customCards || [];
if (!window.customCards.find(card => card.type === 'qbittorrent-tasks-card')) {
  window.customCards.push({
    type: 'qbittorrent-tasks-card',
    name: 'qBittorrent Tasks Card',
    description: 'Display qBittorrent download tasks'
  });
}