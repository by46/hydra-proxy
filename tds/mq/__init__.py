from json import dumps

import requests
from requests.adapters import HTTPAdapter

session = requests.session()
a = HTTPAdapter(max_retries=3)
session.mount('http://', a)
a = HTTPAdapter(max_retries=3)
session.mount('https://', a)


def send(event):
    url = 'http://apis.newegg.org/framework/v1/enterprise-messaging/message'
    headers = {'Content-Type': 'Application/Json', 'Accept': 'Application/Json'}
    json = {
        'MessageName': 'DFIS_TDS',
        'MessageBody': dumps(event),
        'ContentType': 'Application/Json',
        'InvokeType': 'Message'
    }
    response = session.post(url, headers=headers, json=json)
    assert response.status_code == 201
