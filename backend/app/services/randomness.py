from abc import ABC, abstractmethod

from pydantic import BaseModel

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

    # TODO: implement other applicable tests

    def analyse_key_randomness(self, key: str):
        p_value, passed = FrequencyTest.monobit_test(key)
        results = {"test_name": "frequency_monobit", "p_value": p_value, "passed": passed}
        return [RandomnessResult(**results)]
