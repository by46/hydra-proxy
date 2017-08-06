from io import BytesIO

from tds.tokens import PreLoginStream
from .base import Request


class PreLoginRequest(Request):
    def __init__(self, buf):
        """

        :param BytesIO buf: 
        """
        super(PreLoginRequest, self).__init__()
        self.stream = stream = PreLoginStream()
        stream.unmarshal(buf)
