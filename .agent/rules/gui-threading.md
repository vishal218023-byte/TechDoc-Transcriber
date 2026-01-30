---
trigger: always_on
---

# Rule: Thread-Safe GUI Operations

- **Non-Blocking UI:** The main thread must only handle the CustomTkinter `mainloop`.
- **Worker Threads:** All Docling conversion tasks must run in a background `threading.Thread`.
- **UI Updates:** Background threads must NOT update UI elements directly. 
- **The .after() Pattern:** Use `self.after(0, update_func)` or a `queue.Queue` to send data from the background thread back to the main GUI thread safely.