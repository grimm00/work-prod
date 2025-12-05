# Fix Plan: PR #2 Issue #3 - CLI Import Ambiguity

**PR:** #2  
**Sourcery Comment:** #3  
**Status:** ✅ Complete  
**Created:** 2025-12-03  
**Completed:** 2025-12-05  
**Fixed:** ✅ Fixed

---

## Priority Assessment

- **Priority:** 🟠 HIGH
- **Impact:** 🟠 HIGH
- **Effort:** 🟢 LOW

---

## Problem Description

### What's Wrong

The CLI package uses absolute imports that could pick up wrong modules:

**Current Code** (in `scripts/project_cli/api_client.py`):
```python
from config import Config
```

**Current Code** (in `scripts/project_cli/commands/*.py`):
```python
from api_client import APIClient
```

**Problem:**
- Absolute imports depend on PYTHONPATH
- Could import wrong `config` module if one exists elsewhere
- Not resilient to different execution contexts
- May fail when run as `python -m` or from tests

### Sourcery Feedback

"In this package, `from config import Config` might pick up a different `config` module on `PYTHONPATH` depending on how the CLI is invoked. Use an explicit relative import (`from .config import Config`) so it always loads the local module."

---

## Solution Approach

### Use Package-Relative Imports

Convert all intra-package imports to relative imports:

**api_client.py:**
```python
# Before:
from config import Config

# After:
from .config import Config
```

**commands/*.py:**
```python
# Before:
from api_client import APIClient

# After:
from ..api_client import APIClient
```

---

## Implementation Steps

### 1. Fix `api_client.py`

```python
"""
API client for communicating with the backend.
"""

import requests
from typing import List, Dict, Optional
from .config import Config  # Relative import


class APIClient:
    ...
```

### 2. Fix `commands/list_cmd.py`

```python
"""
List command implementation.
"""

import click
from rich.console import Console
from rich.table import Table
from ..api_client import APIClient  # Relative import
```

### 3. Fix `commands/get_cmd.py`

```python
"""
Get command implementation.
"""

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from ..api_client import APIClient  # Relative import
```

### 4. Fix `commands/create_cmd.py`

```python
"""
Create command implementation.
"""

import click
from rich.console import Console
from rich.table import Table
from ..api_client import APIClient  # Relative import
```

### 5. Fix `commands/update_cmd.py`

```python
"""
Update command implementation.
"""

import click
from rich.console import Console
from rich.table import Table
from ..api_client import APIClient  # Relative import
```

---

## Testing Requirements

### Test Different Execution Contexts

1. **From project root:**
   ```bash
   ./scripts/project_cli/proj list
   ```

2. **From scripts directory:**
   ```bash
   cd scripts
   ./project_cli/proj list
   ```

3. **As module:**
   ```bash
   python -m scripts.project_cli.proj list
   ```

4. **With modified PYTHONPATH:**
   ```bash
   PYTHONPATH=/some/other/path ./scripts/project_cli/proj list
   ```

### Expected Results

- All execution methods should work
- Should always import from local package
- No import errors
- No wrong module loaded

### Automated Test

Add to `backend/tests/test_cli_imports.py`:
```python
def test_cli_uses_local_config():
    """Test that CLI imports its own config module."""
    from scripts.project_cli import api_client
    from scripts.project_cli import config
    
    # Verify api_client uses local config
    assert api_client.Config is config.Config
```

---

## Files to Change

1. `scripts/project_cli/api_client.py` - Line 9
2. `scripts/project_cli/commands/list_cmd.py` - Line 10
3. `scripts/project_cli/commands/get_cmd.py` - Line 10  
4. `scripts/project_cli/commands/create_cmd.py` - Line 7
5. `scripts/project_cli/commands/update_cmd.py` - Line 7

**Total:** 5 files, 5 lines changed

---

## Related ADRs

None - This is a Python packaging best practice

---

## Merge Strategy

**Branch:** `feat/phase-2-create-update` (fix in Phase 2 branch)  
**Reason:** Phase 2 added create/update commands that also have this issue  
**Alternative:** Separate fix PR, then rebase Phase 2

---

## Notes

This is a best practice issue that could cause subtle bugs depending on execution context. While it may work fine in our current setup, relative imports make the package more robust and portable.

---

**Created:** 2025-12-03  
**Priority:** 🟠 HIGH  
**Status:** 🔴 Not Fixed  
**Include in:** Phase 2 PR or separate fix PR

