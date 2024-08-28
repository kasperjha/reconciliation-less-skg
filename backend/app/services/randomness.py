from abc import ABC, abstractmethod

from pydantic import BaseModel

from app.services.nist_test_suite.CumulativeSums import CumulativeSums
from app.services.nist_test_suite.RunTest import RunTest
from app.services.nist_test_suite.FrequencyTest import FrequencyTest


class RandomnessResult(BaseModel):
    test_name: str
    p_value: float
    passed: bool


class RandomnessAnalyser(ABC):

    @abstractmethod
    def analyse_key_randomness(self, key: str) -> list[RandomnessResult]:
        pass


class NistRandomnessAnalyser(RandomnessAnalyser):

    def __init__(self):
        self.tests = {}
        self.tests["frequency_monobit"] = FrequencyTest.monobit_test
        self.tests["block_frequency"] = FrequencyTest.block_frequency
        self.tests["approximate_entropy"] = FrequencyTest.block_frequency
        self.tests["runs"] = RunTest.run_test
        self.tests["longest_run_of_ones"] = RunTest.longest_one_block_test
        self.tests["cumulative_sums"] = CumulativeSums.cumulative_sums_test

    def analyse_key_randomness(self, key: str):
        results = []
        for name, test in self.tests.items():
            p_value, passed = test(key)
            results.append(RandomnessResult(**{"test_name": name, "p_value": p_value, "passed": passed}))
        return results
