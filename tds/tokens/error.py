import struct
from io import BytesIO

from tds.base import StreamSerializer


class ErrorStream(StreamSerializer):
    TOKEN_TYPE = 0xAA
    error_number = 0
    error_state = 0
    error_level = 0
    msg = None
    server_name = None
    proc_name = None
    line_number = 0

    def unmarshal(self, buf):
        """

        :param BytesIO buf: 
        :rtype: bool
        """
        token_type, length = struct.unpack('<BH', buf.read(3))
        assert token_type == self.TOKEN_TYPE
        # TODO(benjamin): add parse logical
        error_number, state, error_level = struct.unpack("<LBB", buf.read(6))
        self.error_number = error_number
        self.error_state = state
        self.error_level = error_level
        length, = struct.unpack('<H', buf.read(2))
        if length:
            self.msg = buf.read(length * 2).decode('utf-16-le')
        return True
