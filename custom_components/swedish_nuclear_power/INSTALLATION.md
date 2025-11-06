# Installation Guide

## Option 1: HACS Installation (Recommended)

1. **Install HACS** if you haven't already
2. **Add Repository:**
   - Go to HACS → Integrations
   - Click the three dots → "Custom repositories"
   - Repository: `peglah/swedish-nuclear-power`
   - Category: Integration
   - Click "Add"

3. **Install Integration:**
   - Go to HACS → Integrations
   - Find "Swedish Nuclear Power"
   - Click "Download"
   - Restart Home Assistant

4. **Configure:**
   - Go to Settings → Devices & Services
   - Click "+ Add Integration"
   - Search for "Swedish Nuclear Power"
   - Set update interval (default 60 seconds)

## Option 2: Manual Installation

1. **Download Files:**
   ```bash
   cd /config/custom_components/
   wget https://github.com/peglah/swedish-nuclear-power/archive/main.zip
   unzip main.zip
   mv swedish-nuclear-power-main swedish_nuclear_power
   rm main.zip
   ```

2. **Restart Home Assistant**

3. **Configure Integration:**
   - Settings → Devices & Services → Add Integration
   - Search for "Swedish Nuclear Power"

## Verification

After installation, you should see these sensors:
- `sensor.ringhals_r3_power`
- `sensor.ringhals_r4_power`
- `sensor.forsmark_f1_power`
- `sensor.forsmark_f2_power`
- `sensor.forsmark_f3_power`
- `sensor.okg_o3_power`
- `sensor.swedish_nuclear_power_total_power`

## Troubleshooting

If sensors don't appear:
1. Check Home Assistant logs for errors
2. Verify integration is installed in `/config/custom_components/swedish_nuclear_power/`
3. Restart Home Assistant
4. Try reconfiguring the integration
