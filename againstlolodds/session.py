import requests as req
from lcu_connectorpy import Connector
from operator import itemgetter


class Session:

    headers = {
       'Accept': 'application/json'
    }

    def __init__(self):
        self.conn = Connector()

    def __request(self, api, *args):
        r = req.get(
            self.conn.url + api,
            auth=self.conn.auth,
            headers=self.headers,
            verify=False
        )
        if not r.ok:
            return

        if args:
            getter = itemgetter(*args)
            return getter(r.json())
        return r.json()

    def start(self):
        self.conn.start()

    def get_summoner_name(self, id: str):
        return self.__request(f'/lol-summoner/v1/summoners/{id}', 'displayName')

    def get_champion_name(self, champion_id: str, summoner_id=None):
        summoner_id = summoner_id or self.get_current_summonerid()
        return self.__request(
            f'/lol-champions/v1/inventories/{summoner_id}/champions/{champion_id}', 'name'
        )

    def get_current_session(self) -> dict:
        return self.__request('/lol-champ-select/v1/session')

    def get_current_summonerid(self):
        return self.__request('/lol-summoner/v1/current-summoner', 'summonerId')

    def calculate(self, team, enemy):
        body = [
            [{
                'summonerName': member.name,
                'role': member.role,
                'champion': member.champion,
                'override': None
            } for member in team.values()],
            [{
                'role': member.role,
                'champion': member.champion,
            } for member in enemy.values()],
            {
                'region': 'na'
            }
        ]
        headers = {'Content-Type': 'application/json'}
        r = req.post('https://againstlolodds.com/api/calc/', headers=headers, json=body)
        print(r.status_code)
        return '100%'
