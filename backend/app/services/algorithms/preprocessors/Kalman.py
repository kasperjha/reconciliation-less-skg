from app.services.algorithms.preprocessors import Preprocessor
import numpy as np


class Kalman(Preprocessor):
    def _kalman_block(self, x, P, s, A, H, Q, R):
        """
        Prediction and update in Kalman filter
        input:
            - signal: signal to be filtered
            - x: previous mean state
            - P: previous variance state
            - s: current observation
            - A, H, Q, R: kalman filter parameters
        output:
            - x: mean state prediction
            - P: variance state prediction
        """
        # check laaraiedh2209 for further understand these equations
        x_mean = A * x + np.random.normal(0, Q, 1)[0]  # made modification here to get single value
        P_mean = A * P * A + Q

        K = P_mean * H * (1 / (H * P_mean * H + R))
        x = x_mean + K * (s - H * x_mean)
        P = (1 - K * H) * P_mean

        return x, P

    def run(self, samples: list[int], A=1, H=1, Q=1.6, R=6):
        """
        Implementation of Kalman filter.
        Takes a signal and filter parameters and returns the filtered signal.
        input:
            - signal: signal to be filtered
            - A, H, Q, R: kalman filter parameters
        output:
            - filtered signal
        """
        signal = samples

        predicted_signal = []

        x = signal[0]  # takes first value as first filter prediction
        P = 0  # set first covariance state value to zero

        predicted_signal.append(x)
        for j, s in enumerate(signal[1:]):  # iterates on the entire signal, except the first element

            x, P = self._kalman_block(x, P, s, A, H, Q, R)  # calculates next state prediction

            predicted_signal.append(x)  # update predicted signal with this step calculation

        return predicted_signal
