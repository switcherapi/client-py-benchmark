""" Amplitude Experiment SDK benchmark adapter. """
# https://pypi.org/project/amplitude-experiment/

import os

from amplitude_experiment import Experiment, User

from sdks.sdk_bench import BenchError, SdkBench

class SdkAmplitudeExperiment(SdkBench):
    """ Benchmark adapter for the Experiment Python SDK package. """

    sdk_id = "amplitude-experiment"
    display_name = "Experiment Python SDK"

    def __init__(self):
        self.experiment = Experiment.initialize_local(os.getenv("AMPLITUDE_EXPERIMENT_KEY", "[API_KEY]"))
        self.experiment.start()

        self.user = User(
            device_id="user1"
        )

    def run(self):
        """ Execute the SDK operation that is measured by the benchmark. """
        variants = self.experiment.evaluate_v2(self.user, flag_keys={"feature_flag_local"})
        if variants["feature_flag_local"].value != "on":
            raise BenchError("Failed to get feature flag state.")
