from socket import socket

from tds import protocol
from tds.packages.geventconnpool import ConnectionPool

DEFAULT_POOL_SIZE = 20


class MSSQLConnectionPool(ConnectionPool):
    def __init__(self, host, port, user, password, database,
                 **kwargs):
        """

        :param host: 
        :param port: 
        :param user: 
        :param password: 
        :param database: 
        :param dict kwargs: ConnectionPool args 
        """
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        # TODO(benjamin): instance
        self.server_name = "S1DSQL04\\EHISSQL"
        if 'size' not in kwargs:
            kwargs['size'] = DEFAULT_POOL_SIZE
        super(MSSQLConnectionPool, self).__init__(**kwargs)

    def _new_connection(self):
        conn = socket()
        conn.connect((self.host, self.port))

        # pre-login
        if not protocol.pre_login(conn):
            # TODO(benjamin): login failed
            raise Exception()
        if not protocol.login(conn, self.user, self.password, self.server_name, self.database):
            # TODO(benjamin): login failed
            raise Exception()
        return conn
