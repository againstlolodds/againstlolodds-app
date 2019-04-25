# Against LoL Odds
----------------

**Requires python >= 3.6**

## Setup

### Depend: [Poetry](https://poetry.eustace.io/docs/#installation)

```
python -m poetry install  # --no-dev for release
```

## Run
Kivy uses some external dependencies, review the [installation docs](https://kivy.org/doc/stable/gettingstarted/installation.html) if you run into any issues. It's usually a problem with the virtual environment, see below for how to disable it.
```
python -m poetry run start
```

## Building Binaries
*Dev dependencies need to be installed.*
```
python -m poetry build
```
If this doesn't work, try disabling the virtual environment.
```
python -m poetry config settings.virtualenvs.create false
```
You'll need to delete the existing virtual env too. If that doesn't work, [good luck](https://kivy.org/doc/stable/gettingstarted/packaging.html).


### Author
Noah Corona | noah@coronasoftware.net