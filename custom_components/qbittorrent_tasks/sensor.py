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

from .const import (
    ATTR_DOWNLOADED,
    ATTR_ETA,
    ATTR_PROGRESS,
    ATTR_RATIO,
    ATTR_SIZE,
    ATTR_SPEED_DOWN,
    ATTR_SPEED_UP,
    ATTR_STATE,
    DOMAIN,
)
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

    @callback
    def _create_entities():
        entities = []
        for torrent_hash, torrent_data in coordinator.data.items():
            entities.append(
                QBittorrentTorrentSensor(
                    coordinator=coordinator,
                    torrent_hash=torrent_hash,
                )
            )
        return entities

    coordinator.async_add_listener(_create_entities)
    async_add_entities(_create_entities())


class QBittorrentTorrentSensor(
    CoordinatorEntity[QBittorrentDataUpdateCoordinator], SensorEntity
):
    """Representation of a qBittorrent torrent sensor."""

    def __init__(
        self,
        coordinator: QBittorrentDataUpdateCoordinator,
        torrent_hash: str,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._torrent_hash = torrent_hash
        self._attr_unique_id = f"{DOMAIN}_{torrent_hash}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, coordinator.config_entry.entry_id)},
            name="qBittorrent",
            manufacturer="qBittorrent",
        )

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return self.coordinator.data[self._torrent_hash]["name"]

    @property
    def native_value(self) -> StateType:
        """Return the state of the sensor."""
        return f"{self.coordinator.data[self._torrent_hash]['progress']}%"

    @property
    def extra_state_attributes(self) -> dict:
        """Return the state attributes of the sensor."""
        data = self.coordinator.data[self._torrent_hash]
        return {
            ATTR_PROGRESS: data["progress"],
            ATTR_STATE: data["state"],
            ATTR_DOWNLOADED: data["downloaded"],
            ATTR_SIZE: data["size"],
            ATTR_SPEED_DOWN: data["download_speed"],
            ATTR_SPEED_UP: data["upload_speed"],
            ATTR_RATIO: data["ratio"],
            ATTR_ETA: data["eta"],
        }