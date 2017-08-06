from io import BytesIO

from tds.base import StreamSerializer


class DoneInProcedureStream(StreamSerializer):
    TOKEN_TYPE = 0xFF

    def unmarshal(self, buf):
        """

        :param BytesIO buf: 
        :rtype: bool
        """
