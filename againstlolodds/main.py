import requests as req
import time
from lcu_connectorpy import Connector

port = 56443
url = f'https://127.0.0.1:{port}'


headers = {
    # 'Authorization': 'Basic cmlvdDpSWTFMQXhYRUdHdDl6NmV6UVpDZS1n',
    'Accept': 'application/json'
}


def get_session(conn):
    return req.get(
        f'{conn.url}/lol-champ-select/v1/session',
        auth=conn.auth,
        headers=headers,
        verify=False
    )


def parse_players(team: dict) -> dict:
    return {player['championId']: player['summonerId'] for player in team}


def parse_session(r: dict) -> dict:
    return {
        'team': parse_players(r['myTeam']),
        'enemy': parse_players(r['theirTeam'])
    }


def wait_for_session(conn) -> dict:
    while True:
        r = get_session(conn)
        if r.status_code != 200:
            time.sleep(1)
            continue

        return r.json()


def get_all_players(conn):
    session = wait_for_session(conn)
    while True:
        time.sleep(1)
        yield parse_session(session)


def main():
    conn = Connector()
    conn.start()

    for players in get_all_players(conn):
        print(json.dumps(players, indent=4))
