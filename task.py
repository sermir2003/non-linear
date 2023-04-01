import json
import kernels

task_file_default_name = "TaskFile.json"
result_file_default_name = "plot.txt"


class TaskFileParseException(Exception):
    pass


markup_of_input_data = [
    ('dim', 'Environment dimensionality', 1),
    ('radius', 'Integration area radius', 20),
    ('iter', 'Iteration count', 1000),
    ('nodes', 'Grid count', 5001),
    ('alpha', 'alpha', 1),
    ('beta', 'beta', 1),
    ('gamma', 'gamma', 1),
    ('d', 'd', 0),
    ('s', 'd\'', 1),
    ('b', 'b', 1),
    ('res_file_path', 'Path to result file', result_file_default_name),
    ('precision', 'Signs after decimal point', 8),
    ('kernels', 'Kernels', kernels.GaussSimpleKernels(1).__dict__())
]


class Task(object):
    @staticmethod
    def create_task_file(filename=task_file_default_name):
        file_content_dict = {}
        for attribute in markup_of_input_data:
            file_content_dict[attribute[1]] = attribute[2]
        file_content = json.dumps(file_content_dict, sort_keys=True, indent=4)
        with open(filename, 'w') as task_file:
            print(file_content, file=task_file)

    def __init__(self, filename=task_file_default_name):
        # This is intended for static code analyzers and guarantees the existence of the necessary fields
        self.dim = None
        self.radius = None
        self.iter = None
        self.nodes = None
        self.alpha = None
        self.beta = None
        self.gamma = None
        self.d = None
        self.s = None
        self.b = None
        self.res_file_path = None
        self.precision = None
        self.kernels = None

        with open(filename) as task_file:
            json_input = json.load(task_file)
            for attribute in markup_of_input_data:
                field_name = attribute[0]
                user_name = attribute[1]
                try:
                    value = json_input[user_name]
                except KeyError:
                    raise TaskFileParseException('Incorrect TaskFile: {} is missed'.format(user_name))
                if field_name == 'kernels':
                    self.kernels = kernels.kernel_by_description(value)
                else:
                    setattr(self, field_name, value)
                json_input.pop(user_name)
            if len(json_input) != 0:
                print('WARNING! Redundant data in TaskFile:\n{}\nHowever, this does not interfere with the '
                      'execution\n'.format(json_input))
        self.step = self.radius / self.nodes
