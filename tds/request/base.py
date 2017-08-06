class Request(object):
    def __init__(self):
        self.stream = object()

    def __getattr__(self, item):
        return getattr(self.stream, item)
