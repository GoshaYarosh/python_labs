from tempfile import TemporaryFile
from random import randint


def external_sort(source_file_name, reverse=False, chunk_size=100):

    def reset(source_file):
        source_file.seek(0)
        return source_file

    def file_length(source_file):
        length = reduce(lambda length, line: length + 1, source_file, 0)
        source_file.seek(0)
        return length

    def split_file(source_file, low_part, high_part):
        length = file_length(source_file)
        source_file = reset(source_file)
        low_part.writelines(
            source_file.readline()
            for i in xrange(length // 2)
        )
        high_part.writelines(source_file.readlines())

    def sort_chunk(source_file):
        numbers = [float(line) for line in source_file]
        numbers.sort()
        source_file.seek(0)
        source_file.writelines('{0:g}\n'.format(number) for number in numbers)

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
        length = file_length(source_file)
        if length <= chunk_size:
            sort_chunk(source_file)
        else:
            with TemporaryFile() as low_part, TemporaryFile() as high_part:
                split_file(source_file, low_part, high_part)
                sort(reset(low_part))
                sort(reset(high_part))
                merge_parts(
                    reset(source_file),
                    reset(low_part),
                    reset(high_part)
                )

    with open(source_file_name, 'r+w') as source_file:
        if chunk_size > 0:
            sort(source_file)
        else:
            raise ValueError('Chunk size must be greater than zero')
