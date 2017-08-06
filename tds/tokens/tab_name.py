from io import BytesIO

from tds.base import StreamSerializer


class TableNameStream(StreamSerializer):
    TOKEN_TYPE = 0xA4

    def unmarshal(self, buf):
        """

        :param BytesIO buf: 
        :rtype: bool
        """
