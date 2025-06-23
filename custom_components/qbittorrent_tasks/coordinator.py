"""Data update coordinator for qBittorrent Tasks."""
from datetime import timedelta
import logging

import qbittorrentapi

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    CONF_HOST,
    CONF_PASSWORD,
    CONF_PORT,
    CONF_USERNAME,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)
SCAN_INTERVAL = timedelta(seconds=30)

class QBittorrentDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching qBittorrent data."""

    def __init__(
        self,
        hass: HomeAssistant,
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=SCAN_INTERVAL,
        )
        self.config_entry = config_entry
        
        host = config_entry.data[CONF_HOST]
        port = config_entry.data[CONF_PORT]
        username = config_entry.data[CONF_USERNAME]
        password = config_entry.data[CONF_PASSWORD]

        self.client = qbittorrentapi.Client(
            host=host,
            port=port,
            username=username,
            password=password,
        )

    async def _async_update_data(self):
        """Fetch data from qBittorrent."""
        try:
            # Get torrents data
            torrents = await self.hass.async_add_executor_job(
                self.client.torrents_info
            )
            
            # Process torrents data
            data = {}
            for torrent in torrents:
                data[torrent.hash] = {
                    "name": torrent.name,
                    "progress": round(torrent.progress * 100, 2),
                    "state": torrent.state,
                    "downloaded": torrent.downloaded,
                    "size": torrent.size,
                    "download_speed": torrent.dlspeed,
                    "upload_speed": torrent.upspeed,
                    "ratio": round(torrent.ratio, 3),
                    "eta": torrent.eta,
                }
            return data

        except Exception as err:
            raise UpdateFailed(f"Error communicating with qBittorrent: {err}")