from io import BytesIO

from tds.base import StreamSerializer


class RowStream(StreamSerializer):
    TOKEN_TYPE = 0xD1

    def unmarshal(self, buf):
        """

        :param BytesIO buf: 
        :rtype: bool
        """
