# AGENTS.md

## Build/Test Commands
```bash
# Run the full integration test suite (no Home Assistant required)
python3 test_standalone.py

# Test fetching a single plant (requires active network)
python3 -c "
from test_standalone import NuclearDataFetcher, PLANTS
f = NuclearDataFetcher();
print(f._fetch_vattenfall_data('ringhals', PLANTS['ringhals']))
"
```

No lint, typecheck, or formatter config exists in this repo. There is no `pyproject.toml`, `setup.cfg`, or CI workflow.

## Architecture

This is a Home Assistant custom integration distributed via HACS.

**`hacs.json` sets `"content_in_root": false`** — the integration code lives in `custom_components/swedish_nuclear_power/`, not at the repo root. Only the HA integration package is loaded; the root `test_standalone.py` is for development only.

### Data Fetching
Two distinct data sources, gated by the `api` flag in plant configs:

| Source | Plants | Mechanism |
|---|---|---|
| Vattenfall (HTML scraping) | Ringhals, Forsmark | Extracts embedded JSON from `<script type="application/json">` tags in the page HTML |
| OKG API | Oskarshamn | Direct API call; **requires `?format=json` query parameter** |

The coordinator (`coordinator.py`) uses **sync `requests.Session`** wrapped in `async_add_executor_job` to avoid blocking the HA event loop.

### Plant Configuration
`test_standalone.py` has its **own standalone copy** of `PLANTS`. When changing plant configs (reactors, URLs, capacities), you **must update both** `const.py` (the HA integration) **and** `test_standalone.py` (the test harness).

### Sensor Layout
- One power sensor per reactor (e.g. `sensor.ringhals_r3_power`)
- One timestamp sensor per plant (e.g. `sensor.ringhals_last_update`)
- One total-power sensor (`sensor.swedish_nuclear_power_total_power`)

## Style & Conventions

- `from __future__ import annotations` in every Python file
- Home Assistant integration patterns: `ConfigFlow`, `OptionsFlow`, `DataUpdateCoordinator`, `CoordinatorEntity`
- Config constants: `const.py` defines `CONF_SCAN_INTERVAL` (matches HA's built-in `homeassistant.const.CONF_SCAN_INTERVAL` — they have the same value `"scan_interval"` but are separate symbols)
- `dateutil.parser` is used in `sensor.py` for timestamp parsing (not listed in `manifest.json` requirements — it ships with HA)

## Pitfalls

- The Vattenfall scraping depends on HTML `<script type="application/json">` blocks being present. If the target site changes its markup, extraction breaks silently.
- `manifest.json` declares `requirements: ["requests"]` but `sensor.py` also imports `dateutil`. If HA ever removes `dateutil` from its bundled packages, the integration will fail at runtime.
