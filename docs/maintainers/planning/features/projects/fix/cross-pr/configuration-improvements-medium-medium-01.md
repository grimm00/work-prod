# Fix Plan: Cross-PR Batch Configuration Improvements

**Batch:** configuration-improvements-medium-medium-01  
**Priority:** 🟡 MEDIUM  
**Effort:** 🟡 MEDIUM  
**Status:** 🔴 Not Started  
**Created:** 2025-12-06  
**Source:** fix-review-report-2025-12-06.md  
**Issues:** 3 issues from 1 PR

---

## Issues in This Batch

| Issue | PR | Priority | Impact | Effort | Description |
|-------|----|----------|--------|--------|-------------|
| PR24-#2 | #24 | 🟡 MEDIUM | 🟡 MEDIUM | 🟡 MEDIUM | Use configured API base URL in error messages |
| PR24-Overall #1 | #24 | 🟡 MEDIUM | 🟡 MEDIUM | 🟡 MEDIUM | Config defaults visibility - Consider merging DEFAULT_CONFIG into get_all() output |
| PR24-Overall #2 | #24 | 🟡 MEDIUM | 🟡 MEDIUM | 🟡 MEDIUM | Hardcoded URLs - Use Config.get_api_url() in error messages |

---

## Overview

This batch contains 3 configuration-related improvements from PR #24. These issues improve user experience by making error messages and configuration display more accurate and helpful.

