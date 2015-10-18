import contextlib
import errno
import os
import time
import tempfile
import importlib


def import_from_classname(class_name_str):
    module, class_name = class_name_str.rsplit('.', 1)
    Class = getattr(importlib.import_module(module), class_name)
    return Class


def ctypes_dict():
    from django.contrib.contenttypes.models import ContentType

    values = ContentType.objects.values_list('app_label', 'model', 'id')
    ctypes = {}
    [ctypes.update({"%s.%s" % x[:2]: x[2]}) for x in values]
    return ctypes


@contextlib.contextmanager
def filelock(name, wait_delay=.1):
    path = os.path.join(tempfile.gettempdir(), name)
    while True:
        try:
            fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_RDWR)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
            time.sleep(wait_delay)
            continue
        else:
            break
    try:
        yield fd
    finally:
        os.close(fd)
        os.unlink(path)
