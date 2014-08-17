import time
import numpy


def benchmark(func, iterations, verbose=False, skip=1):
    results = []
    for i in range(iterations):
        a = time.clock()
        func()
        b = time.clock()
        diff = b - a
        results.append(diff)
        if verbose and i % skip == 0:
            print('iteration={0}/{1} time={2} s'.format(i + 1, iterations, diff))

    avg = numpy.mean(results)
    std = numpy.std(results)
    med = numpy.median(results)

    if verbose:
        print('Average :', avg, 's')
        print('Median  :', med, 's')
        print('Std dev :', std, 's')

    return avg, std, med, results


def benchmark_precise(func, iterations, verbose=False):
    a = time.clock()
    for i in range(iterations):
        func()
    b = time.clock()
    diff = b - a
    avg = diff / iterations
    if verbose:
        print('Average :', avg)
    return avg