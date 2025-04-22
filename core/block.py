from dataclasses import dataclass


@dataclass
class Block:
    index: int
    size: int
    data: bytes | None = None
    is_free: bool = True
    allocated: bool = False

    def read(self):
        return self.data

    def write(self, data: bytes):
        if len(data) > self.size:
            raise RuntimeError('Espaço requerido maior que o disponivel no setor')

        self.data = data
        self.is_free = False

    def clear(self):
        self.data = None
        self.is_free = True

    def allocate(self):
        self.allocated = True

    def free(self):
        self.allocated = False
