from io import BytesIO

from tds.base import StreamSerializer


class SessionStateStream(StreamSerializer):
    TOKEN_TYPE = 0xE4

    def unmarshal(self, buf):
        """

        :param BytesIO buf: 
        :rtype: bool
        """
