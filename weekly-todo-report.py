#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Weekly tasks done summary.
This report generates a summary from all the tasks in the "Done" list
under the TODO-List Trello Board.
"""
import os
from trello import TrelloClient

s_client = TrelloClient(
    api_key=os.environ['TRELLO_API_KEY'],
    api_secret=os.environ['TRELLO_API_SECRET'],
)

o_client = TrelloClient(
    api_key=os.environ['TRELLO_API_KEY'],
    api_secret=os.environ['TRELLO_API_SECRET'],
    token=os.environ['TRELLO_OATH_TOKEN'],
    token_secret=os.environ['TRELLO_OATH_SECRET']
)

def get_todo_board():
    """Return TODO List Board ID."""
    all_boards = s_client.list_boards()
    todo_board_id = None

    for board in all_boards:
        print(board.name)

    return todo_board_id

if __name__ == "__main__":
    get_todo_board()
