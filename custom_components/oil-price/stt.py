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

from .const import (
    DOMAIN,
    CONF_PROVINCE,
    SENSOR_TYPES,
    API_URL,
)

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(hours=12)

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Oil Price sensor."""
    province = config_entry.data[CONF_PROVINCE]

    async def async_update_data():
        """Fetch data from API."""
        async with aiohttp.ClientSession() as session:
            async with session.get(API_URL) as response:
                data = await response.json()
                # 根据实际API返回格式处理数据
                return data.get(province, {})

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

    @property
    def native_value(self) -> StateType:
        """Return the state of the sensor."""
        if self.coordinator.data:
            return self.coordinator.data.get(self._sensor_type)
        return None