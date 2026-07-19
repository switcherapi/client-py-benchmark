""" Harness Feature Flags SDK benchmark adapter. """
# https://pypi.org/project/harness-featureflags/

import os

from featureflags.client import CfClient, Config, Target

from sdks.sdk_bench import BenchError, SdkBench

class SdkHarness(SdkBench):
    """ Benchmark adapter for the Python SDK For Harness Feature Flags package. """

    sdk_id = "harness-featureflags"
    display_name = "Python SDK For Harness Feature Flags"

    def __init__(self):
        self.client = CfClient(sdk_key=os.getenv("HARNESS_KEY", "[API_KEY]"), config=Config(
            enable_analytics=False,
            enable_stream=True,
            pull_interval=2 * 60 * 1000,  # two min pollInterval
        ))

        self.target = Target(
            identifier='pythonsdk',
            name="PythonSDK",
            attributes={"location": "emea"}
        )

        self.client.wait_for_initialization()

    def run(self):
        """ Execute the SDK operation that is measured by the benchmark. """
        if not self.client.bool_variation("feature_flag", self.target, False):
            raise BenchError("Failed to get feature flag state.")
