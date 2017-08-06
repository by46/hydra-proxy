from io import BytesIO

from tds.tokens import SQLBatchStream
from .base import Request


class SQLBatchRequest(Request):
    def __init__(self, buf):
        """

        :param BytesIO buf: 
        """
        super(SQLBatchRequest, self).__init__()
        self.stream = stream = SQLBatchStream()
        stream.unmarshal(buf)
