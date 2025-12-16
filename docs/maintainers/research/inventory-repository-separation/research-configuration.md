# Research: Configuration Management

**Research Topic:** Inventory Repository Separation  
**Question:** How should configuration be managed in the new repository?  
**Status:** ✅ Complete  
**Created:** 2025-12-16  
**Last Updated:** 2025-12-16

---

## 🎯 Research Question

How should configuration be managed to remove hardcoded paths and make the tool portable across machines?

---

## 🔍 Research Goals

- [x] Goal 1: Evaluate configuration file formats (YAML/JSON/TOML)
- [x] Goal 2: Determine config file location pattern
- [x] Goal 3: Design environment variable overrides
- [x] Goal 4: Create minimal config schema

---

## 📚 Research Methodology

**Sources:**
- [x] XDG Base Directory Specification
- [x] Python configuration patterns (pydantic, configparser)
- [x] 12-factor app methodology
- [x] Existing work-prod config patterns
- [x] Web search: Python CLI configuration

---

## 📊 Findings

### Finding 1: Current Hardcoded Paths Problem

**Description:** Current scripts have hardcoded paths like:

```python
# analyze-tech-stack.py
PROJECT_DIRS = [
    "/Users/cdwilson/Projects",
    "/Users/cdwilson/Learning"
]

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")  # This one is okay
```

**Issues:**
- Won't work on other machines
- Can't easily change scan directories
- Mixed patterns (env var + hardcoded)

**Source:** Current script analysis

**Relevance:** This is the biggest technical debt blocking portability.

---

### Finding 2: XDG Base Directory Standard

**Description:** The XDG standard defines where config files should go:

```
~/.config/[app-name]/config.yaml   # Config files
~/.local/share/[app-name]/         # Data files
~/.cache/[app-name]/               # Cache files
```

**Benefits:**
- Industry standard for Unix tools
- Users expect this location
- Easy to backup/sync configs

**Source:** XDG Base Directory Specification

**Relevance:** Recommended pattern for config location.

---

### Finding 3: YAML vs JSON vs TOML

| Format | Pros | Cons |
|--------|------|------|
| **YAML** | Human-readable, comments | Indentation sensitive |
| **JSON** | Universal, no comments | Verbose |
| **TOML** | Clean, comments | Less familiar |

**Recommendation:** YAML for human-edited config, JSON for data files

**Source:** Format comparison

**Relevance:** YAML is best for user-edited configuration.

---

### Finding 4: Pydantic for Type-Safe Config

**Description:** Using Pydantic for configuration provides:
- Type validation
- Default values
- Environment variable loading
- Clear error messages

```python
from pydantic import BaseSettings, Field
from pathlib import Path

class Settings(BaseSettings):
    scan_dirs: list[Path] = Field(
        default=[Path.home() / "Projects"],
        description="Directories to scan for projects"
    )
    github_token: str | None = Field(
        default=None,
        env="GITHUB_TOKEN"
    )
    github_username: str = Field(
        default="",
        description="GitHub username for API"
    )
    output_dir: Path = Field(
        default=Path.home() / ".local/share/pinv",
        description="Output directory for data files"
    )
    
    class Config:
        env_prefix = "PINV_"
        env_file = ".env"
```

**Source:** Pydantic documentation

**Relevance:** Type-safe config with env var support.

---

### Finding 5: Environment Variable Overrides

**Description:** All config should be overridable via environment variables following pattern:

```bash
export PINV_SCAN_DIRS="/path/one:/path/two"
export PINV_GITHUB_TOKEN="ghp_..."
export PINV_OUTPUT_DIR="/custom/output"
```

**Benefits:**
- CI/CD friendly
- Docker friendly
- No file needed for simple cases

**Source:** 12-factor app methodology

**Relevance:** Essential for automation.

---

## 🔍 Analysis

### Proposed Configuration Schema

```yaml
# ~/.config/pinv/config.yaml

# Directories to scan for local projects
scan_dirs:
  - ~/Projects
  - ~/Learning

# GitHub settings
github:
  username: grimm00
  # token loaded from GITHUB_TOKEN or PINV_GITHUB_TOKEN env var

# Output settings
output:
  dir: ~/.local/share/pinv
  format: json

# Work-prod integration
work_prod:
  api_url: http://localhost:5000
  # Or: https://work-prod.example.com/api

# Filters (optional)
filters:
  exclude_dirs:
    - node_modules
    - venv
    - .git
  min_file_count: 1
```

### Config Loading Priority

1. **Command-line arguments** (highest priority)
2. **Environment variables** (PINV_* prefix)
3. **Config file** (~/.config/pinv/config.yaml)
4. **Default values** (lowest priority)

### Config File Creation

On first run, if no config exists:
```bash
$ pinv scan local
No configuration found. Creating default config at ~/.config/pinv/config.yaml
Edit this file to customize scan directories.
```

---

## 💡 Recommendations

### Primary Recommendation

1. **Use YAML** for human-edited config
2. **Store at** `~/.config/pinv/config.yaml` (XDG standard)
3. **Use Pydantic** for type-safe config loading
4. **Support env vars** with `PINV_` prefix
5. **Create defaults** on first run

### Implementation Approach

```python
# pinv/config.py
from pathlib import Path
from pydantic_settings import BaseSettings

CONFIG_DIR = Path.home() / ".config" / "pinv"
DATA_DIR = Path.home() / ".local" / "share" / "pinv"

class Settings(BaseSettings):
    scan_dirs: list[Path] = [Path.home() / "Projects"]
    github_token: str | None = None
    github_username: str = ""
    output_dir: Path = DATA_DIR
    work_prod_api_url: str = "http://localhost:5000"
    
    class Config:
        env_prefix = "PINV_"

def load_config() -> Settings:
    config_file = CONFIG_DIR / "config.yaml"
    if config_file.exists():
        # Load from YAML
        ...
    return Settings()
```

---

## 📋 Requirements Discovered

- [x] REQ-10: Config stored at `~/.config/pinv/config.yaml`
- [x] REQ-11: All config overridable via `PINV_*` env vars
- [x] REQ-12: YAML format for human-edited config
- [x] REQ-13: Use Pydantic for type-safe config loading
- [x] REQ-14: Create default config on first run
- [x] REQ-15: Command-line args override config file

---

## 🎯 Decision Recommendation

**Decision:** ✅ YAML config with Pydantic validation

**Config Location:** `~/.config/pinv/config.yaml`  
**Data Location:** `~/.local/share/pinv/`  
**Env Prefix:** `PINV_`

**Dependencies to add:**
- `pyyaml` (YAML parsing)
- `pydantic-settings` (config management)

---

**Last Updated:** 2025-12-16

