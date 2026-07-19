""" Optimizely SDK benchmark adapter. """
# https://pypi.org/project/optimizely-sdk/

import os

from optimizely import optimizely

from sdks.sdk_bench import BenchError, SdkBench

class SdkOptimizely(SdkBench):
    """ Benchmark adapter for the Optimizely Feature Experimentation package. """

    sdk_id = "optimizely-sdk"
    display_name = "Optimizely Feature Experimentation"

    def __init__(self):
        self.optimizely_client = optimizely.Optimizely(
            sdk_key = os.environ.get("OPTIMIZELY_KEY"),
            skip_json_validation=True,
            logger=None,
            event_processor_options={
                "batch_size": 10,
                "flush_interval": 1000,
            }
        )

        self.user = self.optimizely_client.create_user_context("user123")

    def run(self):
        """ Execute the SDK operation that is measured by the benchmark. """
        if not self.user or not self.user.decide("my_feature").enabled:
            raise BenchError("Failed to get feature flag state.")
