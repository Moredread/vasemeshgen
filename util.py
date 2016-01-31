def approx_equal(a, b, precision=1e-10):
    """
    >>> approx_equal(1.0, 1.0)
    True
    >>> approx_equal(1.0, 2.0)
    False
    >>> approx_equal(1.0, -1.0)
    False
    >>> import math
    >>> approx_equal(math.sqrt(2), 1.4142135623)
    True
    >>> approx_equal(math.sqrt(2), 1.414, precision=1e-3)
    True
    >>> approx_equal(math.sqrt(2), 1.41, precision=1e-3)
    False
    """
    return abs(a - b) <= precision