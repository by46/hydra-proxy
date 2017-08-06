from io import BytesIO

from tds.base import StreamSerializer


class SSPIStream(StreamSerializer):
    TOKEN_TYPE = 0xED

    def unmarshal(self, buf):
        """

        :param BytesIO buf: 
        :rtype: bool
        """
