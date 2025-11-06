# Git Setup Instructions for GitHub

## 🚀 Repository Setup

### 1. Initialize Git Repository
```bash
# Navigate to your project directory
cd /home/peglah/opencode-projects/swedish-nuclear-power

# Initialize git repository
git init
```

### 2. Create .gitignore File
```bash
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Home Assistant specific
*.log
home-assistant.log
EOF
```

### 3. Add All Files
```bash
git add .
```

### 4. Initial Commit
```bash
git commit -m "Initial release - Swedish Nuclear Power Home Assistant integration

Features:
- Real-time monitoring of all Swedish nuclear reactors
- Support for Ringhals (R3, R4), Forsmark (F1, F2, F3), and Oskarshamn (O3)
- HACS-compatible integration with proper sensors
- Automatic percentage calculations and total power tracking
- Configurable update intervals via UI"
```

### 5. Add GitHub Remote
```bash
git remote add origin https://github.com/peglah/swedish-nuclear-power.git
```

### 6. Push to GitHub
```bash
# Push to main branch
git push -u origin main
```

## 📋 Repository Structure After Push

Your GitHub repository will have this structure:
```
swedish-nuclear-power/
├── swedish_nuclear_power/           # Integration folder
│   ├── __init__.py
│   ├── manifest.json
│   ├── const.py
│   ├── config_flow.py
│   ├── coordinator.py
│   ├── sensor.py
│   ├── options.py
│   ├── translations/
│   │   └── en.json
│   ├── README.md
│   ├── INSTALLATION.md
│   └── LICENSE
├── README.md                        # Repository README
├── test_standalone.py               # Test script
└── .gitignore                       # Git ignore file
```

## 🏷️ Repository Settings (Optional)

### Repository Description:
```
Swedish Nuclear Power - Home Assistant Integration
```

### Repository Topics:
```
home-assistant, hacs, integration, nuclear-power, sweden, energy-monitoring
```

### Repository Website:
```
https://www.home-assistant.io/
```

## 📖 User Installation Instructions

After you push to GitHub, users will install it by:

1. **In HACS:**
   - HACS → Integrations → Menu (⋮) → Custom repositories
   - Add: `https://github.com/peglah/swedish-nuclear-power`
   - Category: Integration

2. **Install and restart Home Assistant**

3. **Add integration via UI**

## 🔄 Updating the Integration

When you make changes:
```bash
git add .
git commit -m "Update: description of changes"
git push origin main
```

Users will then see the update in HACS and can download it.

## ✅ Pre-Push Checklist

- [ ] All markdown files updated with GitHub URLs
- [ ] Integration tested with `python3 test_standalone.py`
- [ ] No sensitive information in files
- [ ] LICENSE file present
- [ ] README.md is comprehensive
- [ ] .gitignore created

## 🎯 Next Steps

1. Create repository on GitHub first
2. Run the commands above
3. Test installation in a development HA instance
4. Share repository URL with users