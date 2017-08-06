from io import BytesIO

from tds.base import StreamSerializer


class DoneProcedureStream(StreamSerializer):
    TOKEN_TYPE = 0xFE

    def unmarshal(self, buf):
        """

        :param BytesIO buf: 
        :rtype: bool
        """
