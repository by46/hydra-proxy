from io import BytesIO

from tds.base import StreamSerializer


class ALTRowStream(StreamSerializer):
    TOKEN_TYPE = 0xD3

    def unmarshal(self, buf):
        """

        :param BytesIO buf: 
        :rtype: bool
        """
