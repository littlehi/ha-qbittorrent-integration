"""Support for qBittorrent sensors."""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
import logging

from homeassistant.components.sensor import (
    SensorEntity,
    SensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
)

from .const import DOMAIN
from .coordinator import QBittorrentDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)

@dataclass
class QBittorrentSensorEntityDescription(SensorEntityDescription):
    """Class describing qBittorrent sensor entities."""

    value_fn: Callable = lambda x: x


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up qBittorrent sensor entries."""
    coordinator: QBittorrentDataUpdateCoordinator = hass.data[DOMAIN][
        config_entry.entry_id
    ]

    async_add_entities([QBittorrentSensor(coordinator)])


class QBittorrentSensor(
    CoordinatorEntity[QBittorrentDataUpdateCoordinator], SensorEntity
):
    """Representation of qBittorrent tasks sensor."""

    def __init__(self, coordinator: QBittorrentDataUpdateCoordinator) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{DOMAIN}_tasks"
        self._attr_name = "qBittorrent Tasks"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, coordinator.config_entry.entry_id)},
            name="qBittorrent",
            manufacturer="qBittorrent",
        )

    @property
    def native_value(self) -> StateType:
        """Return the number of active torrents."""
        return len(self.coordinator.data)

    @property
    def extra_state_attributes(self) -> dict:
        """Return the state attributes with all torrents info."""
        if not self.coordinator.data:
            return {"torrents": []}
        
        torrents = []
        for torrent_hash, data in self.coordinator.data.items():
            torrents.append({
                "hash": torrent_hash,
                "name": data["name"],
                "progress": data["progress"],
                "state": data["state"],
                "download_speed": data["download_speed"],
                "upload_speed": data["upload_speed"],
            })
        
        return {"torrents": torrents}