class QBittorrentTasksCard extends HTMLElement {
  setConfig(config) {
    if (!config.entity) {
      throw new Error('You need to define an entity');
    }
    this.config = config;
  }

  set hass(hass) {
    this._hass = hass;
    this.render();
  }

  render() {
    const entity = this._hass.states[this.config.entity];
    if (!entity) {
      this.innerHTML = `<ha-card><div class="card-content">Entity not found</div></ha-card>`;
      return;
    }

    const torrents = entity.attributes.torrents || [];
    const taskCount = entity.state;

    this.innerHTML = `
      <ha-card>
        <div class="card-header">
          <div class="name">qBittorrent Tasks</div>
          <div class="count">${taskCount} active</div>
        </div>
        <div class="card-content">
          ${torrents.length === 0 ? 
            '<div class="no-tasks">No active tasks</div>' :
            torrents.map(torrent => `
              <div class="task-item">
                <div class="task-name">${torrent.name}</div>
                <div class="task-info">
                  <div class="progress-bar">
                    <div class="progress-fill" style="width: ${torrent.progress}%"></div>
                    <span class="progress-text">${torrent.progress}%</span>
                  </div>
                  <div class="task-details">
                    <span class="state ${torrent.state}">${torrent.state}</span>
                    <span class="speed">↓ ${this.formatSpeed(torrent.download_speed)} ↑ ${this.formatSpeed(torrent.upload_speed)}</span>
                  </div>
                </div>
              </div>
            `).join('')
          }
        </div>
      </ha-card>
      <style>
        .card-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          padding: 16px;
          border-bottom: 1px solid var(--divider-color);
        }
        .name { font-weight: bold; }
        .count { color: var(--secondary-text-color); }
        .no-tasks {
          text-align: center;
          color: var(--secondary-text-color);
          padding: 20px;
        }
        .task-item {
          padding: 12px 16px;
          border-bottom: 1px solid var(--divider-color);
        }
        .task-item:last-child { border-bottom: none; }
        .task-name {
          font-weight: 500;
          margin-bottom: 8px;
          overflow: hidden;
          text-overflow: ellipsis;
          white-space: nowrap;
        }
        .progress-bar {
          position: relative;
          height: 20px;
          background: var(--disabled-color);
          border-radius: 10px;
          margin-bottom: 8px;
        }
        .progress-fill {
          height: 100%;
          background: var(--primary-color);
          border-radius: 10px;
          transition: width 0.3s ease;
        }
        .progress-text {
          position: absolute;
          top: 50%;
          left: 50%;
          transform: translate(-50%, -50%);
          font-size: 12px;
          font-weight: bold;
          color: white;
          text-shadow: 1px 1px 1px rgba(0,0,0,0.5);
        }
        .task-details {
          display: flex;
          justify-content: space-between;
          font-size: 12px;
        }
        .state {
          padding: 2px 6px;
          border-radius: 4px;
          text-transform: capitalize;
        }
        .state.downloading { background: var(--success-color); color: white; }
        .state.uploading { background: var(--info-color); color: white; }
        .state.completed { background: var(--primary-color); color: white; }
        .state.paused { background: var(--warning-color); color: white; }
        .speed { color: var(--secondary-text-color); }
      </style>
    `;
  }

  formatSpeed(bytes) {
    if (bytes === 0) return '0 B/s';
    const k = 1024;
    const sizes = ['B/s', 'KB/s', 'MB/s', 'GB/s'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i];
  }

  getCardSize() {
    return 3;
  }
}

customElements.define('qbittorrent-tasks-card', QBittorrentTasksCard);

window.customCards = window.customCards || [];
window.customCards.push({
  type: 'qbittorrent-tasks-card',
  name: 'qBittorrent Tasks Card',
  description: 'Display qBittorrent download tasks'
});