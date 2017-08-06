import requests
from bunch import Bunch
from requests.adapters import HTTPAdapter

session = requests.session()
a = HTTPAdapter(max_retries=3)
session.mount('http://', a)


def login(user, password):
    """
    
    :param str user: 
    :param str password: 
    :rtype: dict | None | bool
    """
    body = dict(user=user, pwd=password)
    response = session.post('http://st01nbx01/hydra_center/database', json=body, proxies={'http': ''})
    if response.status_code == 401:
        return False
    elif response.status_code == 413:
        return None
    info = Bunch.fromDict(response.json())
    return Bunch(user=info.user,
                 password=info.pwd,
                 # server_name="S1DSQL04\\EHISSQL",
                 server_name=info.server,
                 port=info.port,
                 database=info.database
                 )
