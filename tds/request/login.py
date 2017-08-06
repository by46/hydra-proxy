from io import BytesIO

from tds.tokens import Login7Stream
from .base import Request


class LoginRequest(Request):
    def __init__(self, buf):
        """

        :param BytesIO buf: 
        """
        super(LoginRequest, self).__init__()
        self.stream = stream = Login7Stream()
        stream.unmarshal(buf)
