import math
import numpy as np
import struct

from numpy import cross, eye, dot
from scipy.linalg import expm3, norm

def rotate(input, axis, theta):
    try:
        return [rotate_v(v, axis, theta) in input]
    except TypeError:
        return rotate_v(input, axis, theta)

def rotate_v(v, axis, theta):
    """Adapted from http://stackoverflow.com/questions/6802577/python-rotation-of-3d-vector"""

    def M(axis, theta):
        return expm3(cross(eye(3), axis/norm(axis)*theta))

    return dot(M(axis, theta), v)

def rotate_z(v, theta):
    return rotate(v, np.array([0,0,1]), theta)

def rotate_z_deg(v, angle):
    """
    >>> v = np.array([1, 0, 0])
    >>> v_rot = rotate_z_deg(v, 90)
    >>> abs(v_rot[0]) < 1e-10
    True
    >>> abs(v_rot[1] - 1) < 1e-10
    True
    >>> abs(v_rot[2]) < 1e-10
    True
    """
    return rotate_z(v, angle/360.*2*math.pi)

def write_stl(triangles, name="out.stl"):
    with open(name, "wb") as f:
        f.write(struct.pack('x'*80))
        f.write(struct.pack('I',len(triangles)))

        for p1, p2, p3 in triangles:
            n_ = np.cross(p2 - p1, p3 - p1)
            n  = n_/np.linalg.norm(n_)

            f.write(struct.pack('fff', n[0], n[1], n[2]))
            for p in [p1, p2, p3]:
                f.write(struct.pack('fff', p[0], p[1], p[2]))
            f.write(struct.pack('H',0))

def triangulate(shapes):
    triangles = []

    for i in range(len(shapes) - 1):
        for j in range(len(shapes[0])):
          triangles.append([shapes[i][j], shapes[i+1][j-1], shapes[i+1][j]])
          triangles.append([shapes[i][j], shapes[i][j-1], shapes[i+1][j-1]])

    return triangles

def square(width, z=0.0):
    return regular_polygon(math.sqrt(width/2.), 4, z)

def regular_polygon(radius, n, z=0.0):
    start = np.array([radius, 0.0, z])
    angle = 360./n

    result = []
    for i in range(n):
        result.append(rotate_z_deg(start, angle*i))

    return result

def main():
    n = 20
    height = 5
    step = height/n
    result = [regular_polygon(1.0, 6, i*step) for i in range(n)]
    t = triangulate(result)
    print("Generated {} triangles".format(len(t)))
    write_stl(t)

if __name__ == "__main__":
    main()
