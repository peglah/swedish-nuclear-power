# Swedish Nuclear Power - Home Assistant Integration

A Home Assistant custom integration that monitors real-time power output from all Swedish nuclear power plants: Ringhals, Forsmark, and Oskarshamn.

## 🏭 Monitored Reactors

**Ringhals:**
- R3 (1,074 MW)
- R4 (1,130 MW)

**Forsmark:**
- F1 (1,014 MW)
- F2 (1,121 MW) 
- F3 (1,172 MW)

**Oskarshamn:**
- O3 (1,450 MW)

## ✨ Features

- 📊 **Real-time monitoring** of all Swedish nuclear reactors
- 🏠 **Native Home Assistant integration** with proper sensors
- ⚡ **Automatic updates** (configurable interval)
- 📈 **Total power calculation** for entire Swedish nuclear fleet
- 🔄 **Timestamp tracking** for accurate measurement times
- 📱 **Dashboard-ready** sensors with proper icons and units
- 🎛️ **Configurable** via UI (no YAML required)

## 🚀 Installation via HACS

1. **Add Custom Repository:**
   - Go to HACS → Integrations
   - Click Menu (⋮) → Custom repositories
   - Add repository URL: `https://github.com/peglah/swedish-nuclear-power`
   - Category: Integration
   - Click Add

2. **Install Integration:**
   - Go to HACS → Integrations
   - Find "Swedish Nuclear Power" and click Download
   - Restart Home Assistant

3. **Configure Integration:**
   - Go to Settings → Devices & Services
   - Click "+ Add Integration"
   - Search for "Swedish Nuclear Power"
   - Configure update interval (default: 60 seconds)

## 📁 Manual Installation

1. **Download Files:**
   ```bash
   cd /config/custom_components/
   git clone https://github.com/peglah/swedish-nuclear-power.git swedish_nuclear_power
   ```

2. **Restart Home Assistant**

3. **Configure Integration:**
   - Go to Settings → Devices & Services → Add Integration
   - Search for "Swedish Nuclear Power"

## 🏠 Created Sensors

The integration creates the following sensors:

### Individual Reactor Power Sensors:
- `sensor.ringhals_r3_power` - Ringhals R3 output (MW)
- `sensor.ringhals_r4_power` - Ringhals R4 output (MW)
- `sensor.forsmark_f1_power` - Forsmark F1 output (MW)
- `sensor.forsmark_f2_power` - Forsmark F2 output (MW)
- `sensor.forsmark_f3_power` - Forsmark F3 output (MW)
- `sensor.okg_o3_power` - Oskarshamn O3 output (MW)

### Plant Update Timestamps:
- `sensor.ringhals_last_update` - Ringhals last measurement time
- `sensor.forsmark_last_update` - Forsmark last measurement time
- `sensor.okg_last_update` - Oskarshamn last measurement time

### Total Power:
- `sensor.swedish_nuclear_power_total_power` - Total Swedish nuclear output (MW)

## 📊 Dashboard Example

Add this to your Lovelace dashboard:

```yaml
type: entities
title: Swedish Nuclear Power Plants
entities:
  - entity: sensor.ringhals_r3_power
    name: Ringhals R3
  - entity: sensor.ringhals_r4_power
    name: Ringhals R4
  - entity: sensor.forsmark_f1_power
    name: Forsmark F1
  - entity: sensor.forsmark_f2_power
    name: Forsmark F2
  - entity: sensor.forsmark_f3_power
    name: Forsmark F3
  - entity: sensor.okg_o3_power
    name: Oskarshamn O3
  - type: divider
  - entity: sensor.swedish_nuclear_power_total_power
    name: Total Nuclear Power
    icon: mdi:reactor
```

## 🤖 Automation Examples

### Low Power Alert:
```yaml
alias: Nuclear Power Low Alert
trigger:
  - platform: numeric_state
    entity_id: sensor.swedish_nuclear_power_total_power
    below: 3000
action:
  - service: notify.mobile_app
    data:
      title: "Low Nuclear Power Output"
      message: "Total Swedish nuclear power is below 3000 MW"
```

### Reactor Status Change:
```yaml
alias: Reactor Status Change
trigger:
  - platform: state
    entity_id: sensor.forsmark_f1_power
    from: "0"
    to: "100"
action:
  - service: notify.mobile_app
    data:
      title: "Forsmark F1 Started"
      message: "Forsmark F1 reactor has started producing power"
```

## ⚙️ Configuration

### Update Interval
- **Default:** 60 seconds
- **Range:** 30-3600 seconds
- **Location:** Settings → Devices & Services → Swedish Nuclear Power → Options

### Data Sources
- **Ringhals & Forsmark:** Vattenfall production pages (scraped)
- **Oskarshamn:** OKG API (direct API call)

## 🔧 Testing

### Test Integration:
```bash
python3 test_standalone.py
```

This will test data fetching from all plants without requiring Home Assistant.

## 🔧 Troubleshooting

### Check Integration Status:
```yaml
# Developer Tools → Services
service: homeassistant.update_entity
entity_id: sensor.swedish_nuclear_power_total_power
```

### View Logs:
```bash
# Home Assistant logs
grep "swedish_nuclear_power" /config/home-assistant.log
```

### Manual Data Refresh:
1. Go to Developer Tools → Services
2. Call `homeassistant.update_entity` with sensor entity ID

### Common Issues:
- **No data:** Check network connectivity to Swedish plant websites
- **Stale data:** Verify update interval is appropriate
- **Missing sensors:** Restart Home Assistant after installation

## 📈 Data Accuracy

- **Ringhals & Forsmark:** Data scraped from Vattenfall's official production pages
- **Oskarshamn:** Data from OKG's official API
- **Timestamps:** Reflect actual measurement time, not scraping time
- **Units:** All power measurements in Megawatts (MW)
- **Percentages:** Available for Ringhals & Forsmark, not available for O3

## 📁 Project Structure

```
swedish_nuclear_power/
├── __init__.py              # Main integration setup
├── manifest.json             # Integration metadata
├── const.py                 # Constants and plant configs
├── config_flow.py           # UI configuration flow
├── coordinator.py           # Data fetching coordinator
├── sensor.py                # Sensor entities
├── options.py               # Configuration options
├── translations/en.json      # UI translations
├── README.md                # Integration documentation
├── LICENSE                  # MIT License
└── INSTALLATION.md          # Installation guide
```

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details.

## 🔗 Data Sources

- **Ringhals:** https://karnkraft.vattenfall.se/ringhals/produktion
- **Forsmark:** https://karnkraft.vattenfall.se/forsmark/produktion  
- **Oskarshamn:** https://okg.se/.netlify/functions/getReactorOutput

## 📞 Support

- **Issues:** GitHub Issues
- **Discussions:** GitHub Discussions
- **Home Assistant:** Community Forums