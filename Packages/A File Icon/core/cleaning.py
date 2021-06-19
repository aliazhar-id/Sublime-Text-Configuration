import shutil

import sublime
import sublime_plugin

from .settings import add_listener, clear_listener

from .utils import path
from .utils.logging import log, dump, message
from .utils.overlay import with_ignored_overlay


class AfiRevertCommand(sublime_plugin.ApplicationCommand):
    def run(self):
        @with_ignored_overlay
        def revert():
            clear_listener()
            try:
                clean_all()
            except Exception as error:
                dump(error)
            finally:
                add_listener()

        sublime.set_timeout_async(revert)


def clean_all():
    message("Cleaning up")

    def handler(function, path, excinfo):
        if handler.success:
            handler.success = False
            log("Error during cleaning")
        dump(path)

    handler.success = True

    shutil.rmtree(path.overlay_cache_path(), onerror=handler)
    shutil.rmtree(path.overlay_path(), onerror=handler)

    if handler.success:
        message("Cleaned up successfully")

    return handler.success
