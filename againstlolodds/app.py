import json
from threading import Thread
from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.properties import StringProperty, ListProperty, ObjectProperty

from pathlib import Path
from againstlolodds.session import Session
from requests.exceptions import ConnectionError
from lcu_connectorpy.connect import RestartRequiredError


RES = Path(__file__).parent.with_name('res')
ROLES = RES / 'roles'

WINRATES_FP = RES / 'winrates.json'
WINRATES = json.loads(WINRATES_FP.read_text())


class Role(Button):
    name = StringProperty()
    files = {fp.stem: fp for fp in ROLES.iterdir()}
    root_btn = None

    def on_name(self, *args):
        image_fp = self.files.get(self.name) or self.files['unknown']
        self.image.source = str(image_fp)
        self.image.reload()

    def on_release(self, *args):
        if self.root_btn is not None:
            return

        def switch(btn):
            btn.root_btn.name = name
            self.dropdown.dismiss()

        self.dropdown = DropDown()
        for name, fp in self.files.items():
            if name == self.name:
                continue

            role = Role(size_hint=(None, None))
            role.name = name
            role.size = self.size
            role.root_btn = self
            role.bind(on_release=switch)
            self.dropdown.add_widget(role)

        self.dropdown.open(self)


class Player(BoxLayout):
    """
    This uses old fashion properties instead of the Kivy ones
    because of some timing issues with Session. Not that it doesn't
    work, I just don't want to deal with it.
    """

    _summoner_id = ''
    _champion_id = ''

    def __init__(self, data, session):
        super().__init__()
        self.session = session

        self.summoner_id = data['summonerId']
        self.update(data)

    def __get_name(self):
        return self.session.get_summoner_name(
            self.summoner_id
        ) or ''

    def __get_champion(self):
        return self.session.get_champion_name(
            self.champion_id
        ) or ''

    def update(self, data):
        if self.champion_id != data['championId']:
            self.champion_id = data['championId']

    def get_roles(self):
        data = WINRATES.get(self.champion, {})
        return [v for k, v in data.items() if 'role' in k]

    @property
    def role(self):
        return self.display.role.name

    @role.setter
    def role(self, val):
        self.display.role.name = val

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
        if self.champion:
            self.icon.clear_widgets()
            icon = self.session.get_champion_icon(self.champion_id)
            image = Image(
                texture=icon.texture,
                pos=self.icon.pos,
            )
            self.icon.add_widget(image)
        else:
            self.icon.clear_widgets()


class PlayerList(BoxLayout):

    members = ListProperty()

    def update(self, members):
        bench = self.members.copy()

        def find(id):
            for i, player in enumerate(bench):
                if player.summoner_id == id:
                    return bench.pop(i)

        for mem in members:
            id = mem['summonerId']
            player = find(id)
            if player is None:
                self.add_player(mem)
            else:
                player.update(mem)
        # Clear leftover
        for player in bench:
            self.team.remove_widget(player)
            self.members.remove(player)
        self.sort_roles()

    def add_player(self, data):
        player = Player(data, self.session)
        self.members.append(player)
        self.team.add_widget(player)

    def sort_roles(self):

        def map_roles():
            for member in self.members:
                yield member, member.get_roles()

        # Doesn't account for a champion that has all its
        # roles already taken.
        taken = set()
        for member, roles in sorted(map_roles(), key=lambda x: len(x[1])):
            for role in roles:
                if role not in taken:
                    member.role = role
                    taken.add(role)
                    break


class MainPage(Screen):
    """
    A hot bowl of spaghetti that somehow works.
    """

    session = ObjectProperty(None)

    def __init__(self, *args, **kwds):
        super().__init__(*args, **kwds)

        Clock.schedule_once(self.connect)

    def connect(self, *args):
        try:
            self.session = Session()
            self.manager.current = 'loading'
            Clock.schedule_once(self.begin, -1)
        except RestartRequiredError:
            self.manager.current = 'restart'
            Clock.schedule_once(self.connect, 5)

    def begin(self, *args):
        if not self.session.conn.connected:
            # `client.reset` is expensive and blocks the animation,
            # so we put it in a different thread and
            # pretend we solved the problem.
            Thread(target=self.session.conn.client.reset).start()
            Clock.schedule_once(self.begin, 5)
            return

        self.session.start()
        Clock.schedule_interval(self.refresh, 1)

    def refresh(self, *args):
        try:
            curr = self.session.get_current_session()
        except RestartRequiredError:
            curr = None
            self.manager.current = 'restart'
        except ConnectionError:
            import sys
            sys.exit()

        if curr is not None:
            curr = curr.json()
            self.manager.current = 'main'
            self.ids['team'].update(curr['myTeam'])
            self.ids['enemy'].update(curr['theirTeam'])


class LoadingPage(Screen):
    resdir = RES


class RestartPage(Screen):
    pass


class Manager(ScreenManager):
    pass


class ManagerPage(BoxLayout):
    pass


class Result(BoxLayout):
    pass


class AgainstLoLOddsApp(App):
    def build(self):
        return ManagerPage()
