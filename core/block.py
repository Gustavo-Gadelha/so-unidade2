from dataclasses import dataclass


@dataclass
class Block:
    index: int
    size: int
    data: bytes | None = None
    allocated: bool = False

    def read(self):
        return self.data

    def write(self, data: bytes):
        if len(data) > self.size:
            raise RuntimeError('Espaço requerido maior que o disponivel no setor')

        self.data = data
        self.allocated = False

    def clear(self):
        self.data = None
        self.allocated = True

    def allocate(self):
        self.allocated = True

    def free(self):
        self.allocated = False

    def __repr__(self):
        return f"Block(index={self.index}, size={self.size}, data={self.data}, allocated={self.allocated})"
