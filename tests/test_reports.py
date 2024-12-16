from http import HTTPStatus
import os
from unittest import mock

import pytest
from trello import TrelloClient, Board, List, Card, exceptions

from trello_reports import reports


def test_create_trello_client_succeeds():
    result: TrelloClient = reports.create_trello_client()

    assert result.api_key == os.environ["TRELLO_API_KEY"]
    assert result.api_secret == os.environ["TRELLO_API_SECRET"]


def test_create_trello_client_no_envvars_raises_error():
    os.environ.pop("TRELLO_API_KEY")
    os.environ.pop("TRELLO_API_SECRET")
    with pytest.raises(reports.IllegalStateError):
        reports.create_trello_client()


def test_get_done_cards_succeeds():
    client_mock = mock.create_autospec(TrelloClient)
    board1: Board = Board(name="Something")
    board2: Board = Board(name="Whatever")
    board4: Board = Board(name="Maybe")

    todo_board_mock: Board = mock.create_autospec(Board)
    todo_board_mock.name = reports.TODO_BOARD_NAME
    done_list_mock: List = mock.create_autospec(List)
    done_list_mock.name = reports.TODO_LIST_NAME
    done_list_mock.board = todo_board_mock
    done_list_mock.client = client_mock

    task1: Card = Card(done_list_mock, card_id=1, name="Task 1")
    task2: Card = Card(done_list_mock, card_id=2, name="Task 2")

    response_boards: list[Board] = [board1, board2, todo_board_mock, board4]
    client_mock.list_boards.return_value = response_boards

    todo_board_mock.list_lists.return_value = list([done_list_mock])
    done_list_mock.list_cards.return_value = list([task1, task2])

    result: list[Card] = reports.get_done_cards(client_mock)

    assert client_mock.list_boards.call_count == 1
    expected: list[Card] = [task1, task2]
    assert len(result) == len(expected)
    assert expected.sort(key=lambda x: x.id) == result.sort(key=lambda x: x.id)


def test_get_done_cards_no_done_list_raises_error():
    client_mock = mock.create_autospec(TrelloClient)
    board1: Board = Board(name="Something")
    board2: Board = Board(name="Whatever")
    board4: Board = Board(name="Maybe")

    todo_board_mock: Board = mock.create_autospec(Board)
    todo_board_mock.name = reports.TODO_BOARD_NAME
    todo_board_mock.client = client_mock

    list1: List = List(board=todo_board_mock, list_id=1, name="List 1")
    list2: List = List(board=todo_board_mock, list_id=2, name="List 2")
    list3: List = List(board=todo_board_mock, list_id=3, name="List 3")

    response_boards: list[Board] = [board1, board2, todo_board_mock, board4]
    client_mock.list_boards.return_value = response_boards

    todo_board_mock.list_lists.return_value = [list1, list2, list3]

    with pytest.raises(reports.ListNotFoundError):
        reports.get_done_cards(client_mock)


def test_get_done_cards_no_todo_board_raises_error():
    client_mock = mock.create_autospec(TrelloClient)
    board1: Board = Board(name="Something")
    board2: Board = Board(name="Whatever")
    board4: Board = Board(name="Maybe")
    response_boards: list[Board] = [board1, board2, board4]
    client_mock.list_boards.return_value = response_boards

    with pytest.raises(reports.BoardNotFoundError):
        reports.get_done_cards(client_mock)


def test_generate_report_with_list_boards_error_raises_error():
    client_mock = mock.create_autospec(TrelloClient)
    msg: str = "Bad request"
    http_response = mock.Mock()
    http_response.status_code = HTTPStatus.FORBIDDEN
    client_mock.list_boards.side_effect = exceptions.ResourceUnavailable(
        msg=msg, http_response=http_response
    )

    with pytest.raises(reports.BoardsUnavailableError):
        reports.get_done_cards(client_mock)
