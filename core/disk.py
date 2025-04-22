import itertools
import math

from core.block import Block
from core.partition import Partition


class Disk:
    def __init__(self, size: int = 65536, block_size: int = 4096):
        self.size = size
        self.block_size = block_size
        self.total_blocks = size // block_size

        self.blocks: list[Block] = [Block(index, self.block_size) for index in range(self.total_blocks)]
        self.partitions: dict[int, Partition] = {}
        self._partition_id_counter = 0

    def create_partition(self, size: int):
        if size > self.size:
            raise ValueError('Espaço para partição maior que o tamanho do disco')

        needed_blocks = math.ceil(size / self.block_size)
        blocks = self._find_contiguous_blocks(needed_blocks)

        start = blocks[0]
        end = blocks[-1]
        partition = Partition(self, start.index, end.index)
        self.partitions[self._partition_id_counter] = partition
        self._partition_id_counter += 1

        for block in itertools.islice(self.blocks, start.index, end.index + 1):
            block.allocate()

        return partition

    def delete_partition(self, index: int):
        partition = self.partitions.pop(index)
        for block in itertools.islice(self.blocks, partition.start, partition.end + 1):
            block.free()

    def print_debug(self):
        for index, partition in self.partitions.items():
            print(f'{index}: {partition}')

        for block in self.blocks:
            print(block)

    def _find_contiguous_blocks(self, needed: int) -> list[Block]:
        if needed > self.total_blocks:
            raise ValueError(f"Requested {needed} blocks exceeds total available ({self.total_blocks})")

        for i in range(self.total_blocks - needed + 1):
            if self.blocks[i].allocated:
                continue

            sequence = self.blocks[i:i + needed]
            if all(not block.allocated for block in sequence):
                return list(sequence)

        raise ValueError(f'Uma sequencia de {needed} blocos contiguos não foi encontrada')

    def __repr__(self):
        return (f'<Disk total_size={self.size}B '
                f'block_size={self.block_size}B '
                f'total_blocks={self.total_blocks} '
                f'partitions={len(self.partitions)}>')
