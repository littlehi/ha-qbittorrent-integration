"""Frontend for qBittorrent Tasks integration."""
from homeassistant.components.frontend import add_extra_js_url
from homeassistant.core import HomeAssistant
from .const import DOMAIN


async def async_setup_frontend(hass: HomeAssistant) -> None:
    """Set up the frontend."""
    # Add the JavaScript file to Home Assistant
    add_extra_js_url(hass, f"/{DOMAIN}/qbittorrent-tasks-card.js")