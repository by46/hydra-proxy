import logging
from io import BytesIO
from socket import socket

from tds.packets import PACKET_HEADER_LEN
from tds.packets import PacketHeader
from tds.tokens import Login7Stream


def login(conn, user, password, server_name, database):
    """
    
    :param socket conn: 
    :param user: 
    :param password: 
    :param server_name: 
    :param database: 
    :return: 
    """
    stream = Login7Stream()
    stream.tds_version = 0x71000001
    stream.client_version = 4176642822
    stream.client_pid = 14228
    stream.connection_id = 0
    stream.option_flags1 = 0xf0
    stream.option_flags2 = 0x01
    stream.sql_type_flags = 0x00
    stream.reserved_flags = 0x00
    stream.time_zone = 0xFFFFFF88
    stream.collation = 0x00000436
    stream.client_name = 'WCMIS035'
    stream.username = user
    stream.password = password
    stream.app_name = "pymssql=2.1.3"
    stream.server_name = server_name
    stream.lib_name = "DB-Library"
    stream.locale = 'us_english'
    stream.database = database

    packet = PacketHeader()
    packet.packet_type = PacketHeader.TYPE_LOGIN
    conn.sendall(packet.marshal(stream))

    header = conn.recv(PACKET_HEADER_LEN)
    if len(header) != PACKET_HEADER_LEN:
        # TODO(benjamin): process error
        raise Exception()
    packet.unmarshal(header)
    data = conn.recv(packet.length)
    buf = BytesIO(data)
    stream.unmarshal(buf)
    logging.error(stream.username)
    return True
