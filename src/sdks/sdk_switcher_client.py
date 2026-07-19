""" Switcher Client SDK benchmark adapter. """
# https://pypi.org/project/switcher-client/

import os

from switcher_client import Client, ContextOptions, LoadSnapshotOptions

from sdks.sdk_bench import BenchError, SdkBench

class SdkSwitcherClient(SdkBench):
    """ Benchmark adapter for the Switcher Client SDK package. """

    sdk_id = "switcher-client"
    display_name = "Switcher Client SDK"

    def __init__(self):
        Client.build_context(
            domain='Switcher API',
            url='https://api.switcherapi.com',
            api_key=os.getenv("SWITCHER_KEY", "[API_KEY]"),
            component='switcher-client-python',
            options=ContextOptions(
                local=True,
                freeze=True
            )
        )

        Client.load_snapshot(options=LoadSnapshotOptions(fetch_remote=True))
        self.switcher = Client.get_switcher('CLIENT_PYTHON_FEATURE').throttle(1000)

    def run(self):
        """ Execute the SDK operation that is measured by the benchmark. """
        if not self.switcher.is_on():
            raise BenchError("Failed to get feature flag state.")
