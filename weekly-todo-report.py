#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Weekly tasks done summary.
This report generates a summary from all the tasks in the "Done" list
under the TODO-List Trello Board.
"""
import os
import datetime
from trello import TrelloClient, exceptions

s_client = TrelloClient(
    api_key=os.environ.get("TRELLO_API_KEY", ""),
    api_secret=os.environ.get("TRELLO_API_SECRET", ""),
)

o_client = TrelloClient(
    api_key=os.environ.get("TRELLO_API_KEY", ""),
    api_secret=os.environ.get("TRELLO_API_SECRET", ""),
    token=os.environ.get("TRELLO_OATH_TOKEN", ""),
    token_secret=os.environ.get("TRELLO_OATH_SECRET", ""),
)


def get_todo_board():
    """Return trello `TODO List` Board object."""
    try:
        all_boards = s_client.list_boards()
    except exceptions.ResourceUnavailable:
        print(
            "Could not establish connection. Double check your credentials and Internet connection."
        )
        exit(-1)
    todo_board = None

    for board in all_boards:
        if board.name == "TODO List":
            todo_board = board
            break

    return todo_board


def get_todo_done_list_cards(trello_board):
    """Return all open cards in the `Done` list under the `TODO List` board."""
    done_list = None
    done_cards = []

    if trello_board:
        todo_lists = trello_board.list_lists()
        for trello_list in todo_lists:
            if trello_list.name == "Done":
                done_list = trello_list
                break

    if done_list:
        done_cards = done_list.list_cards()

    return done_cards


if __name__ == "__main__":
    print("####################")
    print("TODO List Weekly Report")
    print("Date: {}".format(str(datetime.datetime.now())))
    #  print("Date: {}".format(datetime.datetime.today().strftime('%Y-%m-%d')))
    print("####################")
    my_todo_board = get_todo_board()
    #  print(my_todo_board.id)
    if not my_todo_board:
        print("`TODO List` board not found. " "Double check name and that it exists.")
        exit(1)

    print("--------------------")
    print("Tasks Done")
    print("--------------------")
    my_done_cards = get_todo_done_list_cards(my_todo_board)
    for card in my_done_cards:
        print(card.name)
