def myrange(start, stop=None, step=1):
    if stop is None:
        stop = start
        start = 0

    if step == 0:
        raise ValueError('Step must be non-zero');

    current = start
    while (current - stop) * step < 0:
        yield current
        current += step
