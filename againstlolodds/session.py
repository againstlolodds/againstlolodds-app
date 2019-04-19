import requests as req
from lcu_connectorpy import Connector


class Session:

    headers = {
       'Accept': 'application/json'
    }

    def __init__(self):
        self.conn = Connector()

    def __request(self, api):
        return req.get(
            self.conn.url + api,
            auth=self.conn.auth,
            headers=self.headers,
            verify=False
        )

    def __get_session(self):
        return self.__request('/lol-champ-select/v1/session')

    def get_summoner_name(self, id: str):
        r = self.__request('/lol-summoner/v1/summoners/' + id)
        if r.ok:
            return r.json()['displayName']

    def start(self):
        self.conn.start()

    def get_current(self) -> dict:
        r = self.__get_session()
        if r.ok:
            return r.json()
