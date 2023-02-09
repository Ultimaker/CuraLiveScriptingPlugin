import math

def nearest_radian(radian):
    degree = math.degrees(radian)
    degree = round(degree / 90) * 90
    return math.radians(degree)

print(nearest_radian(math.radians(46)))
