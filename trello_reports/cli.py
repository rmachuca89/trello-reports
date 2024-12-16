from datetime import datetime

import click
from trello.card import Card
from trello.trelloclient import TrelloClient

from trello_reports import __version__
from trello_reports.reports import (
    BoardNotFoundError,
    IllegalStateError,
    create_trello_client,
    get_done_cards,
)


@click.command()
@click.version_option(version=__version__)
def main():
    """Main entrypoint for the trello-reports CLI."""
    try:
        client: TrelloClient = create_trello_client()
    except IllegalStateError as e:
        click.echo(e)
        exit(1)

    try:
        my_done_tasks: list[Card] = get_done_cards(client)
    except BoardNotFoundError as e:
        click.echo(e.msg)
        exit(1)

    _print_report_std(my_done_tasks)


def _print_report_std(done_cards: list[Card]):
    click.echo("####################")
    click.echo("TODO List Weekly Report")
    click.echo("Date: {}".format(str(datetime.now())))
    click.echo("####################")
    click.echo("--------------------")
    click.echo("Tasks Done")
    click.echo("--------------------")
    for card in done_cards:
        click.echo(card.name)


# Required for local debugging for Click applications.
if __name__ == "__main__":
    main()
