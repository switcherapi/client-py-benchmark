""" Static Boolean benchmark adapter. """

import os

from sdks.sdk_bench import BenchError, SdkBench

class SdkStaticBool(SdkBench):
    """ Benchmark adapter for a static boolean value. """

    sdk_id = "static-bool"
    display_name = "static-bool"

    def __init__(self):
        os.environ["MY_ENV_VAR"] = "true"

    def run(self):
        """ Execute the SDK operation that is measured by the benchmark. """
        result = os.getenv("MY_ENV_VAR", "false").lower() == "true"
        if not result:
            raise BenchError("Failed to get feature flag state.")
