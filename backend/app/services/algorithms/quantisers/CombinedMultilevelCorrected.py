import numpy as np
from app.services.algorithms.preprocessors import Preprocessor


class CombinedMultilevelCorrected(Preprocessor):

    def run(self, signal: list[int]) -> str:
        variance = np.var(signal)
        mean = np.mean(signal)
        result = ""

        for sample in signal:
            if sample < (mean - variance):
                result += "00"
            elif (mean - variance) < sample and sample < mean:
                result += "01"
            elif mean < sample and sample < (mean + variance):
                result += "11"
            elif (mean + variance) < sample:
                result += "10"
            else:
                pass

        return result
