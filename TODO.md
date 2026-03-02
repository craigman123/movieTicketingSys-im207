# Project Fix Plan

## Issues Identified:

### 1. Backend-Frontend Mismatch
- Frontend templates are for Movie Ticketing System
- Backend (main.py) is for Prison/Inmate Management System
- Need to decide which one to keep

### 2. Code Bugs in main.py:
- [ ] Duplicate class definition: `Movies` defined twice (lines 26-47 and 49-62)
- [ ] First class should be `Inmate` not `Movies`
- [ ] Second class should remain `InmateRecord` (already correct)
- [ ] User model missing required fields: `badge`, `approved`, `email`, `system_access`

### 3. Route-Template Mismatches:
- [ ] Login: template has username/email/password, route expects username/password/badge
- [ ] Register: template has first/last/email/password, route expects last/first/email/password

## Proposed Fix Options:

### Option A: Fix Prison/Inmate Management System
- Update templates to match prison management system
- Fix all model definitions and routes

### Option B: Fix Movie Ticketing System  
- Rewrite backend to match the existing movie templates
- Keep the frontend as-is for movie booking

### Option C: Fix Both Independently
- Fix bugs to make code runnable
- Keep both systems functional separately
