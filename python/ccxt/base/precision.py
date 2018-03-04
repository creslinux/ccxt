import decimal
import numbers

# rounding mode
TRUNCATE = 0
ROUND = 1

# digits counting mode
AFTER_POINT = 2
SIGNIFICANT_DIGITS = 3

# padding mode
NO_PADDING = 4
PAD_WITH_ZERO = 5


def decimalToPrecision(n, rounding_mode=ROUND, precision=None, counting_mode=AFTER_POINT, padding_mode=NO_PADDING):
    assert precision is not None and isinstance(precision, numbers.Integral) and precision < 28
    assert rounding_mode in [TRUNCATE, ROUND]
    assert counting_mode in [AFTER_POINT, SIGNIFICANT_DIGITS]
    assert padding_mode in [NO_PADDING, PAD_WITH_ZERO]

    # all default except decimal.Underflow (raised when a number is rounded to zero)
    decimal.getcontext().traps[decimal.Underflow] = True

    dec = decimal.Decimal(n)
    string = str(dec)

    def quant(x):
        return decimal.Decimal('10') ** (-x)

    if rounding_mode == ROUND:
        if counting_mode == AFTER_POINT:
            precise = str(dec.quantize(quant(precision)))  # ROUND_HALF_EVEN is default context
        elif counting_mode == SIGNIFICANT_DIGITS:
            # TODO
            raise NotImplementedError

    elif rounding_mode == TRUNCATE:
        # Slice a string
        if counting_mode == AFTER_POINT:
            before, after = string.split('.')
            truncated = before + '.' + after[:precision]
            precise = truncated.rstrip('.')
        elif counting_mode == SIGNIFICANT_DIGITS:
            start = string.index('.') - dec.adjusted()
            end = start + precision
            precise = string[:end]

    if padding_mode == NO_PADDING:
        return precise.rstrip('0').rstrip('.')
    elif padding_mode == PAD_WITH_ZERO:
        return precise.zfill(precision)