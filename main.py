import cmd_args_parser
import task
import solver

if __name__ == '__main__':
    try:
        command = tuple(cmd_args_parser.parse())
    except cmd_args_parser.ParseException as error:
        print("Incorrect parameters:", error, "\nYou can get more information using the command 'twineq --help'")
        exit(0)
    if command[0] == cmd_args_parser.InputRequestType.CREATE_TASK_FILE:
        if len(command) == 1:
            task.Task.create_task_file()
        else:
            task.Task.create_task_file(command[1])
    elif command[0] == cmd_args_parser.InputRequestType.SOLVE:
        try:
            if len(command) == 1:
                data = task.Task()
            else:
                data = task.Task(command[1])
        except task.TaskFileParseException as error:
            print("Incorrect task file:", error)
            exit(0)
        solver = solver.SolverFFT(data)
        res = solver.solve()
        res.save_to_file(data.res_file_path)
    elif command[0] == cmd_args_parser.InputRequestType.HELP:
        print("The developer of this program needs help himself.\n"
              "(function --help not implemented yet)")
    else:
        raise Exception('logic error')
