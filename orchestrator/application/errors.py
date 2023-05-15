class InvalidMachineId(RuntimeError):
    @classmethod
    def from_identifier(cls, identifier: str):
        return cls('No machine with id %s exists' % identifier)
