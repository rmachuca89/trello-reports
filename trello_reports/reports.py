"""
Generate a weekly report of all tasks completed in the "Done" list
of the "TODO List" Trello board.

This script requires the following environment variables to be set:
  - TRELLO_API_KEY: Your Trello API key.
  - TRELLO_API_SECRET: Your Trello API secret.
"""

from dataclasses import dataclass
import os
from typing import LiteralString

from trello import TrelloClient, exceptions
from trello.board import Board
from trello.card import Card
from trello.trellolist import List

TODO_BOARD_NAME = "TODO List"
TODO_LIST_NAME = "Done"
TRELLO_API_KEY_ENV_VAR_NAME = "TRELLO_API_KEY"
TRELLO_API_SECRET_ENV_VAR_NAME = "TRELLO_API_SECRET"
ILLEGALSTATEERROR_MSG: LiteralString = (
    f"{TRELLO_API_KEY_ENV_VAR_NAME} and {TRELLO_API_SECRET_ENV_VAR_NAME}"
    " environment variables must be set."
)


def create_trello_client(token=None, token_secret=None) -> TrelloClient:
    """
    Create a TrelloClient instance.

    Returns:
        A TrelloClient instance.
    """
    TRELLO_API_KEY: str | None = os.environ.get(TRELLO_API_KEY_ENV_VAR_NAME)
    TRELLO_API_SECRET: str | None = os.environ.get(TRELLO_API_SECRET_ENV_VAR_NAME)

    if not TRELLO_API_KEY or not TRELLO_API_SECRET:
        raise IllegalStateError(ILLEGALSTATEERROR_MSG)

    return TrelloClient(
        api_key=TRELLO_API_KEY,
        api_secret=TRELLO_API_SECRET,
        token=token,
        token_secret=token_secret,
    )


def get_done_cards(client: TrelloClient) -> list[Card]:
    my_todo_board: Board | None = _get_todo_board(client)
    if not my_todo_board:
        raise BoardNotFoundError(
            TODO_BOARD_NAME,
            f"'{TODO_BOARD_NAME}' board not found.",
        )

    return _get_todo_done_list_cards(my_todo_board)


def _get_todo_board(trello_client: TrelloClient) -> Board | None:
    """
    Return the Trello TODO_BOARD_NAME board object.

    Returns:
        The Trello  TODO_BOARD_NAME board object, or None if not found.
    """
    try:
        all_boards: list[Board] = trello_client.list_boards()
    except exceptions.ResourceUnavailable as e:
        raise BoardsUnavailableError(e._msg, e._status)

    todo_board: Board | None = None

    for board in all_boards:
        if board.name == TODO_BOARD_NAME:
            todo_board = board
            break

    return todo_board


def _get_todo_done_list_cards(trello_board: Board) -> list[Card]:
    """
    Return all cards in the TODO_LIST_NAME list under the given Trello board.

    Returns:
        A list of Trello cards.
    """
    done_list: List | None = None
    done_cards: list[Card] = []

    todo_lists: list[List] = trello_board.list_lists()
    for trello_list in todo_lists:
        if trello_list.name == TODO_LIST_NAME:
            done_list = trello_list
            break

    if done_list:
        done_cards = done_list.list_cards()
    else:
        raise ListNotFoundError(
            TODO_LIST_NAME,
            f"'{TODO_LIST_NAME}' list not found under '{TODO_BOARD_NAME}' board.",
        )

    return done_cards


class IllegalStateError(ValueError):
    pass


@dataclass
class BoardsUnavailableError(Exception):
    msg: str
    http_response: int


@dataclass
class BoardNotFoundError(Exception):
    board_name: str
    msg: str


@dataclass
class ListNotFoundError(Exception):
    list_name: str
    msg: str


def _test_only_set_todo_board_name(new_name: str):
    # TODO(#15): Get from configuration object, and remove this func.
    global TODO_BOARD_NAME
    TODO_BOARD_NAME = new_name


def _test_only_get_todo_board_name() -> str:
    # TODO(#15): Get from configuration object, and remove this func.
    return TODO_BOARD_NAME
