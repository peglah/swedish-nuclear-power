"""Sensor platform for Swedish Nuclear Power integration."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import UnitOfPower
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, PLANTS
from .coordinator import SwedishNuclearPowerCoordinator

# Sensor descriptions
POWER_SENSOR_DESCRIPTION = SensorEntityDescription(
    key="power",
    name="Power Output",
    native_unit_of_measurement=UnitOfPower.MEGAWATT,
    device_class=SensorDeviceClass.POWER,
    state_class=SensorStateClass.MEASUREMENT,
    icon="mdi:reactor",
)

TIMESTAMP_SENSOR_DESCRIPTION = SensorEntityDescription(
    key="last_update",
    name="Last Update",
    device_class=SensorDeviceClass.TIMESTAMP,
    icon="mdi:clock",
)

TOTAL_POWER_SENSOR_DESCRIPTION = SensorEntityDescription(
    key="total_power",
    name="Total Swedish Nuclear Power",
    native_unit_of_measurement=UnitOfPower.MEGAWATT,
    device_class=SensorDeviceClass.POWER,
    state_class=SensorStateClass.MEASUREMENT,
    icon="mdi:reactor",
)


async def async_setup_entry(
    hass: HomeAssistant, entry, async_add_entities
) -> None:
    """Set up the sensor platform."""
    coordinator: SwedishNuclearPowerCoordinator = hass.data[DOMAIN][entry.entry_id]
    
    entities: List[SensorEntity] = []
    
    # Create sensors for each plant and reactor
    for plant_key, plant_config in PLANTS.items():
        # Add reactor power sensors
        for reactor in plant_config["reactors"]:
            entities.append(
                NuclearPowerSensor(
                    coordinator,
                    plant_key,
                    reactor,
                    POWER_SENSOR_DESCRIPTION,
                )
            )
        
        # Add last update sensor for each plant
        entities.append(
            NuclearPowerSensor(
                coordinator,
                plant_key,
                plant_key,
                TIMESTAMP_SENSOR_DESCRIPTION,
            )
        )
    
    # Add total power sensor
    entities.append(
        TotalNuclearPowerSensor(coordinator, TOTAL_POWER_SENSOR_DESCRIPTION)
    )
    
    async_add_entities(entities)


class NuclearPowerSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Nuclear Power sensor."""

    def __init__(
        self,
        coordinator: SwedishNuclearPowerCoordinator,
        plant_key: str,
        reactor_name: str,
        description: SensorEntityDescription,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.coordinator = coordinator
        self.plant_key = plant_key
        self.reactor_name = reactor_name
        self.entity_description = description
        self.plant_config = PLANTS[plant_key]
        
        # Set unique ID and name
        if reactor_name == plant_key:
            # This is a timestamp sensor
            self._attr_unique_id = f"{DOMAIN}_{plant_key}_last_update"
            self._attr_name = f"{self.plant_config['name']} Last Update"
        else:
            # This is a power sensor
            self._attr_unique_id = f"{DOMAIN}_{plant_key}_{reactor_name}_power"
            self._attr_name = f"{self.plant_config['name']} {reactor_name} Power"

    @property
    def native_value(self) -> Any:
        """Return the state of the sensor."""
        data = self.coordinator.data
        if not data or self.plant_key not in data:
            return None
        
        plant_data = data[self.plant_key]
        
        if self.entity_description.key == "last_update":
            # Return timestamp
            return plant_data.get("timestamp")
        else:
            # Return reactor power
            for reactor_data in plant_data.get("data", []):
                if reactor_data.get("name") == self.reactor_name:
                    return reactor_data.get("production", 0)
        
        return None

    @property
    def extra_state_attributes(self) -> Dict[str, Any]:
        """Return additional state attributes."""
        data = self.coordinator.data
        if not data or self.plant_key not in data:
            return {}
        
        plant_data = data[self.plant_key]
        
        if self.entity_description.key == "power":
            # Add percentage for power sensors
            for reactor_data in plant_data.get("data", []):
                if reactor_data.get("name") == self.reactor_name:
                    attrs = {}
                    if reactor_data.get("percent") is not None:
                        attrs["percentage"] = round(reactor_data["percent"], 2)
                    if "valueDate" in reactor_data:
                        attrs["value_date"] = reactor_data["valueDate"]
                    return attrs
        
        return {}

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information."""
        return DeviceInfo(
            identifiers={(DOMAIN, self.plant_key)},
            name=self.plant_config["name"],
            manufacturer="Swedish Nuclear Power Plants",
            model=f"{self.plant_config['name']} Nuclear Power Plant",
        )


class TotalNuclearPowerSensor(CoordinatorEntity, SensorEntity):
    """Representation of the total Swedish nuclear power sensor."""

    def __init__(
        self,
        coordinator: SwedishNuclearPowerCoordinator,
        description: SensorEntityDescription,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.coordinator = coordinator
        self.entity_description = description
        self._attr_unique_id = f"{DOMAIN}_total_power"
        self._attr_name = "Total Swedish Nuclear Power"

    @property
    def native_value(self) -> Any:
        """Return the total power output."""
        data = self.coordinator.data
        if not data:
            return None
        
        total_power = 0
        
        for plant_key, plant_data in data.items():
            for reactor_data in plant_data.get("data", []):
                total_power += reactor_data.get("production", 0)
        
        return round(total_power, 2)

    @property
    def extra_state_attributes(self) -> Dict[str, Any]:
        """Return additional state attributes."""
        data = self.coordinator.data
        if not data:
            return {}
        
        attrs = {}
        reactor_count = 0
        active_reactors = 0
        
        for plant_key, plant_data in data.items():
            for reactor_data in plant_data.get("data", []):
                reactor_count += 1
                if reactor_data.get("production", 0) > 0:
                    active_reactors += 1
        
        attrs["total_reactors"] = reactor_count
        attrs["active_reactors"] = active_reactors
        attrs["last_updated"] = datetime.now().isoformat()
        
        return attrs

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information."""
        return DeviceInfo(
            identifiers={(DOMAIN, "swedish_nuclear_power")},
            name="Swedish Nuclear Power",
            manufacturer="Swedish Nuclear Power Plants",
            model="National Power Grid",
        )