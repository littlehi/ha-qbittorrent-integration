"""Frontend for qBittorrent Tasks integration."""
from homeassistant.components.frontend import add_extra_js_url
from homeassistant.core import HomeAssistant


async def async_setup_frontend(hass: HomeAssistant) -> None:
    """Set up the frontend."""
    add_extra_js_url(hass, "/qbittorrent_tasks/qbittorrent-tasks-card.js")