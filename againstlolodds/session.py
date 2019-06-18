import json
import webbrowser
import io
import requests as req
import gzip
from lcu_connectorpy import Connector
from operator import itemgetter
from kivy.core.image import Image as CoreImage


SITE_URL = 'https://againstlolodds.com/'
# SITE_URL = 'http://127.0.0.1:8080/'


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
        return r

    def start(self):
        self.conn.start()

    def get_summoner_name(self, id: str):
        return self.__request(f'/lol-summoner/v1/summoners/{id}', 'displayName')

    def get_champion_icon(self, champion_id):
        champion = self.get_all_champions().get(champion_id)
        if champion is None:
            return

        icon = champion['icon']
        if not isinstance(icon, CoreImage):
            data = io.BytesIO(self.__request(icon).content)
            icon = CoreImage(data, ext='png')
            champion['icon'] = icon

        return icon

    def get_champion_name(self, champion_id: str):
        champion = self.get_all_champions().get(champion_id)
        return champion['name'] if champion else None

    def get_all_champions(self):
        if not self._champion_cache:
            id = self.get_current_summonerid()
            champions = self.__request(
                f"/lol-champions/v1/inventories/{id}/champions"
            ).json()

            self._champion_cache.update({
                champion['id']: {
                    'name': champion['name'],
                    'icon': champion['squarePortraitPath']
                } for champion in champions})

        return self._champion_cache

    def get_current_session(self) -> dict:
        return self.__request('/lol-champ-select/v1/session')

    def get_current_summonerid(self):
        return self.__request(
            '/lol-summoner/v1/current-summoner', 'summonerId'
        )

    def calculate(self, team, enemy):
        players = json.dumps({
            'team': [{
                'summonerName': player.name,
                'role': player.role,
                'champion': player.champion,
                'id': player.summoner_id
            } for player in team],

            'enemy': [{
                'role': player.role,
                'champion': player.champion,
            } for player in enemy],
        })
        players = gzip.compress(bytes(players, 'utf-8'))
        webbrowser.open(SITE_URL + f'calculate/{players}')
