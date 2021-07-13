import threading
import os, errno
from os.path import getmtime, exists as path_exists

from django.utils import translation
from django.utils.deprecation import MiddlewareMixin
from django.utils.translation import trans_real, get_language

from . import get_locale_path


class ReloadTranslationsMiddleware(MiddlewareMixin):
    @staticmethod
    def process_request(request):
        locale_path = get_locale_path()
        if not path_exists(locale_path):
            try:
                os.makedirs(locale_path)
            except OSError as e:
                # https://stackoverflow.com/questions/273192/how-can-i-safely-create-a-nested-directory-in-python
                if e.errno != errno.EEXIST:
                    raise
        locale_mtime = getmtime(get_locale_path())
        try:
            thread_local = threading.local()
            if not hasattr(thread_local, 'locale_mtime') or locale_mtime > thread_local.locale_mtime:
                thread_local.locale_mtime = locale_mtime
                import gettext
                from django.utils.translation import trans_real
                gettext._translations = {}
                trans_real._translations = {}
                trans_real._default = None
                translation.activate(get_language())
        except Exception as e:
            pass
