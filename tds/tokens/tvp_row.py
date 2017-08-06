from io import BytesIO

from tds.base import StreamSerializer


class TVPRowStream(StreamSerializer):
    TOKEN_TYPE = 0x01

    def unmarshal(self, buf):
        """

        :param BytesIO buf: 
        :rtype: bool
        """
