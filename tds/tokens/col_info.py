from io import BytesIO

from tds.base import StreamSerializer


class ColumnInfoStream(StreamSerializer):
    TOKEN_TYPE = 0xA5

    def unmarshal(self, buf):
        """

        :param BytesIO buf: 
        :rtype: bool
        """
