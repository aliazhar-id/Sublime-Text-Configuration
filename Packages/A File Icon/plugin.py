import sys
import sublime

if int(sublime.version()) >= 3114:

    __all__ = ["AfiRevertCommand", "plugin_loaded", "plugin_unloaded"]

    # Clear module cache to force reloading all modules of this package.
    prefix = __package__ + "."  # don't clear the base package
    for module_name in [
        module_name
        for module_name in sys.modules
        if module_name.startswith(prefix) and module_name != __name__
    ]:
        del sys.modules[module_name]
    prefix = None

    from .core.cleaning import AfiRevertCommand, clean_all
    from .core.settings import add_listener, clear_listener
    from .core.utils.overlay import disable_overlay, enable_overlay

    def plugin_loaded():
        def plugin_loaded_async():
            add_listener()
            enable_overlay()

        sublime.set_timeout_async(plugin_loaded_async, 200)

    def plugin_unloaded():
        def cleanup():
            try:
                clean_all()
            finally:
                enable_overlay()

        clear_listener()
        disable_overlay()
        sublime.set_timeout_async(cleanup)


else:
    raise ImportWarning("Doesn't support Sublime Text versions prior to 3114")
