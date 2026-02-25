# AGENTS.md - Development Guidelines for Newton

## Overview

Newton is a Python/Gtk3 desktop application (code editor) using PyGObject. The project follows specific conventions documented below.

---

## Build, Lint, and Test Commands

### Running the Application

```bash
# Activate virtual environment and run
source .venv/bin/activate
python -m src
```

### Type Checking (Pyright)

The project uses pyright for static type checking. Configuration is in `pyrightconfig.json`:

```bash
# Run pyright (ensure venv is activated)
pyright src/

# Or via Python module
python -m pyright src/
```

**pyrightconfig.json settings:**
- `venvPath`: "."
- `venv`: ".venv"
- Reports: unused variables, unused imports, duplicate imports

### No Test Framework

**There are currently no tests in this codebase.** If tests are added:
- Use pytest as the testing framework
- Test files should be in a `tests/` directory
- Run a single test: `pytest tests/test_file.py::test_function_name`

---

## Code Style Guidelines

### Import Organization

Imports must be organized with blank lines between groups (in this exact order):

```python
# Python imports
import os
import logging

# Lib imports
import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk
from gi.repository import GLib

# Application imports
from libs.dto.states import SourceViewStates
from .mixins.source_view_dnd_mixin import SourceViewDnDMixin
```

### Type Hints

- Use type hints for all function parameters and return types
- Use Python's built-in types (`list[str]`, `dict[str, int]`) not typing module aliases
- Example: `def message_to(self, name: str, event: BaseEvent):`

### Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Classes | PascalCase | `ControllerBase`, `SourceView` |
| Methods/Variables | snake_case | `set_controller_context`, `_cut_buffer` |
| Private methods | Leading underscore | `_setup_styles`, `_subscribe_to_events` |
| Constants | UPPER_SNAKE_CASE | `LOG_LEVEL`, `DEFAULT_ZOOM` |
| Exception classes | PascalCase ending in Exception | `ControllerBaseException` |

### Class Structure

```python
class MyClass(Singleton, EmitDispatcher):
    def __init__(self):
        super(MyClass, self).__init__()

        self.controller_context: ControllerContext = None
        self._private_var = None

    def public_method(self, param: str) -> None:
        ...

    def _private_method(self) -> None:
        ...
```

### Placeholder Methods

Use ellipsis `...` for unimplemented methods or abstract-like methods:

```python
def _subscribe_to_events(self):
    ...
```

### Dataclasses for DTOs/Events

Use `@dataclass` for data transfer objects and events:

```python
from dataclasses import dataclass, field

@dataclass
class TextInsertedEvent(CodeEvent):
    location: Gtk.TextIter = None
    text: str              = ""
    length: int            = 0
```

### Error Handling

- Custom exceptions should end with `Exception`
- Use `raise ValueError("message")` for validation errors
- Let exceptions propagate for unexpected errors

### Singleton Pattern

Classes requiring singleton behavior should inherit from `Singleton`:

```python
from libs.singleton import Singleton

class MySingleton(Singleton):
    ...
```

### GTK/Widget Conventions

- Call `_setup_styles()`, `_setup_signals()`, `_subscribe_to_events()`, `_load_widgets()` in `__init__`
- Use `self.connect("signal-name", self._handler)` for GTK signals
- Private GTK attributes use underscore prefix: `self._cut_temp_timeout_id`

### Code Formatting

- Use spaces around operators: `x = value`, not `x=value`
- Align assignments with spaces for related variables:
  ```python
  self.state                = state
  self._cut_temp_timeout_id = None
  ```
- Maximum line length: Let pyright/editor handle warnings (typically 80-120 chars)

### No Comments

DO NOT add comments to code unless explicitly required. Write self-documenting code.

---

## Project Structure

```
Newton/
├── src/
│   ├── app.py              # Main application entry
│   ├── __main__.py         # Module entry point
│   ├── __builtins__.py     # Built-in definitions
│   ├── core/               # Core UI components
│   │   ├── containers/     # Layout containers
│   │   ├── controllers/    # Controllers
│   │   └── widgets/        # GTK widgets
│   ├── libs/               # Core libraries
│   │   ├── controllers/    # Controller infrastructure
│   │   ├── db/             # Database (SQLModel)
│   │   ├── dto/            # Data transfer objects
│   │   ├── mixins/         # Mixin classes
│   │   └── settings/       # Settings management
│   └── plugins/            # Plugin system
├── plugins/                # Plugin implementations
├── user_config/            # User configuration files
├── requirements.txt        # Python dependencies
└── pyrightconfig.json      # Pyright configuration
```

---

## Key Libraries Used

- **PyGObject** (GTK3) - GUI framework
- **sqlmodel** - Database (SQLAlchemy + Pydantic)
- **setproctitle** - Process title management
- **pyxdg** - XDG desktop file parsing

---

## Common Patterns

### Creating a New Controller

```python
from libs.controllers.controller_base import ControllerBase
from libs.controllers.controller_context import ControllerContext

class MyController(ControllerBase):
    def __init__(self):
        super().__init__()
        self.controller_context = None

    def _controller_message(self, event: BaseEvent):
        # Handle events
        pass
```

### Creating a New Event/DTO

```python
from dataclasses import dataclass
from libs.dto.code.code_event import CodeEvent

@dataclass
class MyEvent(CodeEvent):
    field1: str = ""
    field2: int = 0
```

### Connecting to Events

```python
from libs.event_system import EventSystem

event_system = EventSystem()
event_system.subscribe("event_name", self.my_handler)
```
