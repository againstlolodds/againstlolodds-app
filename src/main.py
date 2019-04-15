import requests as req
import json
import time

port = 56443
url = f'https://127.0.0.1:{port}'


headers = {
    'Authorization': 'Basic cmlvdDpSWTFMQXhYRUdHdDl6NmV6UVpDZS1n',
    'Accept': 'application/json'
}


def get_session():
    return req.get(
        f'{url}/lol-champ-select/v1/session',
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


def wait_for_session() -> dict:
    while True:
        r = get_session()
        if r.status_code != 200:
            time.sleep(1)
            continue

        return r.json()


def get_all_players():
    session = wait_for_session()
    while True:
        time.sleep(1)
        yield parse_session(session)


def main():
    for players in get_all_players():
        print(json.dumps(players, indent=4))
