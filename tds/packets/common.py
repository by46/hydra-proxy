import struct
from io import RawIOBase

from tds.base import StreamSerializer


class PacketHeader(StreamSerializer):
    FMT = "!BBHHBB"
    TYPE_BATCH = 1
    TYPE_PRE_TDS7 = 2
    TYPE_RPC = 3
    TYPE_RESPONSE = 4
    TYPE_ATTENTION = 6
    TYPE_BULK = 7
    TYPE_REDERATED = 8
    TYPE_LOGIN = 16
    TYPE_PRE_LOGIN = 18

    def __init__(self):
        self.packet_type = self.TYPE_RESPONSE
        self.status = 1
        self.length = None
        self.pid = 0
        self.packet_id = 0
        self.window = 0
        super(PacketHeader, self).__init__()

    def unmarshal(self, content):
        """

        :param str content: 
        """
        packet_type, status, length, pid, packet_id, window = struct.unpack(self.FMT, content)
        self.packet_type = packet_type
        self.status = status
        self.length = length
        self.pid = pid
        self.packet_id = packet_id
        self.window = window

    def marshal(self, response):
        """

        :param Response | RawIOBase response: 
        :return: 
        """
        if hasattr(response, 'getvalue'):
            message = response.getvalue()
        else:
            message = response.marshal()
        length = len(message) + 8
        self.buf.truncate()
        self.buf.write(chr(self.packet_type))
        self.buf.write(chr(self.status))
        self.buf.write(struct.pack('!HHBB', length, self.pid, self.packet_id, 0))
        self.buf.write(message)
        return self.buf.getvalue()
