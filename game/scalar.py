
class Scalar(object):
    def __init__(self, current, max=None, min=None):
        if max is None:
            self.max = float(current)
        else:
            self.max = float(max)

        if min is None:
            self.min = float(0)
        else:
            self.min = float(min)

        if self.max < self.min:
            self.min, self.max = self.max, self.min

        self.set(current)

    def set(self, value):
        if value > self.max:
            value = self.max

        if value < self.min:
            value = self.min

        self.value = float(value)
        self._calc_fraction()

    def _calc_fraction(self):
        numerator = self.value - self.min
        denominator = self.max - self.min

        self.fraction = numerator / denominator