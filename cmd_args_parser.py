import sys
from enum import Enum

import numpy as np

import task


class ParseException(Exception):
    pass


class InputRequestType(Enum):
    CREATE_TASK_FILE = 1
    SOLVE = 2
    HELP = 3


def parse():
    program_name = sys.argv[0]
    if len(sys.argv) == 1:
        raise ParseException("There are no parameters, launch is impossible.")
    elif sys.argv[1] == "newtask":
        if len(sys.argv) == 3:
            return InputRequestType.CREATE_TASK_FILE, sys.argv[2]
        elif len(sys.argv) == 2:
            return InputRequestType.CREATE_TASK_FILE,
        else:
            raise ParseException("The '{}' should be followed by the path to the file to be created "
                                 "or nothing to create a file with the default name. However, "
                                 "the number of parameters is not conducive to this.".format(program_name))
    elif sys.argv[1] == "solve":
        if len(sys.argv) == 3:
            return InputRequestType.SOLVE, sys.argv[2]
        elif len(sys.argv) == 2:
            return InputRequestType.SOLVE,
        else:
            raise ParseException(
                "The 'solve' should be followed by the path to the Task File or nothing to "
                "use a file with a default name. However, the number of parameters is not "
                "conducive to this.")
    elif sys.argv[1] == "help" or sys.argv[1] == "-h" or sys.argv[1] == "--help":
        if len(sys.argv) == 2:
            return InputRequestType.HELP,
        else:
            raise ParseException("There are too many parameters for the help command.")
    raise ParseException("Invalid key.")
