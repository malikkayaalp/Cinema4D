from decimal import Decimal

def get_multiplier(_from, _to, step):
    digits = []
    for number in [_from, _to, step]:
        pre = Decimal(str(number)) % 1
        digit = len(str(pre)) - 2
        digits.append(digit)
    max_digits = max(digits)
    return float(10 ** (max_digits))


def float_range(_from, _to, step, include=False):
    """Generates a range list of floating point values over the Range [start, stop]
       with step size step
       include=True - allows to include right value to if possible
       !! Works fine with floating point representation !!
    """
    mult = get_multiplier(_from, _to, step)
    # print mult
    int_from = int(round(_from * mult))
    int_to = int(round(_to * mult))
    int_step = int(round(step * mult))
    # print int_from,int_to,int_step
    if include:
        result = range(int_from, int_to + int_step, int_step)
        result = [r for r in result if r <= int_to]
    else:
        result = range(int_from, int_to, int_step)
    # print result
    float_result = [r / mult for r in result]
    return float_result


print float_range(-1, 0, 0.01,include=False)