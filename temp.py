from more_itertools import chunked
import json
import re

with open('foo.txt') as fp:
    champions = fp.read()


with open('res/winrates.json') as fp:
    winrates = json.load(fp)


data = re.findall(r'(\d+)|(".+")', champions)


def f():
    for match in data:
        for x in match:
            if x:
                yield x


d = {int(k): v.replace('"', '') for k, v in chunked(f(), 2)}

# with open('res/champions.json', 'w+') as fp:
#     json.dump(d, fp, indent=4)

print(set(winrates) - set(d.values()))