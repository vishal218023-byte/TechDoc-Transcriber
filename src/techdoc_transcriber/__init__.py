__all__ = [
    "DocumentModel",
    "DocumentView",
    "DocumentController",
]

_MODULE_MAPPING = {
    "DocumentModel": "model",
    "DocumentView": "view",
    "DocumentController": "controller",
}


def __getattr__(name):
    module_name = _MODULE_MAPPING.get(name)
    if not module_name:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

    module = __import__(f"{__name__}.{module_name}", fromlist=[name])
    value = getattr(module, name)
    globals()[name] = value
    return value
