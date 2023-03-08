import math


def norm_pdf(x, mean=5, sd=2):
    var = float(sd) ** 2
    denom = (2 * math.pi * var) ** .5
    num = math.exp(-(float(x) - float(mean)) ** 2 / (2 * var))
    return num / denom * 3


def get_hint(weight, tolerance=0.001):
    if abs(weight) < tolerance:
        return "🖤🖤🖤🖤🖤"

    if weight > 0:
        if weight < 0.2:
            return "💖🖤🖤🖤🖤"
        elif weight < 0.4:
            return "💖💖🖤🖤🖤"
        elif weight < 0.6:
            return "💖💖💖🖤🖤"
        elif weight < 0.8:
            return "💖💖💖💖🖤"
        else:
            return "💖💖💖💖💖"
    else:
        if weight > -0.2:
            return "💔🖤🖤🖤🖤"
        elif weight > -0.4:
            return "💔💔🖤🖤🖤"
        elif weight > -0.6:
            return "💔💔💔🖤🖤"
        elif weight > -0.8:
            return "💔💔💔💔🖤"
        else:
            return "💔💔💔💔💔"

