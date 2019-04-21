import requests as req
from lcu_connectorpy import Connector
from operator import itemgetter


class Session:

    headers = {
       'Accept': 'application/json'
    }

    _champion_cache: dict = {}

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

    def get_champion_name(self, champion_id: str):
        return self.get_all_champions().get(champion_id)

    def get_all_champions(self):
        if not self._champion_cache:
            id = self.get_current_summonerid()
            champions = self.__request(f"/lol-champions/v1/inventories/{id}/champions")
            self._champion_cache.update({c['id']: c['name'] for c in champions})
        return self._champion_cache

    def get_current_session(self) -> dict:
        return self.__request('/lol-champ-select/v1/session')

    def get_current_summonerid(self):
        return self.__request('/lol-summoner/v1/current-summoner', 'summonerId')

    def calculate(self, team, enemy):
        # body = [
        #     [{
        #         'summonerName': member.name,
        #         'role': member.role,
        #         'champion': member.champion,
        #         'override': None
        #     } for member in team.values()],
        #     [{
        #         'role': member.role,
        #         'champion': member.champion,
        #     } for member in enemy.values()],
        #     {
        #         'region': 'na'
        #     }
        # ]
        # import json
        # headers = {'Content-Type': 'application/json'}
        # r = req.post('https://againstlolodds.com:3000/api/calc', headers=headers, data=json.dumps(body))
        # print(r.status_code)
        return 100
