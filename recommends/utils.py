import contextlib
import errno
import os
import time
import tempfile


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
