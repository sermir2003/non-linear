import numpy as np
from task import Task
import auxiliary_math as aux_math
import progress_counter


class Result:
    def __init__(self):
        pass

    def save_to_file(self, filename):
        with open(filename, 'w') as file_out:
            for item in zip(np.linspace(0, self.radius, self.nodes, endpoint=False), self.C):
                print("{:.8f} {:.8f}".format(item[0], item[1]), file=file_out)


class SolverFFT(object):
    def __init__(self, data: Task):
        self.N = 0
        self.data = data
        n = self.data.nodes
        self.scale = np.linspace(0, self.data.radius, self.data.nodes, endpoint=False)
        self.m = np.vectorize(self.data.kernels.m)(self.scale)
        self.w = np.vectorize(self.data.kernels.w)(self.scale)
        self.mC = np.zeros(n)
        self.wC = np.zeros(n)
        self.CwC = np.zeros(n)

        m_norm = aux_math.int_dot_norm(self.m, self.data.dim, self.scale)
        self.m = self.m * (self.data.b / m_norm)
        w_norm = aux_math.int_dot_norm(self.w, self.data.dim, self.scale)
        self.w = self.w * (self.data.s / w_norm)

        self.C = self.w.copy()

        tmp_m = self.m.copy()
        tmp_w = self.w.copy()
        if self.data.dim == 2:
            pass  # Do not know
        elif self.data.dim == 3:
            tmp_m = np.multiply(tmp_m, self.scale) * (4 * np.pi)
            tmp_w = np.multiply(tmp_w, self.scale) * (4 * np.pi)
        self.fft_m = np.fft.rfft(tmp_m)
        self.fft_w = np.fft.rfft(tmp_w)

    def solve(self):
        b = self.data.b
        d = self.data.d
        s = self.data.s
        alpha = self.data.alpha
        beta = self.data.beta
        gamma = self.data.gamma
        progress = progress_counter.ProgressCounter('Calculation')
        for iteration in range(1, self.data.iter + 1):
            progress.update_progress(iteration / self.data.iter)
            self.N = (self.data.b - self.data.d) / (
                    aux_math.int_dot_prod(self.C, self.w, self.data.dim, self.scale) + self.data.s)
            self.recalculate_conv()

            numerator = np.add(self.wC, self.CwC)
            numerator *= -self.N * (beta + gamma) / (alpha + gamma)
            numerator = np.add(numerator, self.mC)
            numerator = np.subtract(numerator, self.w)
            m_div_N = self.m / self.N
            numerator = np.add(numerator, m_div_N)
            denominator = self.w + d + alpha * (b - d) / (alpha + gamma) + beta * s
            self.C = np.divide(numerator, denominator)
        progress.finish_action()
        res = Result()
        res.N = self.N
        res.C = np.vectorize(lambda x: (x + 1) * self.N * self.N)(self.C)
        res.dim = self.data.dim
        res.nodes = self.data.nodes
        res.radius = self.data.radius
        return res

    def recalculate_conv(self):
        w_mult_C = np.multiply(self.w, self.C)
        if self.data.dim == 2:
            pass  # Do not know
        elif self.data.dim == 3:
            w_mult_C = np.multiply(w_mult_C, self.scale) * (4 * np.pi)

        fft_w_mult_C = np.fft.rfft(w_mult_C)
        fft_C = np.fft.rfft(self.C)
        self.mC = self.fft_conv(self.fft_m, fft_C)
        self.wC = self.fft_conv(self.fft_w, fft_C)
        self.CwC = self.fft_conv(fft_w_mult_C, fft_C)

    def fft_conv(self, fft_a, fft_b):
        n = self.data.nodes
        fft = np.multiply(fft_a, fft_b)
        conv = np.fft.irfft(fft, n)
        return conv * (self.data.step / (2 * n))
