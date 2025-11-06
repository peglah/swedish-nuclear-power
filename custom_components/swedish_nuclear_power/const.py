"""Constants for Swedish Nuclear Power integration."""

from __future__ import annotations

DOMAIN = "swedish_nuclear_power"
CONF_SCAN_INTERVAL = "scan_interval"

# Default scan interval in seconds
DEFAULT_SCAN_INTERVAL = 60

# Plant configurations
PLANTS = {
    "ringhals": {
        "name": "Ringhals",
        "url": "https://karnkraft.vattenfall.se/ringhals/produktion",
        "reactors": ["R3", "R4"],
        "max_capacity": {"R3": 1074, "R4": 1130},  # Maximum capacity in MW from technical data
    },
    "forsmark": {
        "name": "Forsmark", 
        "url": "https://karnkraft.vattenfall.se/forsmark/produktion",
        "reactors": ["F1", "F2", "F3"],
        "max_capacity": {"F1": 1014, "F2": 1121, "F3": 1172},  # Maximum capacity in MW from technical data
    },
    "okg": {
        "name": "Oskarshamn",
        "url": "https://okg.se/.netlify/functions/getReactorOutput",
        "reactors": ["O3"],
        "api": True,
        "max_capacity": {"O3": 1450},  # Maximum capacity in MW for percentage calculation
    },
}