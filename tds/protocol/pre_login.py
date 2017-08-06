import threading
from io import BytesIO
from socket import socket

from tds.packets import PACKET_HEADER_LEN
from tds.packets import PacketHeader
from tds.tokens import PreLoginStream


def pre_login(conn):
    """
    
    :param socket conn: 
    :return: 
    """
    # pre-login
    stream = PreLoginStream()
    stream.version = (1426128904, 0)
    stream.encryption = PreLoginStream.ENCRYPT_NOT_SUP
    stream.inst_opt = "MSSQLServer"
    stream.thread_id = threading.current_thread().ident % 4294967295
    packet = PacketHeader()
    packet.packet_type = PacketHeader.TYPE_PRE_LOGIN
    conn.sendall(packet.marshal(stream))

    header = conn.recv(PACKET_HEADER_LEN)
    if len(header) != PACKET_HEADER_LEN:
        # TODO(benjamin): process error
        raise Exception()
    packet.unmarshal(header)
    data = conn.recv(packet.length)
    buf = BytesIO(data)
    stream.unmarshal(buf)
    return True
