from io import BytesIO

from tds.base import StreamSerializer


class ReturnStatusStream(StreamSerializer):
    TOKEN_TYPE = 0x79

    def unmarshal(self, buf):
        """

        :param BytesIO buf: 
        :rtype: bool
        """
