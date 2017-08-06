from io import BytesIO

from tds.base import StreamSerializer


class ALTMetadataStream(StreamSerializer):
    TOKEN_TYPE = 0x88

    def unmarshal(self, buf):
        """
        
        :param BytesIO buf: 
        :rtype: bool
        """
