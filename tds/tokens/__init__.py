from io import BytesIO

from .alt_metadata import ALTMetadataStream
from .alt_row import ALTRowStream
from .col_info import ColumnInfoStream
from .col_metadata import ColumnMetadataStream
from .collation import Collation
from .done import DoneStream
from .done_in_proc import DoneInProcedureStream
from .done_proc import DoneProcedureStream
from .envchange import EnvChangeStream
from .feature_ext_ack import FeatureExtAckStream
from .fed_auth_info import FedAuthInfoStream
from .info import InfoStream
from .login import Login7Stream
from .login import LoginAckStream
from .nbc_row import NBCRowStream
from .offset import OffsetStream
from .order import OrderStream
from .pre_login import PreLoginStream
from .return_status import ReturnStatusStream
from .return_value import ReturnValueStream
from .row import RowStream
from .session_state import SessionStateStream
from .sql_batch import SQLBatchStream
from .sspi import SSPIStream
from .tab_name import TableNameStream
from .tvp_row import TVPRowStream

Tokens = [ALTMetadataStream, ALTRowStream, ColumnInfoStream,
          ColumnMetadataStream,
          Collation, DoneStream, DoneInProcedureStream, DoneProcedureStream,
          EnvChangeStream, FeatureExtAckStream, FedAuthInfoStream, InfoStream,
          Login7Stream, LoginAckStream,
          NBCRowStream, OffsetStream, OrderStream, PreLoginStream,
          ReturnStatusStream, ReturnValueStream,
          RowStream, SessionStateStream, SQLBatchStream,
          SSPIStream, TableNameStream, TVPRowStream]


def parse_tokens(buf):
    """
    Parse all tokens 
    :param BytesIO buf: 
    :rtype: []
    """
