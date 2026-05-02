""" Benchmark adapter contract and shared benchmark errors. """

class SdkBench:
    """Common lifecycle for an SDK benchmark adapter."""

    sdk_id = ""
    display_name = ""

    def run(self):
        """ Execute the single SDK call that should be timed. """
        raise NotImplementedError("Run method not implemented.")

class BenchError(Exception):
    """ Custom exception for benchmark errors. """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
