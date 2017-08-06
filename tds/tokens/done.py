import struct
from io import BytesIO

from tds.base import StreamSerializer


class DoneStream(StreamSerializer):
    TOKEN_TYPE = 0xFD
    FMT = '<BHHL'

    def __init__(self, status=0, current_cmd=0, done_row_count=0):
        self.status = status
        self.current_cmd = current_cmd
        self.done_row_count = done_row_count
        super(DoneStream, self).__init__()

    def marshal(self):
        return struct.pack(self.FMT, self.TOKEN_TYPE, self.status, self.current_cmd, self.done_row_count)

    def unmarshal(self, buf):
        """
        
        :param BytesIO buf: 
        :return: 
        """
        size = struct.calcsize(self.FMT)
        token_type, status, current_cmd, row_count = struct.unpack(self.FMT, buf.read(size))
        assert self.TOKEN_TYPE == token_type
        self.status = status
        self.current_cmd = current_cmd
        self.done_row_count = row_count
        return True
