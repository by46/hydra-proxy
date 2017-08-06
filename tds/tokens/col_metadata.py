from io import BytesIO

from tds.base import StreamSerializer


class ColumnMetadataStream(StreamSerializer):
    TOKEN_TYPE = 0x81

    def unmarshal(self, buf):
        """

        :param BytesIO buf: 
        :rtype: bool
        """
