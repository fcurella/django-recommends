import contextlib
import errno
import os
import time
import tempfile
from django.utils import importlib


def import_from_classname(class_name_str):
    module, class_name = class_name_str.rsplit('.', 1)
    Class = getattr(importlib.import_module(module), class_name)
    return Class


@contextlib.contextmanager
def filelock(name, wait_delay=.1):
    path = os.path.join(tempfile.gettempdir(), name)
    while True:
        try:
            fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_RDWR)
        except OSError, e:
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
