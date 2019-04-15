import sys
import psutil
import time
from pathlib import Path
from watchdog import events
from watchdog.observers import Observer


class Lock:

    def __init__(self, path: Path):
        self.path = path

        self.data = {
            'name': None,
            'id': None,
            'port': None,
            'password': None,
            'protocol': None
        }

    def load(self) -> dict:
        if self.path.exists():
            data = self.path.read_text().split(':')
            self.data = {k: v for k, v in zip(self.data, data)}

        else:
            self.data = {k: None for k in self.data}

        return self.data


class LeagueClient:
    name = "LeagueClient"

    def __init__(self):
        self.name += '.exe' if sys.platform.startswith('win') else '.app'
        self.reset()

    def reset(self):
        self.process = self.__get_process()
        self.lock = self.__get_lock()

    def __get_process(self) -> psutil.Process:
        for p in psutil.process_iter():
            if self.name == p.name():
                return p

    def __get_lock(self) -> Lock:
        if self.process is None:
            return

        for file in self.process.open_files():
            if file.path.endswith('lockfile'):
                return Lock(Path(file.path))

    def wait(self):
        while not self.ready:
            self.reset()
            time.sleep(1)

    @property
    def ready(self) -> bool:
        return bool(self.process and self.lock)


class Connector(events.FileSystemEventHandler):
    address = '127.0.0.1'
    username = 'riot'

    def __init__(self, *args, **kwds):
        super().__init__(*args, **kwds)

        self.client = LeagueClient()
        self.observer = Observer()

    def __is_lock_event(self, event: events.FileSystemEvent):
        return all((
            not event.is_directory,
            Path(event.src_path) == self.client.lock.path
        ))

    def start(self):
        self.client.wait()
        self.update()

        self.observer.schedule(self, str(self.client.lock.path.parent))
        self.observer.start()

    def on_any_event(self, event):
        if self.__is_lock_event(event):
            self.update()

    def update(self):
        self.__dict__.update(self.client.lock.load())
