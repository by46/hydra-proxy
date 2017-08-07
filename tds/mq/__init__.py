import logging
from json import dumps

import requests
from requests.adapters import HTTPAdapter

session = requests.session()
a = HTTPAdapter(max_retries=3)
session.mount('http://', a)
a = HTTPAdapter(max_retries=3)
session.mount('https://', a)
logger = logging.getLogger('tds')


def send(event):
    url = 'http://apis.newegg.org/framework/v1/enterprise-messaging/message'
    url = 'http://10.1.54.117/framework/v1/enterprise-messaging/message'
    # url = 'http://10.16.75.24:3000/framework/v1/enterprise-messaging/message'
    headers = {'Content-Type': 'Application/Json', 'Accept': 'Application/Json'}
    json = {
        'MessageName': 'DFIS_TDS',
        'MessageBody': dumps(event),
        'ContentType': 'Application/Json',
        'InvokeType': 'Message'
    }
    response = session.post(url, headers=headers, json=json)

    logger.info('send mq starting %s', response.status_code)
    # TODO(benjamin): process error
    if response.status_code != 201:
        logger.error('send mq failed, %s', response.content)


if __name__ == '__main__':
    send(event={
        "stamp": "20170802140000",
        "user": "user1",
        "database": "EHISQL",
        "client_ip": "10.16.82.135",
        "event": "batch",
        "text": "SELECT * FROM User LIMIT 10;",
        "elapse": 120,
        "error": "Unknown Databases"
    })
