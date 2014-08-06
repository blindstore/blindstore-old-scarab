import time
import numpy


class Benchmark:
    def __init__(self, func):
        self.func = func

    def run(self, iterations, verbose=False, skip=1):
        results = []
        for i in range(iterations):
            a = time.clock()
            self.func()
            b = time.clock()
            diff = b - a
            results.append(diff)
            if verbose and i % skip == 0:
                print('iteration={0}/{1} time={2} s'.format(i + 1, iterations, diff))

        avg = numpy.mean(results)
        std = numpy.std(results)
        med = numpy.median(results)

        if verbose:
            print('Average :', avg)
            print('Median  :', med)
            print('Std dev :', std)

        return avg, std, med, results

    def run_precise(self, iterations, verbose=False):
        a = time.clock()
        for i in range(iterations):
            self.func()
        b = time.clock()
        diff = b - a
        avg = diff / iterations
        if verbose:
            print('Average :', avg)
        return avg