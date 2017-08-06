from io import BytesIO

from tds.base import StreamSerializer


class OrderStream(StreamSerializer):
    TOKEN_TYPE = 0xA9

    def unmarshal(self, buf):
        """

        :param BytesIO buf: 
        :rtype: bool
        """
