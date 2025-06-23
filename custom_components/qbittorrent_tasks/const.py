"""Constants for the qBittorrent Tasks integration."""
from homeassistant.const import (
    CONF_HOST,
    CONF_PASSWORD,
    CONF_PORT,
    CONF_USERNAME,
)

DOMAIN = "qbittorrent_tasks"
DEFAULT_NAME = "qBittorrent"
DEFAULT_PORT = 8080
DEFAULT_USERNAME = "admin"

ATTR_PROGRESS = "progress"
ATTR_STATE = "state"
ATTR_DOWNLOADED = "downloaded"
ATTR_SIZE = "size"
ATTR_SPEED_DOWN = "download_speed"
ATTR_SPEED_UP = "upload_speed"
ATTR_RATIO = "ratio"
ATTR_ETA = "eta"