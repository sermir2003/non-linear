import numpy as np


def make_jacobian(dim):
    if dim == 1:
        return lambda x: 1
    elif dim == 2:
        return lambda x: x
    elif dim == 3:
        return lambda x: x ** 2
    raise Exception('dimension is not in [1, 2, 3]')


def calc_dim_ratio(dim):
    if dim == 1:
        return 2
    elif dim == 2:
        return 2 * np.pi
    elif dim == 3:
        return 4 * np.pi
    raise Exception('dimension is not in [1, 2, 3]')


def int_dot_prod(f: np.array, g: np.array, dim, scale):
    step_size = abs(scale[1] - scale[0])
    tmp_arr = np.vectorize(make_jacobian(dim))(scale)  # 'jacobian' array
    tmp_arr = np.multiply(tmp_arr, f)
    tmp_arr = np.multiply(tmp_arr, g)
    return np.sum(tmp_arr) * step_size * calc_dim_ratio(dim)


def int_dot_norm(f: np.ndarray, dim, scale):
    step_size = abs(scale[1] - scale[0])
    return np.sum(np.multiply(np.absolute(f), np.vectorize(make_jacobian(dim))(scale))) * step_size * calc_dim_ratio(dim)
