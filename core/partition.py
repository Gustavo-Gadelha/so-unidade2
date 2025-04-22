class Partition:
    def __init__(self, disk, start, end):
        self.disk = disk
        self.start = start
        self.end = end

        self.total_blocks = (end - start) + 1
        self.size = self.total_blocks * self.disk.block_size

    def __repr__(self):
        return (f'Partition('
                f'size={self.size}B, '
                f'start={self.start}, '
                f'end={self.end}, '
                f'total_blocks={self.total_blocks})')
