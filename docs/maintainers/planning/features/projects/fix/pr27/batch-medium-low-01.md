# Fix Plan: PR #27 Batch MEDIUM LOW - Batch 01

**PR:** #27  
**Batch:** medium-low-01  
**Priority:** 🟡 MEDIUM  
**Effort:** 🟢 LOW / 🟡 MEDIUM  
**Status:** 🔴 Not Started  
**Created:** 2025-12-06  
**Issues:** 2 issues (1 unique issue + 1 duplicate, 1 additional issue)

---

## Issues in This Batch

| Issue   | Priority   | Impact   | Effort   | Description   |
| ------- | ---------- | -------- | -------- | ------------- |
| PR27-#1 | 🟡 MEDIUM | 🟡 MEDIUM | 🟢 LOW | Extract health URL construction to helper function |
| PR27-Overall #2 | 🟡 MEDIUM | 🟡 MEDIUM | 🟡 MEDIUM | Handle missing/invalid configured URL |

**Note:** PR27-Overall #1 is a duplicate of PR27-#1 (same issue mentioned twice), so only counted once.

---

## Overview

This batch contains 2 MEDIUM priority issues with LOW/MEDIUM effort. These issues improve error handler code quality by reducing duplication and adding defensive error handling.

**Estimated Time:** 1-2 hours  
**Files Affected:**
- `scripts/project_cli/error_handler.py` (both issues)

---

## Issue Details

### Issue PR27-#1: Extract Health URL Construction to Helper

**Location:** `scripts/project_cli/error_handler.py:59-64` (and similar in other handlers)  
**Sourcery Comment:** Comment #1  
**Priority:** 🟡 MEDIUM | **Impact:** 🟡 MEDIUM | **Effort:** 🟢 LOW

**Description:**
This `Config.get_instance()` + `get_api_url()` + `rstrip('/')` + `/health` sequence is now repeated in `_handle_connection_error`, `_handle_timeout_error`, and `_handle_generic_error`. Consider extracting a helper like `_get_health_url()` to avoid duplication, keep the URL format consistent if it changes, and keep the handlers focused on error-specific logic.

**Current Code:**
```python
def _handle_connection_error(error: requests.exceptions.ConnectionError, console: Console) -> None:
    """Handle connection refused/network errors."""
    config = Config.get_instance()
    config_url = config.get_api_url()
    
    # Construct health URL properly
    base = config_url.rstrip('/')
    health_url = f"{base}/health"
    # ... rest of handler

def _handle_timeout_error(error: requests.exceptions.Timeout, console: Console) -> None:
    """Handle timeout errors."""
    config = Config.get_instance()
    base_url = config.get_api_url()
    base = base_url.rstrip('/')
    health_url = f"{base}/health"
    # ... rest of handler

def _handle_generic_error(error: Exception, console: Console) -> None:
    """Handle generic/unexpected errors."""
    config = Config.get_instance()
    base_url = config.get_api_url()
    base = base_url.rstrip('/')
    health_url = f"{base}/health"
    # ... rest of handler
```

**Proposed Solution:**
```python
def _get_health_url() -> str:
    """
    Get the health check URL from configured API base URL.
    
    Returns:
        Health check URL (e.g., 'http://localhost:5000/api/health')
    """
    config = Config.get_instance()
    base_url = config.get_api_url()
    base = base_url.rstrip('/')
    return f"{base}/health"

def _handle_connection_error(error: requests.exceptions.ConnectionError, console: Console) -> None:
    """Handle connection refused/network errors."""
    health_url = _get_health_url()
    # ... rest of handler uses health_url

def _handle_timeout_error(error: requests.exceptions.Timeout, console: Console) -> None:
    """Handle timeout errors."""
    health_url = _get_health_url()
    # ... rest of handler uses health_url

def _handle_generic_error(error: Exception, console: Console) -> None:
    """Handle generic/unexpected errors."""
    health_url = _get_health_url()
    # ... rest of handler uses health_url
```

**Rationale:** Reduces code duplication, centralizes URL construction logic, and makes it easier to maintain if URL format changes.

---

### Issue PR27-Overall #2: Handle Missing/Invalid Configured URL

**Location:** `scripts/project_cli/error_handler.py` (all handlers using Config.get_api_url())  
**Sourcery Comment:** Overall Comment #2  
**Priority:** 🟡 MEDIUM | **Impact:** 🟡 MEDIUM | **Effort:** 🟡 MEDIUM

