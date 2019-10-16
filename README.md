# Against LoL Odds
----------------
The companion app for [AgainstLoLOdds].

Download the latest version [here](https://againstlolodds.com/companion).

# Usage

This app automates the data entry required to make win chance predictions on the [AgainstLoLOdds] site.

It accomplishes this through the provided [game client API](https://developer.riotgames.com/docs/lol#league-client).
This does not violate Riot ToS (there is no risk of getting in trouble).

## Instructions

1. Launch the companion app and your LoL client. If it's your first time it will ask you to restart your client. Do that now.
2. Queue for a ranked 5v5 game normally. The companion app will detect the match as soon as the selection phase begins.
3. Wait for everyone to pick their champions. It will try to guess player roles; you can set these manually as needed.
4. Click the "Calculate" button in the companion app. This will open the [AgainstLoLOdds calculation page](https://againstlolodds.com/calculate) in your default web browser with all the necessary fields populated.
5. Click the "Calculate" button on the website.
6. Dodge when your win chance is below the first arrow if it's your first time, or below the second arrow if it's your second time.
7. Repeat steps 2-7 as needed. Remember to wait 16 hours after your second dodge before dodging again.

## Support

If you have any questions, please email the author: [noah@coronasoftware.net](mailto:noah@coronasoftware.net).

# Development
Pull requests are welcome!

## Dependencies
- [Python >=3.6](https://www.python.org/downloads/)
- [Poetry](https://poetry.eustace.io/docs/#installation)

## Setup
Run this command:

    python -m poetry install  # `--no-dev` for release

## Run
Kivy uses external dependencies. Review the [installation docs](https://kivy.org/doc/stable/gettingstarted/installation.html) if you experience any issues.

    python -m poetry run start

## Building Binaries
Building requires dev dependencies.

    python -m poetry build

If this doesn't work, try disabling the virtual environment first.

    python -m poetry config settings.virtualenvs.create false
    python -m poetry build

# Author
[Noah Corona](mailto:noah@coronasoftware.net)

[<img src="https://coronasoftware.net/s/sLogo.png">](https://coronasoftware.net)

[AgainstLoLOdds]: https://againstlolodds.com
