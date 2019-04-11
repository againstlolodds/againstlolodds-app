import requests as req

port = 55234

r = req.get(f'127.0.0.1:{port}/lol-lobby/v1/lobby/availability')

print(r.status, r.json)
