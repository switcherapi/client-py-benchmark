""" Split.io Client SDK benchmark adapter. """
# https://pypi.org/project/splitio-client/

from sdks.sdk_bench import BenchError, SdkBench
from splitio import get_factory

class SdkSplitioClient(SdkBench):
    """ Benchmark adapter for the Split.io SDK for Python package. """

    sdk_id = "splitio-client"
    display_name = "Split.io SDK for Python"

    def __init__(self):
        factory = get_factory("localhost", config={
                'splitFile': './resources/flags.split',
                'localhostRefreshEnabled': False,
                'impressionsMode': 'optimized'
        })
        if factory is not None:
            factory.block_until_ready(5) # wait up to 5 seconds
            self.split = factory.client()
        else:
            raise BenchError("Failed to initialize Split.io factory.")

    def run(self):
        """ Execute the SDK operation that is measured by the benchmark. """
        treatment = self.split.get_treatment('CUSTOMER_ID', 'FEATURE_FLAG_NAME')
        if treatment == "off":
            raise BenchError("Failed to get feature flag state.")
