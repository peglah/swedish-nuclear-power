"""Options flow for Swedish Nuclear Power integration."""

from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant.config_entries import ConfigEntry, OptionsFlow
from homeassistant.const import CONF_SCAN_INTERVAL
from homeassistant.helpers.selector import NumberSelector, NumberSelectorConfig

from .const import DEFAULT_SCAN_INTERVAL


class SwedishNuclearPowerOptionsFlow(OptionsFlow):
    """Handle options flow for Swedish Nuclear Power."""

    def __init__(self, config_entry: ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(
                title="Swedish Nuclear Power",
                data=user_input,
            )

        scan_interval = self.config_entry.options.get(
            CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL
        )

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Optional(
                        CONF_SCAN_INTERVAL,
                        default=scan_interval,
                    ): NumberSelector(
                        NumberSelectorConfig(
                            min=30,
                            max=3600,
                            step=30,
                            unit_of_measurement="seconds",
                            mode="slider",
                        )
                    ),
                }
            ),
        )