import math

def MatrixMultiplier(matrix, coords):
    x = matrix[0][0] * coords[0] + matrix[0][1] * coords[1] + matrix[0][2] * coords[2] + matrix[0][3] * coords[3]
    y = matrix[1][0] * coords[0] + matrix[1][1] * coords[1] + matrix[1][2] * coords[2] + matrix[1][3] * coords[3]
    z = matrix[2][0] * coords[0] + matrix[2][1] * coords[1] + matrix[2][2] * coords[2] + matrix[2][3] * coords[3]
    w = matrix[3][0] * coords[0] + matrix[3][1] * coords[1] + matrix[3][2] * coords[2] + matrix[3][3] * coords[3]
    if w != 0: x /= w; y /= w; z /= w
    return (x, y, z, 1)

def Radian(x):
    # converts degrees to radians
    return x * (math.pi / 180.0)

def CrossProduct(a, b):
    # finds the cross product of two vectors for calculations
    x = (a[1] * b[2] - a[2] * b[1],
         a[2] * b[0] - a[0] * b[2],
         a[0] * b[1] - a[1] * b[0],)
    return x

def DotProduct(a, b):
    # finds the dot product of two vectors for calculations
    return a[0] * b[0] + a[1] * b[1]+ a[2] * b[2]

def UnitVector(a):
    # finds the unit vector of a vector for calculations
    u = 0
    u = a[0]**2 + a[1]**2 + a[2]**2
    if u == 0: return (0, 0, 0)
    u = math.sqrt(u)
    x = a[0] / u
    y = a[1] / u
    z = a[2] / u
    return (x, y, z, 1)

def UnitVector2x1(a):
    # finds the unit vector of a vector for calculations
    u = 0
    u = a[0]**2 + a[1]**2
    if u == 0: return (0, 0)
    u = math.sqrt(u)
    x = a[0] / u
    y = a[1] / u
    return (x, y)


def SubtractVectors(a, b): return (a[0] - b[0], a[1] - b[1], a[2] - b[2])

def AddVectors(a, b): return (a[0] + b[0], a[1] + b[1], a[2] + b[2])

def MultiplyVector(a, x): return(x * a[0], x * a[1], x * a[2])

def RotationMatrixY(angle):
    # returns a rotation matrix for y by a certain angle
    m = (
        (math.cos(angle), 0, math.sin(angle), 0),
        (0, 1, 0, 0),
        (-math.sin(angle), 0, math.cos(angle), 0),
        (0, 0, 0, 1)
    )
    return m

def RotationMatrixX(angle, x, z):
    # returns a rotation matrix for relative x by a certain angle
    sin = math.sin(angle)
    cos = 1 - math.cos(angle)
    zs = z**2
    xs = x**2
    m = (
        (1 - zs * cos, -z * sin, -z * x * cos, 0),
        (z * sin, 1 - (zs + xs) * cos, -x * sin, 0),
        (z * x * cos, x * sin, 1 - xs * cos, 0),
        (0, 0, 0, 1)
    )
    return m

def PlaneLineIntersection(p, n, a, b):
    # tests if the line ab intersects with the plane with point p and normal n
    direction = SubtractVectors(b, a)
    t = DotProduct(n, SubtractVectors(p, a)) / DotProduct(n, direction)
    return AddVectors(a, MultiplyVector(direction, t))

def PointPlaneDistance(p, n, a):
    # finds the distance between a point and a plane
    n = UnitVector(n)
    return (DotProduct(a, n) - DotProduct(p, n))

# I've kind of cheated here and just copied code from my inefficient program
def YPlaneFromLine(line):
    # creates a plane parallel to the y plane that overlaps with a given line
    x = line[1][2]
    z = -line[1][0]
    d = -DotProduct((x, 0, z), line[0])
    return ((x, 0, z), d)

def XPlaneFromLine(line):
    # creates a plane perpendicular to the y plane that overlaps with a given line
    x = line[1][0] * line[1][1]
    y = -(line[1][0]**2 + line[1][2]**2)
    z = line[1][2] * line[1][1]
    d = line[0][1]*(line[1][0]**2 + line[1][2]**2) - line[1][0]*line[0][0]*line[1][1] - line[1][2]*line[0][2]*line[1][1]
    return ((x, y, z), d)