**Description:**
In the error handlers that use `Config.get_instance().get_api_url()`, it might be worth handling cases where the configured URL is missing or invalid (e.g., empty string) to avoid producing unusable `curl` commands like `curl /health` and to provide a clearer fallback message.

**Current Code:**
```python
def _handle_connection_error(error: requests.exceptions.ConnectionError, console: Console) -> None:
    """Handle connection refused/network errors."""
    config = Config.get_instance()
    config_url = config.get_api_url()
    
    # Construct health URL properly
    base = config_url.rstrip('/')
    health_url = f"{base}/health"
    
    message = "[bold red]Cannot connect to backend API[/bold red]\n\n"
    # ... includes curl command with health_url
```

**Proposed Solution:**
```python
def _get_health_url() -> str:
    """
    Get the health check URL from configured API base URL.
    
    Returns:
        Health check URL (e.g., 'http://localhost:5000/api/health')
        Returns default URL if configured URL is missing or invalid
    """
    config = Config.get_instance()
    base_url = config.get_api_url()
    
    # Validate URL
    if not base_url or not base_url.strip():
        # Fallback to default
        base_url = 'http://localhost:5000/api'
    
    base = base_url.rstrip('/')
    health_url = f"{base}/health"
    
    # Additional validation: ensure URL looks valid
    if not health_url.startswith('http://') and not health_url.startswith('https://'):
        # Fallback to default
        health_url = 'http://localhost:5000/api/health'
    
    return health_url

def _handle_connection_error(error: requests.exceptions.ConnectionError, console: Console) -> None:
    """Handle connection refused/network errors."""
    health_url = _get_health_url()
    
    message = "[bold red]Cannot connect to backend API[/bold red]\n\n"
    message += "The backend server appears to be offline or unreachable.\n\n"
    message += "[bold]To fix this:[/bold]\n"
    message += "1. Start the backend server:\n"
    message += "   [cyan]cd backend && python run.py[/cyan]\n\n"
    message += "2. Verify the server is running:\n"
    message += f"   [cyan]curl {health_url}[/cyan]\n\n"
    message += "3. Check your API URL configuration:\n"
    message += "   [cyan]proj config get api base_url[/cyan]\n"
    message += "   Or set it: [cyan]proj config set api base_url <your-url>[/cyan]"
    
    console.print(Panel(message, title="Connection Error", border_style="red"))
    console.print(f"\n[dim]Technical details: {error}[/dim]")
```

**Rationale:** Prevents edge case issues where invalid configuration produces unusable error messages. Provides fallback to default URL for better user experience.

---

## Implementation Steps

1. **Issue PR27-#1: Extract Health URL Helper**
   - [ ] Create `_get_health_url()` helper function in `error_handler.py`
   - [ ] Update `_handle_connection_error()` to use helper
   - [ ] Update `_handle_timeout_error()` to use helper
   - [ ] Update `_handle_generic_error()` to use helper
   - [ ] Test all error handlers still work correctly
   - [ ] Verify health URL construction is consistent

2. **Issue PR27-Overall #2: Handle Missing/Invalid URL**
   - [ ] Add URL validation to `_get_health_url()` helper
   - [ ] Check for empty/missing URL
   - [ ] Check for invalid URL format (must start with http:// or https://)
   - [ ] Provide fallback to default URL
   - [ ] Test with empty URL configuration
   - [ ] Test with invalid URL format
   - [ ] Verify error messages are still helpful

---

## Testing

- [ ] All existing tests pass
- [ ] Test error handlers with default URL
- [ ] Test error handlers with custom URL
- [ ] Test error handlers with empty URL (should use default)
- [ ] Test error handlers with invalid URL format (should use default)
- [ ] Verify health URL construction is consistent across all handlers
- [ ] Manual testing: Error messages show correct URLs
- [ ] No regressions introduced

---

## Files to Modify

- `scripts/project_cli/error_handler.py` - Extract helper function and add URL validation (both issues)

---

## Definition of Done

- [ ] All 2 issues in batch fixed
- [ ] Health URL helper function extracted
- [ ] URL validation added with fallback
- [ ] All error handlers updated to use helper
- [ ] Tests passing
- [ ] Code reviewed
- [ ] Manual testing completed
- [ ] No regressions introduced
- [ ] Ready for PR

---

**Batch Rationale:**
These issues are batched together because they:

- Both relate to error handler improvements
- Share the same file (`error_handler.py`)
- Can be implemented together efficiently
- Improve code quality and maintainability
- Are MEDIUM priority improvements (not urgent but valuable)

