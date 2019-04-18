import requests as req
from lcu_connectorpy import Connector


class Session:

    headers = {
       'Accept': 'application/json'
    }

    def __init__(self):
        self.conn = Connector()

    def __get_session(self):
        return req.get(
            f'{self.conn.url}/lol-champ-select/v1/session',
            auth=self.conn.auth,
            headers=self.headers,
            verify=False
        )

    def start(self):
        self.conn.start()

    def get_current(self) -> dict:
        r = self.__get_session()
        if r.ok:
            return r.json()
