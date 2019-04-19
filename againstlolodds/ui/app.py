from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ListProperty
from ..session import Session


class Player(BoxLayout):
    pass


class TeamList(BoxLayout):

    members = ListProperty()

    def on_members(self, *args):
        self.team.clear_widgets()
        for d in self.members:
            player = Player()
            player.name = self.parent.parent.parent.session.get_summoner_name(
                str(d['summonerId'])
            ) or 'Bot'
            player.champion = str(d['championId'] or 'Unknown')

            self.team.add_widget(player)


class MainPage(Screen):

    def __init__(self, *args, **kwds):
        super().__init__(*args, **kwds)

        Clock.schedule_interval(self.refresh, 1)

    def refresh(self, *args):
        self.session.conn.update()
        team = self.ids['team']
        enemy = self.ids['enemy']
        curr = self.session.get_current()

        if curr is not None:
            self.manager.current = 'main'
            team.members = curr['myTeam']
            enemy.members = curr['theirTeam']


class LoadingPage(Screen):
    pass


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
