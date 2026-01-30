---
trigger: always_on
---

# Rule: Python Engineering Standards

- **Encapsulation:** All logic must reside within classes. No global state.
- **Type Hinting:** Use `typing` for all method signatures (e.g., `def convert(self, path: str) -> str:`).
- **Docstrings:** Follow Google-style docstrings for every class and method.
- **Error Handling:** Every file I/O or conversion call must be wrapped in `try-except` blocks.
- **Logging:** Use the standard `logging` library. Redirect logs to `app.log`