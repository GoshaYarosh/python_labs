from tempfile import TemporaryFile


# seek file to start
def _reset(source_file):
    source_file.seek(0)
    return source_file


# returns number of lines in file
def _file_length(source_file):
    length = reduce(lambda length, line: length + 1, source_file, 0)
    source_file.seek(0)
    return length


def external_sort(file_name, reverse=False, chunk_size=None):
    '''External sort function

    Sorts some file with numbers by merge sort alrorithm. File format: every
    numbers must be stored in new line.

    Params:
        file_name - the name of file that you want sorted
        reverse - if false sort by ascending, else sort by descending
        chunk_size - size of maximal chunk that can be sorted in memory

    Exceptions:
        ValueError - if chunk size is zero
    '''

    # split file in two equal parts
    def split_file(source_file, low_part, high_part):
        length = _file_length(source_file)
        source_file = _reset(source_file)
        low_part.writelines(
            source_file.readline()
            for i in xrange(length // 2)
        )
        high_part.writelines(source_file.readlines())

    # sort chunk by ordinary sort
    def sort_chunk(source_file):
        numbers = [float(line) for line in source_file]
        numbers.sort()
        source_file.seek(0)
        source_file.writelines('{0:g}\n'.format(number) for number in numbers)

    # merge two files into one
    def merge_parts(dest_file, low_part, high_part):
        dest_file.truncate(0)
        low_part_number = low_part.readline()
        high_part_number = high_part.readline()
        while low_part_number and high_part_number:
            if float(low_part_number) < float(high_part_number) and not reverse:
                dest_file.write(low_part_number)
                low_part_number = low_part.readline()
            else:
                dest_file.write(high_part_number)
                high_part_number = high_part.readline()
        dest_file.writelines(list(low_part_number))
        dest_file.writelines(list(high_part_number))
        dest_file.writelines(low_part)
        dest_file.writelines(high_part)

    def sort(source_file):
        length = _file_length(source_file)
        if length <= chunk_size:
            sort_chunk(source_file)
        else:
            with TemporaryFile() as low_part, TemporaryFile() as high_part:
                split_file(source_file, low_part, high_part)
                sort(_reset(low_part))
                sort(_reset(high_part))
                merge_parts(
                    _reset(source_file),
                    _reset(low_part),
                    _reset(high_part)
                )

    chunk_size = 100 if chunk_size is None else chunk_size
    with open(file_name, 'r+') as source_file:
        if chunk_size > 0:
            sort(source_file)
        else:
            raise ValueError('Chunk size must be greater than zero')


def main():
    import argparse
    import random

    parser = argparse.ArgumentParser()
    parser.add_argument('file_name', type=str, help='the name of file')
    parser.add_argument('-c', '--create_file', action='store_true')
    parser.add_argument('-r', '--reverse', action='store_true')
    parser.add_argument('-cs', '--chunk_size', type=int)
    args = parser.parse_args()

    if args.create_file:
        with open(args.file_name, 'w+') as f:
            numbers = (str(random.randint(-1000, 1000)) for i in range(1000))
            f.writelines('\n'.join(numbers))
    else:
        external_sort(args.file_name, args.reverse, args.chunk_size)


if __name__ == "__main__":  # pragma: no cover
    main()
