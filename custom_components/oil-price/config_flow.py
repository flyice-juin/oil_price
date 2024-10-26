"""Config flow for Oil Price integration."""
from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult

from .const import DOMAIN, PROVINCES, CONF_PROVINCE

class OilPriceConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Oil Price."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            return self.async_create_entry(
                title=f"油价 - {user_input[CONF_PROVINCE]}",
                data=user_input,
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_PROVINCE): vol.In(PROVINCES),
                }
            ),
            errors=errors,
        )