from io import BytesIO

from tds.base import StreamSerializer


class NBCRowStream(StreamSerializer):
    TOKEN_TYPE = 0xD2

    def unmarshal(self, buf):
        """

        :param BytesIO buf: 
        :rtype: bool
        """
