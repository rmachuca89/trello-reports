import click

from . import __version__


@click.command()
@click.version_option(version=__version__)
def main():
    """Main entrypoint for the trello-reports CLI."""
    click.echo("Hello, world!")
