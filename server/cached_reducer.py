class CachedReducer:
    def __init__(self, func):
        self.func = func
        self.cache = {}

    def reduce(self, sequence, initial=None):
        """
        Performs the reduce operation on the given sequence.
        :param sequence: list of values to be reduced
        :param initial: initial value
        :return:
        """
        sequence = list(sequence)

        if not sequence:
            return initial

        # Now the reduce() function iterates through all the values in the same order.
        # Rearranging the values and finding the cached pairs can make the hit/miss ratio much higher.
        # TODO optimize

        while True:
            results = []
            while len(sequence) > 1:
                x = sequence.pop(0)
                y = sequence.pop(0)
                results.append(self.call(x, y))
            sequence = results + sequence  # preserve element order
            if len(sequence) == 1:
                break

        return sequence[0]

    def call(self, x, y):
        v = self.cache.get((x, y), None)
        if not v:
            v = self.func(x, y)
            self.cache[(x, y)] = v
        return v