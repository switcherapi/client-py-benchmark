""" Registry of benchmarkable SDK adapters. """

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from sdks.sdk_bench import BenchError, SdkBench
from sdks.sdk_amplitude_experiment import SdkAmplitudeExperiment
from sdks.sdk_harness import SdkHarness
from sdks.sdk_optimizely import SdkOptimizely
from sdks.sdk_splitio_client import SdkSplitioClient
from sdks.sdk_static_bool import SdkStaticBool
from sdks.sdk_switcher_client import SdkSwitcherClient
from sdks.sdk_unleash_client import SdkUnleashClient

@dataclass(frozen=True)
class AdapterRegistration:
    """ Metadata required to build and report an SDK benchmark adapter. """

    sdk_id: str
    display_name: str
    factory: Callable[[], SdkBench]

_REGISTRY = {
    SdkStaticBool.sdk_id: AdapterRegistration(
        sdk_id=SdkStaticBool.sdk_id,
        display_name=SdkStaticBool.display_name,
        factory=SdkStaticBool,
    ),
    SdkSwitcherClient.sdk_id: AdapterRegistration(
        sdk_id=SdkSwitcherClient.sdk_id,
        display_name=SdkSwitcherClient.display_name,
        factory=SdkSwitcherClient,
    ),
    SdkHarness.sdk_id: AdapterRegistration(
        sdk_id=SdkHarness.sdk_id,
        display_name=SdkHarness.display_name,
        factory=SdkHarness,
    ),
    SdkUnleashClient.sdk_id: AdapterRegistration(
        sdk_id=SdkUnleashClient.sdk_id,
        display_name=SdkUnleashClient.display_name,
        factory=SdkUnleashClient,
    ),
    SdkOptimizely.sdk_id: AdapterRegistration(
        sdk_id=SdkOptimizely.sdk_id,
        display_name=SdkOptimizely.display_name,
        factory=SdkOptimizely,
    ),
    SdkAmplitudeExperiment.sdk_id: AdapterRegistration(
        sdk_id=SdkAmplitudeExperiment.sdk_id,
        display_name=SdkAmplitudeExperiment.display_name,
        factory=SdkAmplitudeExperiment,
    ),
    SdkSplitioClient.sdk_id: AdapterRegistration(
        sdk_id=SdkSplitioClient.sdk_id,
        display_name=SdkSplitioClient.display_name,
        factory=SdkSplitioClient,
    )
}

def list_adapter_registrations():
    """ Return all registered SDK benchmark adapters. """
    return tuple(_REGISTRY.values())

def get_adapter_registration(sdk_id):
    """ Resolve a registered SDK adapter by its CLI identifier. """
    try:
        return _REGISTRY[sdk_id]
    except KeyError as error:
        raise BenchError(
            f"Unknown SDK adapter '{sdk_id}'. Use --list-sdks to see the available adapters."
        ) from error
