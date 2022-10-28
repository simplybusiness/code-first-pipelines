from typing import List, Tuple


class CycledPipelineError(Exception):
    def __init__(self, cycles: List[Tuple[str, str]]):
        self.cycles = cycles

        message = "\n".join([f'f "{f1}" depends on "{f2}".' for f1, f2 in cycles])

        super().__init__("Your pipeline contains cycles: " + message)
