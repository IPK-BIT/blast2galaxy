import sys

class Blast2galaxyError(Exception):
    """Base class for all exceptions raised by blast2galaxy, used for general errors"""
    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message

    def show(self) -> None:
        print(f'Error: {self.message}', file=sys.stderr)
        exit(1)

class Blast2galaxyConfigFileError(Blast2galaxyError):
    """Raised for an error with the configuration of blast2galaxy"""
    pass