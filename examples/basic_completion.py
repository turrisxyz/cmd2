#!/usr/bin/env python
# coding=utf-8
"""
A simple example demonstrating how to enable tab completion by assigning a completer function to do_* commands.
This also demonstrates capabilities of the following completer methods included with cmd2:
- flag_based_complete
- index_based_complete
- delimiter_completer

For an example integrating tab completion with argparse, see argparse_completion.py
"""
import functools

import cmd2

# List of strings used with completion functions
food_item_strs = ['Pizza', 'Ham', 'Ham Sandwich', 'Potato']
sport_item_strs = ['Bat', 'Basket', 'Basketball', 'Football', 'Space Ball']

# This data is used to demonstrate delimiter_complete
file_strs = \
    [
        '/home/user/file.db',
        '/home/user/file space.db',
        '/home/user/another.db',
        '/home/other user/maps.db',
        '/home/other user/tests.db'
    ]


class BasicCompletion(cmd2.Cmd):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def do_flag_based(self, statement: cmd2.Statement):
        """Tab completes arguments based on a preceding flag using flag_based_complete
        -f, --food [completes food items]
        -s, --sport [completes sports]
        -p, --path [completes local file system paths]
        """
        self.poutput("Args: {}".format(statement.args))

    def complete_flag_based(self, text, line, begidx, endidx):
        """Completion function for do_flag_based"""
        flag_dict = \
            {
                # Tab-complete food items after -f and --food flags in command line
                '-f': food_item_strs,
                '--food': food_item_strs,

                # Tab-complete sport items after -s and --sport flags in command line
                '-s': sport_item_strs,
                '--sport': sport_item_strs,

                # Tab-complete using path_complete function after -p and --path flags in command line
                '-p': self.path_complete,
                '--path': self.path_complete,
            }

        return self.flag_based_complete(text, line, begidx, endidx, flag_dict=flag_dict)

    def do_index_based(self, statement: cmd2.Statement):
        """Tab completes first 3 arguments using index_based_complete"""
        self.poutput("Args: {}".format(statement.args))

    def complete_index_based(self, text, line, begidx, endidx):
        """Completion function for do_index_based"""
        index_dict = \
            {
                1: food_item_strs,  # Tab-complete food items at index 1 in command line
                2: sport_item_strs,  # Tab-complete sport items at index 2 in command line
                3: self.path_complete,  # Tab-complete using path_complete function at index 3 in command line
            }

        return self.index_based_complete(text, line, begidx, endidx, index_dict=index_dict)

    def do_delimiter_complete(self, statement: cmd2.Statement):
        """Tab completes files from a list using delimiter_complete"""
        self.poutput("Args: {}".format(statement.args))

    # Use a partialmethod to set arguments to delimiter_complete
    complete_delimiter_complete = functools.partialmethod(cmd2.Cmd.delimiter_complete,
                                                          match_against=file_strs, delimiter='/')


if __name__ == '__main__':
    import sys
    app = BasicCompletion()
    sys.exit(app.cmdloop())
