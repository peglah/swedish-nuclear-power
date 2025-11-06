# Swedish Nuclear Power Integration

**This integration is already installed via HACS.** For full documentation, visit the [repository](https://github.com/peglah/swedish-nuclear-power).

## 🏠 Created Sensors

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

## ⚙️ Configuration

- **Update Interval:** Settings → Devices & Services → Swedish Nuclear Power → Options
- **Default:** 60 seconds (30-3600 seconds range)

## 🔧 Troubleshooting

### Manual Data Refresh:
1. Developer Tools → Services
2. Call `homeassistant.update_entity` with sensor entity ID

### Common Issues:
- **No data:** Check network connectivity to Swedish plant websites
- **Missing sensors:** Restart Home Assistant

## 📄 License

MIT License - see LICENSE file for details.