**Estimated Time:** 2-3 hours  
**Files Affected:**
- `scripts/project_cli/config.py` (PR24-Overall #1)
- `scripts/project_cli/error_handler.py` (PR24-#2, Overall #2)

**Source PRs:**
- PR #24: CLI Enhancement & Daily Use Tools (3 issues)

---

## Issue Details

### Issue PR24-#2: Use Configured API Base URL in Error Messages

**Source PR:** #24 - CLI Enhancement & Daily Use Tools  
**Location:** `scripts/project_cli/error_handler.py:58-67`  
**Sourcery Comment:** Comment #2  
**Priority:** 🟡 MEDIUM | **Impact:** 🟡 MEDIUM | **Effort:** 🟡 MEDIUM

**Description:**
These hints always point to `http://localhost:5000/api`, which may be wrong when `api.base_url` is configured differently. Consider reading the base URL from `Config` (e.g. `Config.get_instance().get_api_url()`) and deriving the health endpoint from that so the suggested commands reflect the actual configuration, even if that means importing `Config` here.

**Current Code:**
```python
def _handle_connection_error(error: requests.exceptions.ConnectionError, console: Console) -> None:
    """Handle connection refused/network errors."""
    config_url = "http://localhost:5000/api"
    
    message = "[bold red]Cannot connect to backend API[/bold red]\n"
    message += "The backend server appears to be offline or unreachable.\n"
    message += "[bold]To fix this:[/bold]\n"
    message += "1. Start the backend server:\n"
    message += "   [cyan]cd backend && python run.py[/cyan]\n"
    message += "2. Verify the server is running:\n"
    message += f"   [cyan]curl {config_url.replace('/api', '/api/health')}[/cyan]\n"
    message += "3. Check your API URL configuration:\n"
    message += "   [cyan]proj config get api base_url[/cyan]\n"
    message += "   Or set it: [cyan]proj config set api base_url <your-url>[/cyan]"
```

**Proposed Solution:**
```python
from ..config import Config

def _handle_connection_error(error: requests.exceptions.ConnectionError, console: Console) -> None:
    """Handle connection refused/network errors."""
    config = Config.get_instance()
    config_url = config.get_api_url()
    
    # Construct health URL properly
    base = config_url.rstrip('/')
    health_url = f"{base}/health"
    
    message = "[bold red]Cannot connect to backend API[/bold red]\n"
    message += "The backend server appears to be offline or unreachable.\n"
    message += "[bold]To fix this:[/bold]\n"
    message += "1. Start the backend server:\n"
    message += "   [cyan]cd backend && python run.py[/cyan]\n"
    message += "2. Verify the server is running:\n"
    message += f"   [cyan]curl {health_url}[/cyan]\n"
    message += "3. Check your API URL configuration:\n"
    message += "   [cyan]proj config get api base_url[/cyan]\n"
    message += "   Or set it: [cyan]proj config set api base_url <your-url>[/cyan]"
```

**Rationale:** Error messages will show the actual configured URL, making troubleshooting more accurate.

---

### Issue PR24-Overall #1: Config Defaults Visibility

**Source PR:** #24 - CLI Enhancement & Daily Use Tools  
**Location:** `scripts/project_cli/config.py` (get_all method)  
**Sourcery Comment:** Overall Comment #1  
**Priority:** 🟡 MEDIUM | **Impact:** 🟡 MEDIUM | **Effort:** 🟡 MEDIUM

**Description:**
The new `Config` singleton only exposes values that exist in the parsed `ConfigParser`, so `get_all()`/`proj config show` will omit default values that were never persisted to `~/.projrc`; consider merging `DEFAULT_CONFIG` into the returned dict so users can see effective defaults as well as overrides.

**Current Code:**
```python
def get_all(self):
    """Get all configuration as a dictionary."""
    result = {}
    for section in self.config.sections():
        result[section] = dict(self.config.items(section))
    return result
```

**Proposed Solution:**
```python
def get_all(self):
    """Get all configuration as a dictionary, including defaults."""
    result = {}
    # Start with defaults
    for section, options in self.DEFAULT_CONFIG.items():
        result[section] = options.copy()
    
    # Override with actual config values
    for section in self.config.sections():
        if section not in result:
            result[section] = {}
        for key, value in self.config.items(section):
            result[section][key] = value
    
    return result
```

**Rationale:** Users can see all effective configuration values, not just overrides. Makes `proj config show` more useful.

---

### Issue PR24-Overall #2: Hardcoded URLs in Error Messages

**Source PR:** #24 - CLI Enhancement & Daily Use Tools  
**Location:** `scripts/project_cli/error_handler.py` (multiple functions)  
**Sourcery Comment:** Overall Comment #2  
**Priority:** 🟡 MEDIUM | **Impact:** 🟡 MEDIUM | **Effort:** 🟡 MEDIUM

**Description:**
In `error_handler._handle_connection_error` and related messaging you hard-code `http://localhost:5000/api` and its health URL, which can drift from the actual configured base URL; using `Config.get_instance().get_api_url()` (or passing the URL in) would keep troubleshooting instructions accurate.

**Current Code:**
```python
def _handle_timeout_error(error: requests.exceptions.Timeout, console: Console) -> None:
    """Handle timeout errors."""
    message = "[bold red]Request timed out[/bold red]\n"
    message += "The backend server took too long to respond.\n"
    message += "[bold]Possible causes:[/bold]\n"
    message += "• Backend server is overloaded\n"
    message += "• Network connectivity issues\n"
    message += "• Backend server may be unresponsive\n"
    message += "[bold]Try:[/bold]\n"
    message += "• Check if backend is running: [cyan]curl http://localhost:5000/api/health[/cyan]\n"
    message += "• Restart the backend server"
```

**Proposed Solution:**
```python
from ..config import Config

def _handle_timeout_error(error: requests.exceptions.Timeout, console: Console) -> None:
    """Handle timeout errors."""
    config = Config.get_instance()
    base_url = config.get_api_url()
    base = base_url.rstrip('/')
    health_url = f"{base}/health"
    
    message = "[bold red]Request timed out[/bold red]\n"
    message += "The backend server took too long to respond.\n"
    message += "[bold]Possible causes:[/bold]\n"
    message += "• Backend server is overloaded\n"
    message += "• Network connectivity issues\n"
    message += "• Backend server may be unresponsive\n"
    message += "[bold]Try:[/bold]\n"
    message += f"• Check if backend is running: [cyan]curl {health_url}[/cyan]\n"
    message += "• Restart the backend server"
```

**Rationale:** Error messages show actual configured URLs, improving troubleshooting accuracy.

---

## Implementation Steps

1. **Issue PR24-#2: Use Configured URL in Connection Error**
   - [ ] Import `Config` in `error_handler.py`
   - [ ] Update `_handle_connection_error()` to use `Config.get_instance().get_api_url()`
   - [ ] Construct health URL properly
   - [ ] Test with different base URLs

2. **Issue PR24-Overall #1: Config Defaults Visibility**
   - [ ] Update `get_all()` method to merge DEFAULT_CONFIG
   - [ ] Ensure user overrides take precedence
   - [ ] Test `proj config show` displays all values
   - [ ] Verify defaults are shown correctly

3. **Issue PR24-Overall #2: Hardcoded URLs in Error Messages**
   - [ ] Update `_handle_timeout_error()` to use configured URL
   - [ ] Update any other error handlers with hardcoded URLs
   - [ ] Test with different base URLs
   - [ ] Verify error messages show correct URLs

---

## Testing

- [ ] All existing tests pass
- [ ] Test `proj config show` shows defaults and overrides
- [ ] Test error messages with custom base URLs
- [ ] Test health URL construction with various base URL formats
- [ ] Manual testing: Error messages show correct URLs
- [ ] No regressions introduced

---

## Files to Modify

- `scripts/project_cli/config.py` - Update `get_all()` to include defaults (PR24-Overall #1)
- `scripts/project_cli/error_handler.py` - Use configured URLs in error messages (PR24-#2, Overall #2)

---

## Definition of Done

- [ ] All 3 issues in batch fixed
- [ ] Tests passing
- [ ] Code reviewed
- [ ] Manual testing completed
- [ ] Error messages show configured URLs
- [ ] Config show displays defaults
- [ ] No regressions introduced
- [ ] Ready for PR

---

**Batch Rationale:**
These issues are batched together because they:

- All relate to configuration and URL handling
- Improve user experience and troubleshooting
- Share similar implementation approach (using Config singleton)
- Are MEDIUM priority improvements (not urgent but valuable)

