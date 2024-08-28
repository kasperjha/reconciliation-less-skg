from app.services.algorithms.quantisers import Quantiser


class MeanStdQuantiser(Quantiser):
    def std_dev(self, samples):
        n = len(samples)
        mean = sum(samples) / n
        sumsq = sum(v * v for v in samples)
        return (sumsq / n - mean * mean) ** 0.5

    def run(self, samples: list[int]) -> str:
        mean = sum(samples) / len(samples)
        std = self.std_dev(samples)
        alpha = 0
        threshold_pos = mean + alpha * std
        threshold_neg = mean - alpha * std

        bits = ""

        for sample in samples:
            if threshold_pos < sample:
                bits += "1"
            if sample < threshold_neg:
                bits += "0"
            else:
                continue

        return bits
