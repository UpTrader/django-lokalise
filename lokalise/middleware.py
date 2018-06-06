import threading
from os.path import getmtime

from django.utils import translation
from django.utils.autoreload import reset_translations
from django.utils.translation import trans_real, get_language

from . import get_locale_path


class ReloadTranslationsMiddleware(object):
    @staticmethod
    def process_request(request):
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
