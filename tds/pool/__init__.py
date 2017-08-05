import logging
from io import BytesIO
from socket import socket

from tds.packets import PacketHeader
from tds.tokens import Login7Stream
from tds.tokens import PreLoginStream
from .poolmanager import PoolManager

manager = PoolManager(size=1)


def get_connection(user, password, server_name):
    """
    user=CTIDbo
    password=Dev@CTIdb0
    server_name=S1DSQL04\\EHISSQL
    
    :param str user: real user
    :param str password: real password
    :param str server_name: database instance
    :rtype: socket 
    """
    conn = socket()
    conn.connect(('10.1.25.24', 1433))

    # pre-login
    stream = PreLoginStream()
    stream.version = (1426128904, 0)
    stream.encryption = PreLoginStream.ENCRYPT_NOT_SUP
    stream.inst_opt = "EHISSQL"
    stream.thread_id = 9999
    packet = PacketHeader()
    packet.packet_type = PacketHeader.TYPE_PRE_LOGIN
    # beautify_hex(stream.marshal())
    conn.sendall(packet.marshal(stream))

    header = conn.recv(8)
    packet.unmarshal(header)
    data = conn.recv(packet.length)
    buf = BytesIO(data)
    stream.unmarshal(buf)

    # login

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
    stream.database = 'CTI'

    packet = PacketHeader()
    packet.packet_type = PacketHeader.TYPE_LOGIN
    # beautify_hex(stream.marshal())
    conn.sendall(packet.marshal(stream))

    header = conn.recv(8)
    packet.unmarshal(header)
    data = conn.recv(packet.length)
    buf = BytesIO(data)
    stream.unmarshal(buf)
    logging.error(stream.username)
    return conn
