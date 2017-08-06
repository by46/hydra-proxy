import errno
import os
from logging.handlers import RotatingFileHandler


def ensure_dir(path):
    """os.makedirs without EEXIST."""
    try:
        os.makedirs(path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise


class BetterRotatingFileHandler(RotatingFileHandler):
    def _open(self):
        ensure_dir(os.path.dirname(self.baseFilename))
        return super(BetterRotatingFileHandler, self)._open()
