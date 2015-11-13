def myrange(*args):
    """myrange function

    Return a generator object that generates numbers of the range on demand.
    The range is specified by the start - a first number of the range, stop - an
    upper bound of numbers of the range, step - an difference between current and
    next number

    Arguments:
        If one argument is passed - it will be the stop of the range.
        If two argument is passed - the first will be the start, second - the
        stop of the range.
        If three arguments is passed - the first will be the  start, second - the
        stop of the range, third - step
    """

    start = 0
    stop = None
    step = 1
    if len(args) == 1:
        stop = args[0]
    elif len(args) == 2:
        start, stop = args[0], args[1]
    else:
        start, stop, step = args[0], args[1], args[2]

    if step == 0:
        raise ValueError('Step must be non zero')

    current = start
    while (current - stop) * step < 0:
        yield current
        current += step


def main():
    import re

    params = [int(param) for param in re.split(r'\s+', raw_input("Params: "))]
    numbers = myrange(*params)
    print ' '.join(str(number) for number in numbers)


if __name__ == '__main__':  # pragma: no cover
    main()
