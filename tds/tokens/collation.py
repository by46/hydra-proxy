from tds.base import StreamSerializer


class Collation(StreamSerializer):
    def marshal(self):
        # TODO(benjamin): parse collation
        return '\x09\x04\xd0\x00\x34'
