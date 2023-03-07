import math


def norm_pdf(x, mean=5, sd=2):
    var = float(sd) ** 2
    denom = (2 * math.pi * var) ** .5
    num = math.exp(-(float(x) - float(mean)) ** 2 / (2 * var))
    return num / denom * 3

