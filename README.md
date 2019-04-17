# Trello Reports

Repository to interact with the [Trello API][trello_api] and generate required reports.

Example: `weekly-todo-report.py`

Weekly report to get all the cards that are under the `Done` list in my TODO-List board.

## Setup and Configuration

```
$ pipenv install
```

Then source the environment variables with corresponding values (`TRELLO_API_KEY` and `TRELLO_API_SECRET`).
See [this link](https://trello.com/app-key) as a reference to generate them.

## Optional Requirements

This automates the initialization of the required ENV VARs and corresponding python virtual environment
to ineract with [Trello API][trello_api], by leveraging [`direnv`](https://direnv.net/)

```
$ sudo apt install direnv
$ cp .env_example .env
$ vim .env
$ direnv allow
```

[trello_api]: https://developers.trello.com/
