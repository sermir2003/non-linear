import math


def kernel_by_description(descript):
    if descript['type'] == 'undefined':
        return Kernels()
    elif descript['type'] == 'Gauss simple':
        return GaussSimpleKernels(descript['sigma'])


class Kernels(object):
    def m(self, x):
        pass

    def w(self, x):
        pass

    def __dict__(self):
        return {'type': 'undefined'}


class GaussSimpleKernels(Kernels):
    def __init__(self, sigma):
        self.sigma = sigma
        self.sigma_squared = sigma * sigma

    def m(self, x):
        return math.exp(-x * x / (2 * self.sigma_squared)) / math.sqrt(2 * math.pi * self.sigma_squared)

    def w(self, x):
        return math.exp(-x * x / (2 * self.sigma_squared)) / math.sqrt(2 * math.pi * self.sigma_squared)

    def __dict__(self):
        return {'type': 'Gauss simple', 'sigma': self.sigma}
