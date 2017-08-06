import struct
from io import BytesIO

from tds.base import StreamSerializer


class SQLBatchStream(StreamSerializer):
    TOKEN_TYPE = 0xFD
    FMT = '<BHHL'

    def __init__(self, text=None):
        self.text = text
        super(SQLBatchStream, self).__init__()

    def marshal(self):
        return struct.pack(self.FMT, self.TOKEN_TYPE, self.status, self.current_cmd, self.done_row_count)

    def unmarshal(self, buf):
        """
        
        :param BytesIO buf: 
        :return: 
        """
        self.text = buf.getvalue().decode('utf-16-le')
