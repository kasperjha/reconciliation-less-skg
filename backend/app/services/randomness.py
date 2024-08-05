from abc import ABC, abstractmethod

from app.services.nist_test_suite.FrequencyTest import FrequencyTest


class RandomnessAnalyser(ABC):

    # TODO: establish a sensible return format

    @abstractmethod
    def analyse_key_randomness(key: str) -> bool:
        pass


class NistRandomnessAnalyser(RandomnessAnalyser):

    # TODO: implement other applicable tests

    def analyse_key_randomness(key: str) -> bool:
        _, passed = FrequencyTest.monobit_test(key)
        return passed
