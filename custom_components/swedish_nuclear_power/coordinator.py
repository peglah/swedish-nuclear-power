"""Data coordinator for Swedish Nuclear Power integration."""

from __future__ import annotations

import asyncio
import json
import logging
import re
from datetime import datetime
from typing import Any, Dict, Optional

import requests

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import PLANTS, DOMAIN

_LOGGER = logging.getLogger(__name__)


class SwedishNuclearPowerCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from Swedish nuclear power plants."""

    def __init__(self, hass: HomeAssistant, scan_interval: int) -> None:
        """Initialize."""
        super().__init__(
            hass,
            logger=_LOGGER,
            name="Swedish Nuclear Power",
            update_interval=scan_interval,
        )
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })

    async def _async_update_data(self) -> Dict[str, Any]:
        """Update data via library."""
        try:
            # Use asyncio to run the synchronous requests in an executor
            data = await self.hass.async_add_executor_job(self._fetch_all_plants)
            return data
        except Exception as exception:
            raise UpdateFailed(f"Error communicating with nuclear plants: {exception}")

    def _fetch_all_plants(self) -> Dict[str, Any]:
        """Fetch data from all nuclear plants."""
        all_data = {}
        
        for plant_key, plant_config in PLANTS.items():
            try:
                if plant_config.get("api", False):
                    # O3 API call
                    data = self._fetch_okg_data(plant_config)
                else:
                    # Vattenfall scraping
                    data = self._fetch_vattenfall_data(plant_key, plant_config)
                
                if data:
                    all_data[plant_key] = data
                    
            except Exception as e:
                _LOGGER.warning(f"Failed to fetch data from {plant_config['name']}: {e}")
                continue
        
        return all_data

    def _fetch_vattenfall_data(self, plant_key: str, plant_config: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Fetch data from Vattenfall plants (Ringhals, Forsmark)."""
        try:
            url = plant_config["url"]
            _LOGGER.info(f"Fetching data from {url}")
            
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            data = self._extract_production_data(response.text, plant_key)
            if data:
                _LOGGER.info(f"Successfully extracted data for {plant_key}")
                return data
            else:
                _LOGGER.error(f"Failed to extract data from {plant_key}")
                return None
                
        except requests.RequestException as e:
            _LOGGER.error(f"Request error for {plant_key}: {e}")
        except Exception as e:
            _LOGGER.error(f"Unexpected error for {plant_key}: {e}")
            return None

    def _extract_production_data(self, html_content: str, plant_name: str) -> Optional[Dict[str, Any]]:
        """Extract production data from the JSON embedded in HTML."""
        try:
            # Look for JSON data in script tags
            pattern = r'<script[^>]*type="application/json"[^>]*>(.*?)</script>'
            matches = re.findall(pattern, html_content, re.DOTALL)
            
            for match in matches:
                try:
                    json_data = json.loads(match.strip())
                    if 'powerPlant' in json_data and 'blockProductionDataList' in json_data:
                        if json_data['powerPlant'].lower() == plant_name.lower():
                            return {
                                'timestamp': json_data.get('timestamp'),
                                'power_plant': json_data['powerPlant'],
                                'data': json_data['blockProductionDataList']
                            }
                except json.JSONDecodeError:
                    continue
            
            _LOGGER.warning(f"No valid JSON data found for {plant_name}")
            return None
            
        except Exception as e:
            _LOGGER.error(f"Error extracting data for {plant_name}: {e}")
            return None

    def _fetch_okg_data(self, plant_config: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Fetch data from OKG O3 API."""
        try:
            url = plant_config["url"]
            _LOGGER.info(f"Fetching data from {url}")
            
            # OKG API requires format parameter
            response = self.session.get(f"{url}?format=json", timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            # Calculate percentage for O3 using max capacity
            max_capacity = plant_config.get("max_capacity", {}).get("O3", 1450)
            current_power = data.get('value', 0)
            percentage = (current_power / max_capacity * 100) if max_capacity > 0 else 0
            
            # OKG returns single reactor data
            return {
                'timestamp': data.get('timestamp'),
                'power_plant': plant_config['name'],
                'data': [{
                    'name': 'O3',
                    'production': current_power,
                    'percent': round(percentage, 1),
                    'unit': 'MW',
                    'valueDate': data.get('valueDate')
                }]
            }
            
        except requests.RequestException as e:
            _LOGGER.error(f"Request error for OKG: {e}")
        except Exception as e:
            _LOGGER.error(f"Unexpected error for OKG: {e}")
            return None