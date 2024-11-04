"""Support for Oil Price sensors."""
from __future__ import annotations

import logging
from datetime import timedelta
import aiohttp

from homeassistant.components.sensor import (
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)
from homeassistant.helpers.device_registry import DeviceInfo

from .const import (
    DOMAIN,
    CONF_PROVINCE,
    SENSOR_TYPES,
    API_URL,
)

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(hours=12)

SENSOR_ICONS = {
    "92h": "mdi:gas-station",
    "95h": "mdi:gas-station",
    "98h": "mdi:gas-station",
    "0h": "mdi:gas-station"
}

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Oil Price sensor."""
    province = config_entry.data[CONF_PROVINCE]

    async def async_update_data():
        """Fetch data from API."""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(API_URL) as response:
                    if response.status != 200:
                        _LOGGER.error("API request failed with status: %s", response.status)
                        return {}
                    
                    data = await response.json()
                    # 查找匹配省份的数据
                    for item in data:
                        if item.get("city") == province:
                            _LOGGER.debug("Found data for province %s: %s", province, item)
                            return item
                    
                    _LOGGER.warning("No data found for province: %s", province)
                    return {}
                    
        except Exception as err:
            _LOGGER.error("Error in update method: %s", err)
            return {}

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name=f"oil_price_{province}",
        update_method=async_update_data,
        update_interval=SCAN_INTERVAL,
    )

    await coordinator.async_config_entry_first_refresh()

    entities = []
    for sensor_type, sensor_name in SENSOR_TYPES.items():
        entities.append(
            OilPriceSensor(
                coordinator,
                config_entry,
                province,
                sensor_type,
                sensor_name,
            )
        )

    async_add_entities(entities)

class OilPriceSensor(CoordinatorEntity, SensorEntity):
    """Representation of an Oil Price sensor."""

    def __init__(
        self,
        coordinator,
        config_entry: ConfigEntry,
        province: str,
        sensor_type: str,
        sensor_name: str,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._province = province
        self._sensor_type = sensor_type
        self._attr_name = f"{province} {sensor_name}"
        self._attr_unique_id = f"oil_price_{province}_{sensor_type}"
        self._attr_native_unit_of_measurement = "元/升"
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_icon = SENSOR_ICONS.get(sensor_type)
        
        # Device info
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, f"{province}_oil_price")},
            name=f"{province}油价",
            manufacturer="聚合api数据",
            model="油价信息",
            via_device=(DOMAIN, config_entry.entry_id),
            entry_type="service",
            configuration_url="https://www.ndrc.gov.cn/",
            sw_version="1.0",
            suggested_area=""
        )

    @property
    def native_value(self) -> StateType:
        """Return the state of the sensor."""
        if self.coordinator.data:
            value = self.coordinator.data.get(self._sensor_type)
            try:
                if value is not None:
                    return float(value)
                return None
            except (ValueError, TypeError) as err:
                _LOGGER.error(
                    "Error converting value for %s/%s: %s",
                    self._province,
                    self._sensor_type,
                    err
                )
                return None
        return None

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        if self.coordinator.data:
            return {
                "city": self.coordinator.data.get("city"),
                "last_update": self.coordinator.last_update_success
            }
        return None