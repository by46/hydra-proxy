from io import BytesIO

from tds.base import StreamSerializer


class OffsetStream(StreamSerializer):
    TOKEN_TYPE = 0x78

    def unmarshal(self, buf):
        """

        :param BytesIO buf: 
        :rtype: bool
        """
