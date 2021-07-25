# Trello Reports

[![Tests](https://github.com/rmachuca89/trello-reports/workflows/Tests/badge.svg)](https://github.com/rmachuca89/trello-reports/actions?workflow=Tests)

Repository to interact with the [Trello API][trello_api] and generate required
reports.

Example: `python3 weekly-todo-report.py`

Weekly report to get all the cards that are under the `Done` list in my
TODO-List board.

Sample Output:

```
$ ./weekly-todo-report.py
####################
TODO List Weekly Report
Date: 2021-07-22 22:42:31.269518
####################
--------------------
Tasks Done
--------------------
Monthly Email Housekeeping
Finish Essay
Fix Computer
```

**INFO**: Current setup requires to manually install dependencies on a python
*environment as described below. Better packaging and possible upload to PyPi
*may be planned in a future release.

## Setup and Build

Project is under [poetry](https://python-poetry.org/) package and dependency
manager

```sh
$ poetry install
```

Then source the environment variables with corresponding values
(`TRELLO_API_KEY` and `TRELLO_API_SECRET`). See [this
link](https://trello.com/app-key) as a reference to generate them.

And finally run it manually with:

```sh
$ poetry run python weekly-todo-report.py
```

## Optional: Environment Auto-Configuration with `direnv`

To automate the initialization of the required ENV VARs and corresponding python
virtual environment with all dependencies installed to ineract with [Trello
API][trello_api], you can take of leverage of [`direnv`](https://direnv.net/)
and manually confmanual igure it to enable poetry virtual env auto-activiton
with the [following function amanual dded to
`~/.direnvrc`](https://github.com/direnv/direnv/wiki/Python#poetry)

For example, for a Debian `apt` based system:

```sh
$ sudo apt install direnv
$ cp .env_example .env
$ vim .env
$ direnv allow
```

The above setup allows to run within the poetry virtual environment

```
(trello-reports-L5dNkZrm-py3.9)user@host ~/code/trello-reports: ./weekly-todo-report.py
```

[trello_api]: https://developers.trello.com/
