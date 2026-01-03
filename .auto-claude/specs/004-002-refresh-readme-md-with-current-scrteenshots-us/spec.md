# Quick Spec: Refresh README Screenshots

## Overview
Copy new screenshots from `.playwright-mcp/` to `docs/screenshots/` and update README.md to include them, then merge and push.

## Workflow Type
feature

## Task Scope
### Files to Modify
- `README.md` - Add references to new screenshots
- `docs/screenshots/` - Copy new screenshot files

### Change Details
Two new screenshots exist in `.playwright-mcp/` that need to be added:
- `dashboard-with-domains.png` - Shows the dashboard with domain graphs
- `space-domain.png` - Shows the space domain visualization

### Steps
1. Copy `dashboard-with-domains.png` and `space-domain.png` to `docs/screenshots/`
2. Add new screenshot sections to README.md after the existing "Parent Dashboard" section
3. Commit, merge to main, and push

## Success Criteria
- [ ] New screenshots exist in `docs/screenshots/`
- [ ] README.md references new screenshots
- [ ] Images render correctly in README
- [ ] Changes pushed to remote

## Notes
- Existing screenshots (login-page.png, dashboard.png, device-emulator.png) are already in sync - no update needed
