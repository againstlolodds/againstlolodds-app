import json
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ListProperty, DictProperty
from pathlib import Path
from .session import Session


RES = Path(__file__).parent.with_name('res')
WINRATES_FP = RES / 'winrates.json'
with WINRATES_FP.open() as fp:
    WINRATES = json.load(fp)


class AttrLabel(Label):
    pass


class Role(Label):

    @property
    def image_path(self):
        return str(RES / 'images' / (self.name.upper() + '.png'))


class Player(BoxLayout):

    def __init__(self, data, session):
        super().__init__()

        self.session = session
        self.summoner_id = data['summonerId']
        self.champion_id = data['championId']
        self.role = WINRATES.get(self.champion)['role1']

    def __get_name(self):
        return self.session.get_summoner_name(
            self.summoner_id
        ) or 'Bot'

    def __get_champion(self):
        return self.session.get_champion_name(
            self.champion_id, summoner_id=self.summoner_id
        ) or 'Unknown'

    def update(self, data):
        if self.champion_id != data['championId']:
            self.champion_id = data['championId']
        self.role = WINRATES.get(self.champion)['role1']

    def 

    @property
    def summoner_id(self):
        return self._summoner_id

    @summoner_id.setter
    def summoner_id(self, val):
        self._summoner_id = val
        self.name = self.__get_name()

    @property
    def champion_id(self):
        return self._champion_id

    @champion_id.setter
    def champion_id(self, val):
        self._champion_id = val
        self.champion = self.__get_champion()


class Enemy(Player):
    pass


class Friendly(Player):
    pass


class Header(Label):
    pass


class PlayerList(BoxLayout):

    member_cls = Player

    members = DictProperty()
    headers = ListProperty()

    def update(self, members):
        for mem in members:
            id = mem['summonerId']
            player = self.members.get(id)
            if player is None:
                self.add_player(mem)
            else:
                player.update(mem)

    def add_player(self, data):
        player = self.member_cls(data, self.session)
        self.members[player.summoner_id] = player
        self.team.add_widget(player)

    def on_headers(self, *args):
        for name in self.headers:
            self.ids['header'].add_widget(Header(text=name))


class TeamList(PlayerList):
    member_cls = Friendly


class EnemyList(PlayerList):
    member_cls = Enemy


class MainPage(Screen):

    def __init__(self, *args, **kwds):
        super().__init__(*args, **kwds)

        Clock.schedule_interval(self.refresh, 1)

    def refresh(self, *args):
        self.session.conn.update()
        curr = self.session.get_current_session()
        if curr is None:
            return
        self.manager.current = 'main'

        self.ids['team'].update(curr['myTeam'])
        self.ids['enemy'].update(curr['theirTeam'])


class LoadingPage(Screen):
    resdir = RES


class Manager(ScreenManager):
    pass


class ManagerPage(BoxLayout):
    pass


class Result(BoxLayout):
    pass


class AgainstLoLOddsApp(App):

    def build(self):
        self.session = Session()
        return ManagerPage()
