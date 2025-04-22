import itertools
import math

from core.units import Block


class Disk:
    def __init__(self, root: str = '/', total_size: int = 65536, block_size: int = 1024):
        self.root = root
        self.total_size = total_size
        self.block_size = block_size
        self.total_blocks = total_size // block_size

        self.blocks: list[Block] = [Block(index, self.block_size) for index in range(self.total_blocks)]
        self.partitions: dict[str, Partition] = {}

    def create_partition(self, name: str, size: int):
        if size > self.total_size:
            raise ValueError('Espaço para partição maior que o espaço em disco')

        needed_blocks = math.ceil(size / self.block_size)
        blocks = self._find_contiguous_blocks(needed_blocks)

        start = blocks[0]
        end = blocks[-1]
        partition = Partition(self, start.index, end.index)
        self.partitions[name] = partition

        for block in itertools.islice(self.blocks, start.index, end.index + 1):
            block.allocate()

        return partition

    def delete_partition(self, root: str):
        if root not in self.partitions:
            raise ValueError('Partição não existe')

        partition = self.partitions.pop(root)
        for block in itertools.islice(self.blocks, partition.start, partition.end + 1):
            block.free()

    # TODO: iterar apenas sobre blocos livres, causa fragmentação excessiva caso contrario
    def _find_contiguous_blocks(self, needed: int) -> list[Block] | None:
        for batch in itertools.batched(self.blocks, n=needed):
            if all(not block.allocated for block in batch):
                return list(batch)

        else:
            raise ValueError(f'Uma sequencia de {needed} blocos contiguos não foi encontrada')

    def __repr__(self):
        return (f'<Disk root=\'{self.root}\' '
                f'total_size={self.total_size}B '
                f'block_size={self.block_size}B '
                f'total_blocks={self.total_blocks} '
                f'partitions={len(self.partitions)}>')


class Partition:
    def __init__(self, disk: Disk, start: int, end: int):
        self.start = start
        self.end = end
        self.total_blocks = (end - start) + 1
        self.size = self.total_blocks * disk.block_size

    def __repr__(self):
        return (f'<Partition start={self.start} '
                f'end={self.end} '
                f'total_blocks={self.total_blocks} '
                f'size={self.size}B>')
