# Fix: Production Logging Configuration

**Sourcery Issue:** PR #1, Comment #1  
**Location:** `backend/config.py:69-71`  
**Priority:** 🟠 HIGH | **Impact:** 🟡 MEDIUM | **Effort:** 🟢 LOW

## Problem

`ProductionConfig.init_app()` adds a new `StreamHandler` each time `create_app()` runs, causing:
1. Duplicate log entries in reloading environments
2. Unformatted logs (no timestamp, level, or structured format)

## Solution

1. Check if handler already exists before adding
2. Add proper formatter with timestamp, level, message
3. Consider using Flask's built-in logging config

## Implementation

**File:** `backend/config.py`

```python
@staticmethod
def init_app(app):
    """Initialize production-specific configuration."""
    # Only add handler if not already present
    if not app.logger.handlers:
        import logging
        from logging import StreamHandler
        
        handler = StreamHandler()
        handler.setLevel(logging.INFO)
        
        # Add formatter
        formatter = logging.Formatter(
            '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
        )
        handler.setFormatter(formatter)
        
        app.logger.addHandler(handler)
        app.logger.setLevel(logging.INFO)
```

## Testing

1. Restart Flask server multiple times
2. Verify no duplicate log entries
3. Verify logs include timestamp and level
4. Test in production-like environment

## ADRs

No ADR needed - implementation detail fix.

