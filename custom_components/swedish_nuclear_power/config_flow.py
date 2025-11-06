"""Config flow for Swedish Nuclear Power integration."""

from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.const import CONF_SCAN_INTERVAL
from homeassistant.helpers.selector import NumberSelector, NumberSelectorConfig

from .const import DEFAULT_SCAN_INTERVAL, DOMAIN


class SwedishNuclearPowerConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Swedish Nuclear Power."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""
        if user_input is not None:
            return self.async_create_entry(
                title="Swedish Nuclear Power",
                data=user_input,
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Optional(
                        CONF_SCAN_INTERVAL,
                        default=DEFAULT_SCAN_INTERVAL,
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