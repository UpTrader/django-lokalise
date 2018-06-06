import threading
from os.path import getmtime

from django.utils.autoreload import reset_translations

from . import get_locale_path


class ReloadTranslationsMiddleware(object):
    @staticmethod
    def process_request(request):
        locale_mtime = getmtime(get_locale_path())
        try:
            thread_local = threading.local
            if not hasattr(thread_locale, 'locale_mtime') or locale_mtime > thread_local.locale_mtime:
                thread_local.locale_mtime = locale_mtime
                reset_translations()
        except Exception as e:
            pass
