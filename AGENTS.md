# AGENTS.md - Development Guidelines

## Build/Test Commands
```bash
# Run integration test suite
python3 test_standalone.py

# Test specific plant data fetching
python3 -c "from test_standalone import NuclearDataFetcher; f=NuclearDataFetcher(); print(f._fetch_vattenfall_data('ringhals', PLANTS['ringhals']))"
```

## Code Style Guidelines
- Use `from __future__ import annotations` in all Python files
- Follow Home Assistant integration patterns strictly
- Type hints required: `Dict[str, Any]`, `Optional[str]`, etc.
- Import order: stdlib → third-party → Home Assistant → local imports
- Use async/await for network operations, wrap sync calls in executor
- Error handling: log warnings for failed plant fetches, continue processing
- Naming: `snake_case` for functions/variables, `PascalCase` for classes
- Constants in `const.py`, plant configs as Dict[str, Dict[str, Any]>
- Use f-strings for string formatting, never % formatting
- Session management: reuse requests.Session with proper headers
- Data validation: check for None values before accessing dict keys
- Fix syntax errors: ensure proper bracket matching in dict structures