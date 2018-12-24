#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of django-lokalise.
# https://github.com/yarlson/django-lokalise

# Licensed under the BSD license:
# http://www.opensource.org/licenses/BSD-license
# Copyright (c) 2016, Yar Kravtsov <yarlson@gmail.com>

import errno
import os
import re
import shutil
import time
import zipfile
from io import BytesIO

from django.conf import settings
from django.core.management.commands.compilemessages import Command

from lokalise.version import __version__  # NOQA


def get_locale_path():
    p = os.path.dirname(os.path.normpath(os.sys.modules[settings.SETTINGS_MODULE].__file__))
    return os.path.join(re.sub(r"settings$", "", p), 'locale')


def make_dir(folder_name):
    try:
        os.makedirs(folder_name)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise


def compile_po(full_file_path):
    file_name = os.path.basename(full_file_path)
    dir_name = os.path.dirname(full_file_path)

    compile_command = Command()
    compile_command.verbosity = 0
    compile_command.compile_messages([(dir_name, file_name)])


def handle_content(content):
    locale_path = get_locale_path()

    f = BytesIO(content)

    if os.access(locale_path, os.W_OK | os.X_OK):
        with zipfile.ZipFile(f) as zip_file:
            for member in zip_file.namelist():
                filename = os.path.basename(member)
                if not filename:
                    continue

                if re.search(r"\.po$", filename):
                    [lang, ext] = os.path.splitext(filename)

                    lang_path = os.path.join(os.path.join(locale_path, lang), 'LC_MESSAGES')
                    make_dir(lang_path)

                    po_file = os.path.join(lang_path, "django{0}".format(ext))

                    source = zip_file.open(member)
                    target = open(po_file, "wb")
                    with source, target:
                        shutil.copyfileobj(source, target)

                    compile_po(po_file)

                    current_time = time.time()
                    os.utime(locale_path, (current_time, current_time))
