from io import BytesIO

from tds.base import StreamSerializer


class FedAuthInfoStream(StreamSerializer):
    TOKEN_TYPE = 0xEE

    def unmarshal(self, buf):
        """

        :param BytesIO buf: 
        :rtype: bool
        """
