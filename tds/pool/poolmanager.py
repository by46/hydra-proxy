import logging
from io import BytesIO
from socket import socket

from gevent.queue import Empty
from gevent.queue import Full
from gevent.queue import LifoQueue
from urllib3.util import is_connection_dropped

from tds.packets import PacketHeader
from tds.tokens import Login7Stream
from tds.tokens import PreLoginStream
from .pool import MSSQLConnectionPool


class PoolManager(object):
    """
    
    
    Example:
        >>> manager = PoolManager()
        >>> pool = manager.get_connection({})
        >>> with pool.get() as conn:
        >>>     conn.send("message")
    """
    PoolCls = MSSQLConnectionPool

    def __init__(self, **kwargs):
        self.connection_pool_kw = kwargs
        self.pools = dict()

    def get_connection(self, connection_settings):
        """
        connection_settings = {
            "user": "real_user",
            "password": "real_password",
            "instance": "S1DSQL04\\EHISSQL",
            "database": "EHISSQL",
            "ip": "10.1.25.24",
            "port": 1433
        }
        :param dict connection_settings: 
        :rtype: MSSQLConnectionPool
        """
        ip = connection_settings['ip']
        port = connection_settings['port']
        password = connection_settings['password']
        user = connection_settings['user']
        database = connection_settings['database']
        return self.connection_from_host(ip, port, user, password, database)

    def connection_from_host(self, host, port, user, password, database):
        pool_key = (host, port, user)
        pool = self.pools.get(pool_key)
        if pool:
            return pool
        pool = self._new_pool(host, port, user, password, database)
        self.pools[pool_key] = pool
        return pool

    def _new_pool(self, host, port, user, password, database):
        kwargs = self.connection_pool_kw
        return self.PoolCls(host, port, user, password, database, **kwargs)


class ConnectionPool2(object):
    QueueCls = LifoQueue

    def __init__(self, host, port, user, password, database, server_name):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.server_name = server_name
        self.pool = self.QueueCls()
        # TODO(benjamin): need initialize
        self.block = False

    def _get_conn(self, timeout=None):
        conn = None
        try:
            conn = self.pool.get(block=self.block, timeout=timeout)
        except Empty:
            if self.block:
                raise Exception("Pool reached maximum size and"
                                "no more connections are allowed")
        if conn and is_connection_dropped(conn):
            conn.close()

        return conn or self._new_conn()

    def _put_conn(self, conn):
        try:
            self.pool.put(conn, block=False)
        except Full:
            # TODO(benjamin): process error
            pass
        if conn:
            conn.close()

    def _new_conn(self):
        conn = socket()
        conn.connect((self.host, self.port))

        # pre-login
        stream = PreLoginStream()
        stream.version = (1426128904, 0)
        stream.encryption = PreLoginStream.ENCRYPT_NOT_SUP
        stream.inst_opt = self.database
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
        stream.username = self.user
        stream.password = self.password
        stream.app_name = "pymssql=2.1.3"
        stream.server_name = self.server_name
        stream.lib_name = "DB-Library"
        stream.locale = 'us_english'
        stream.database = self.database

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
