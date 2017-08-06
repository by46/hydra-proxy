import struct
from io import BytesIO

import six

from tds.base import StreamSerializer


class PreLoginStream(StreamSerializer):
    TOKEN_TYPE = 0xAD
    TERMINATOR = 0xFF
    ENCRYPT_OFF = 0x00
    ENCRYPT_ON = 0x01
    ENCRYPT_NOT_SUP = 0x02
    ENCRYPT_REQ = 0x03
    OPTIONS = {
        0x00: ('version', '!LH'),
        0x01: ('encryption', '!B'),
        0x02: ('inst_opt', None),
        0x03: ('thread_id', '!L'),
        0x04: ('mars', '!B'),
        0x05: ('trace_id', '!16s20s'),
        0x06: ('fedauth_required', '!B'),
        0x07: ('nonce_opt', '!32s'),
        0xFF: None
    }

    def __init__(self):
        self.version = None
        self.encryption = None
        self.inst_opt = None
        self.thread_id = None
        self.mars = None
        self.trace_id = None
        self.fedauth_required = None
        self.nonce_opt = None
        super(PreLoginStream, self).__init__()

    def marshal(self):
        """
        
        :rtype: bytes 
        """
        options_data = BytesIO()
        payload_data = BytesIO()
        options = []
        for key in sorted(six.iterkeys(self.OPTIONS)):
            if key == self.TERMINATOR:
                continue
            name, fmt = self.OPTIONS.get(key)
            if getattr(self, name, None) is not None:
                options.append((key, name, fmt))

        offset = len(options) * 5 + 1

        for key, name, fmt in options:
            if fmt:
                length = struct.calcsize(fmt)
                options_data.write(struct.pack('!BHH', key, offset, length))
                params = getattr(self, name)
                if not isinstance(params, tuple):
                    params = (params,)
                payload_data.write(struct.pack(fmt, *params))
                offset += length
            else:
                # inst_opt
                value = getattr(self, name) + '\x00'
                length = len(value)
                options_data.write(struct.pack('!BHH', key, offset, length))
                payload_data.write(value)
                offset += length

        options_data.write(chr(0xFF))
        options_data.write(payload_data.getvalue())
        return options_data.getvalue()

    def unmarshal(self, buf):
        """
        
        :param BytesIO buf: 
        """
        while True:
            token_type, = struct.unpack('!B', buf.read(1))
            if token_type not in self.OPTIONS:
                raise ValueError()
            if token_type == self.TERMINATOR:
                break
            position, length = struct.unpack("!HH", buf.read(4))
            if not length:
                continue
            old_position = buf.tell()
            buf.seek(position)
            tmp = buf.read(length)
            name, fmt = self.OPTIONS.get(token_type)
            if fmt:
                values = struct.unpack(fmt, tmp)
                setattr(self, name, values[0] if len(values) == 1 else values)
            else:
                setattr(self, name, tmp)
            buf.seek(old_position)
