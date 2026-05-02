""" Unleash Client SDK benchmark adapter. """
# https://pypi.org/project/UnleashClient/

from sdks.sdk_bench import BenchError, SdkBench
from UnleashClient import UnleashClient
from UnleashClient.cache import FileCache

class SdkUnleashClient(SdkBench):
    """ Benchmark adapter for the Unleash SDK for Python package. """

    sdk_id = "unleash-client"
    display_name = "Unleash SDK for Python"

    def __init__(self):
        cache = FileCache("MY_CACHE")
        cache.bootstrap_from_dict({
            "version": 2,
            "features": [
                {
                    "name": "my_toggle",
                    "enabled": True,
                    "strategies": [{"name": "default"}],
                }
            ]
        })

        self.client = UnleashClient(
            url="https://app.unleash-hosted2.com/demo/api/",
            app_name="my-application",
            cache=cache
        )

    def run(self):
        """ Execute the SDK operation that is measured by the benchmark. """
        if not self.client.is_enabled("my_toggle"):
            raise BenchError("Failed to get feature flag state.")
