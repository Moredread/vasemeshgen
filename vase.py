import math
import struct

import numpy as np
from numpy import cross, eye, dot
from scipy.linalg import expm3, norm


def rotate(v, axis, theta):
    """Adapted from http://stackoverflow.com/questions/6802577/python-rotation-of-3d-vector"""

    def r(axis, theta):
        return expm3(cross(eye(3), axis / norm(axis) * theta))

    return dot(r(axis, theta), v)


def rotate_z(v, theta):
    return rotate(v, np.array([0, 0, 1]), theta)


def rotate_z_deg_all(input, degrees):
    return [rotate_z_deg(v, degrees) for v in input]


def split(poly, n=2):
    for v1, v2 in zip(poly, poly[1:] + [poly[0]]):
        for i in range(n):
            yield v1 + (v2 - v1) * i / n


def rotate_z_deg(v, angle):
    """
    >>> from util import approx_equal
    >>> v = np.array([1, 0, 0])
    >>> v_rot = rotate_z_deg(v, 90)
    >>> approx_equal(v_rot[0], 0.0)
    True
    >>> approx_equal(v_rot[1], 1.0)
    True
    >>> approx_equal(v_rot[2], 0.0)
    True
    """
    return rotate_z(v, (angle % 360) / 360. * 2 * math.pi)


def write_stl(triangles, filename="out.stl"):
    with open(filename, "wb") as f:
        f.write(struct.pack('x' * 80))
        f.write(struct.pack('I', len(triangles)))

        print("Writing {} triangles to {}".format(len(triangles), filename))
        for p1, p2, p3 in triangles:
            n_ = np.cross(p2 - p1, p3 - p1)
            n = -1 * n_ / np.linalg.norm(n_)

            f.write(struct.pack('fff', n[0], n[1], n[2]))
            for p in [p1, p2, p3]:
                f.write(struct.pack('fff', p[0], p[1], p[2]))
            f.write(struct.pack('H', 0))


def triangulate(shapes):
    triangles = []

    for i in range(len(shapes) - 1):
        for j in range(len(shapes[0])):
            triangles.append([shapes[i][j], shapes[i + 1][j - 1], shapes[i + 1][j]])
            triangles.append([shapes[i][j], shapes[i][j - 1], shapes[i + 1][j - 1]])

    return triangles


def interpolate(a, b, factor):
    for x, y in zip(a, b):
        yield x + factor * (y - x)


def square(width, z=0.0):
    return n_poly(math.sqrt(width / 2.), 4, z)


def n_poly(radius, n, z=0.0):
    start = np.array([radius, 0.0, z])
    angle = 360. / n

    result = []
    for i in range(n):
        result.append(rotate_z_deg(start, angle * i))

    return result


def interpolated_pentagon_vase():
    n = 10
    height = 4
    step = height / n
    polys = [list(interpolate(n_poly(2.0, 5, i * step), n_poly(1.0, 5, i * step), i / n)) for i in range(n)]
    result = [rotate_z_deg_all(polys[i], -i * 180 / (n - 1)) for i in range(n)]
    return triangulate(result)


def twisted_pentagon_vase():
    n = 1000
    height = 4
    step = height / n
    polys = [n_poly(1.0, 5, i * step) for i in range(n)]
    result = [rotate_z_deg_all(polys[i], -i * 180 / (n - 1)) for i in range(n)]
    return triangulate(result)


def twisted_pentagon_vase_lowpoly():
    n = 10
    height = 4
    step = height / n
    polys = [split(n_poly(1.0, 5, i * step), 3) for i in range(n)]
    result = [rotate_z_deg_all(polys[i], -i * 180 / (n - 1)) for i in range(n)]
    return triangulate(result)


def main():
    write_stl(twisted_pentagon_vase(), "twisted_pentagon_vase.stl")
    write_stl(twisted_pentagon_vase_lowpoly(), "twisted_pentagon_vase_lowpoly.stl")
    write_stl(interpolated_pentagon_vase(), "interpolated_pentagon_vase.stl")


if __name__ == "__main__":
    main()
