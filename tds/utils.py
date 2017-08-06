import struct

decrypt_bets = {0: 'Z', 1: 'J', 2: 'z', 3: 'j', 6: ':', 7: '*', 16: '[', 17: 'K', 18: '{', 19: 'k', 23: '+', 32: 'X',
                33: 'H', 34: 'x', 35: 'h', 38: '8', 39: '(', 48: 'Y', 49: 'I', 50: 'y', 51: 'i', 54: '9', 55: ')',
                64: '^', 65: 'N', 66: '~', 67: 'n', 70: '>', 71: '.', 80: '_', 81: 'O', 83: 'o', 86: '?', 87: '/',
                96: '\\', 97: 'L', 98: '|', 99: 'l', 102: '<', 103: ',', 112: ']', 113: 'M', 114: '}', 115: 'm',
                118: '=', 119: '-', 128: 'R', 129: 'B', 130: 'r', 131: 'b', 134: '2', 135: '"', 144: 'S', 145: 'C',
                146: 's', 147: 'c', 150: '3', 151: '#', 160: 'P', 161: '@', 162: 'p', 163: '`', 166: '0', 176: 'Q',
                177: 'A', 178: 'q', 179: 'a', 182: '1', 183: '!', 192: 'V', 193: 'F', 194: 'v', 195: 'f', 198: '6',
                199: '&', 208: 'W', 209: 'G', 210: 'w', 211: 'g', 214: '7', 215: "'", 224: 'T', 225: 'D', 226: 't',
                227: 'd', 230: '4', 231: '$', 240: 'U', 241: 'E', 242: 'u', 243: 'e', 246: '5', 247: '%'}

encrypt_bets = {'$': 231, '(': 39, ',': 103, '0': 166, '4': 230, '8': 38, '<': 102, '@': 161, 'D': 225, 'H': 33,
                'L': 97, 'P': 160, 'T': 224, 'X': 32, '\\': 96, '`': 163, 'd': 227, 'h': 35, 'l': 99, 'p': 162,
                't': 226, 'x': 34, '|': 98, '#': 151, "'": 215, '+': 23, '/': 87, '3': 150, '7': 214, '?': 86, 'C': 145,
                'G': 209, 'K': 17, 'O': 81, 'S': 144, 'W': 208, '[': 16, '_': 80, 'c': 147, 'g': 211, 'k': 19, 'o': 83,
                's': 146, 'w': 210, '{': 18, '"': 135, '&': 199, '*': 7, '.': 71, '2': 134, '6': 198, ':': 6, '>': 70,
                'B': 129, 'F': 193, 'J': 1, 'N': 65, 'R': 128, 'V': 192, 'Z': 0, '^': 64, 'b': 131, 'f': 195, 'j': 3,
                'n': 67, 'r': 130, 'v': 194, 'z': 2, '~': 66, '!': 183, '%': 247, ')': 55, '-': 119, '1': 182, '5': 246,
                '9': 54, '=': 118, 'A': 177, 'E': 241, 'I': 49, 'M': 113, 'Q': 176, 'U': 240, 'Y': 48, ']': 112,
                'a': 179, 'e': 243, 'i': 51, 'm': 115, 'q': 178, 'u': 242, 'y': 50, '}': 114}

LENGTH_FMT = {
    1: '<B',
    2: '<H',
    4: '<L'
}


def decrypt(text):
    """

    :param str text: 
    :rtype: str
    """
    plain = []
    for i in range(0, len(text), 2):
        num, = struct.unpack('!B', text[i])
        plain.append(decrypt_bets.get(num))
    return ''.join(plain)


def encrypt(text):
    return ''.join([chr(encrypt_bets.get(c)) + '\xA5' for c in text])


def decode(text):
    return ''.join([c for c in text if c != '\x00'])


def beautify_hex(text):
    for i in range(0, len(text), 16):
        tmp = [ord(c) for c in text[i:i + 16]]
        fmt = "{:02X} " * len(tmp)
        print fmt.format(*tmp)


def b_varchar_encode(text):
    """
    encode with utf-16-le
    Byte *Varchar
    :param str text: 
    :return: 
    """
    if not text:
        return '\x00'
    length = len(text)
    return chr(length) + text.encode('utf-16-le')


def us_varchar_encode(text):
    """
    encode with utf-16-le
    UShort *Varchar
    :param str text: 
    :return: 
    """
    if not text:
        return '\x00\x00'
    length = len(text)
    return struct.pack('<H', length) + text.encode('utf-16-le')


def b_varbyte_encode(value):
    return varbyte_encode(value)


def us_varbyte_encode(value):
    return varbyte_encode(value, byte_length=2)


def l_varbyte_encode(value):
    return varbyte_encode(value, byte_length=4)


def varbyte_encode(value, byte_length=1):
    value = value or ''
    length = len(value)
    if byte_length not in LENGTH_FMT:
        raise ValueError('byte_length should been 1, 2, 4')
    fmt = LENGTH_FMT.get(byte_length)

    return struct.pack(fmt, length) + value
