from io import BytesIO

from tds.base import StreamSerializer


class FeatureExtAckStream(StreamSerializer):
    TOKEN_TYPE = 0xAE

    def unmarshal(self, buf):
        """

        :param BytesIO buf: 
        :rtype: bool
        """
