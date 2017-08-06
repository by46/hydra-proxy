from io import BytesIO

from tds.base import StreamSerializer


class ReturnValueStream(StreamSerializer):
    TOKEN_TYPE = 0xAC

    def unmarshal(self, buf):
        """

        :param BytesIO buf: 
        :rtype: bool
        """
