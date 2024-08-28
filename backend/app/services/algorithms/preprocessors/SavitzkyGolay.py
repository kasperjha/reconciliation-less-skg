from app.services.algorithms.preprocessors import Preprocessor
from scipy.signal import savgol_filter


class SavitzkyGolay(Preprocessor):
    def __init__(self, window_length=13, polyorder=3):
        self.window_length = window_length
        self.polyorder = polyorder

    def run(self, samples):
        return savgol_filter(samples, window_length=self.window_length, polyorder=self.polyorder)
