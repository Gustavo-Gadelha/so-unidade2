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

    def clear(self):
        self.data = None

    def allocate(self):
        self.allocated = True

    def free(self):
        self.allocated = False
