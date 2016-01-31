def almost_equal(a, b, precision=1e-10):
    """
    >>> almost_equal(1.0, 1.0)
    True
    >>> almost_equal(1.0, 2.0)
    False
    >>> almost_equal(1.0, -1.0)
    False
    >>> import math
    >>> almost_equal(math.sqrt(2), 1.4142135623)
    True
    >>> almost_equal(math.sqrt(2), 1.414, precision=1e-3)
    True
    >>> almost_equal(math.sqrt(2), 1.41, precision=1e-3)
    False
    """
    return abs(a - b) <= precision