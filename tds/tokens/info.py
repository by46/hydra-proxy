import struct
from io import BytesIO
from tds.base import StreamSerializer
from tds.utils import b_varchar_encode
from tds.utils import us_varchar_encode


class InfoStream(StreamSerializer):
    TOKEN_TYPE = 0xAB

    def __init__(self):
        self.sql_error_number = 5701
        self.state = 2
        self.severity = 0
        self.msg = None
        self.server_name = None
        self.process_name = None
        self.line_number = 0
        super(InfoStream, self).__init__()

    def marshal(self):
        self.buf.truncate()
        self.buf.write(struct.pack('<L', self.sql_error_number))
        self.buf.write(chr(self.state))
        self.buf.write(chr(self.severity))
        self.buf.write(us_varchar_encode(self.msg))
        self.buf.write(b_varchar_encode(self.server_name))
        self.buf.write(b_varchar_encode(self.process_name))
        self.buf.write(struct.pack('<H', self.line_number))
        return super(InfoStream, self).marshal()

    def unmarshal(self, buf):
        """
        
        :param BytesIO buf: 
        :return: 
        """
        token_type, length = struct.unpack('<BH', buf.read(3))
        assert token_type == self.TOKEN_TYPE
        # TODO(benjamin): add parse logical
        data = buf.read(length)
        return True