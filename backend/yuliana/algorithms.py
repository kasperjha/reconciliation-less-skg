import numpy as np

from app.services.algorithms.preprocessors import SavitzkyGolay
from app.services.algorithms.preprocessors.Kalman import Kalman
from app.services.algorithms.quantisers.CombinedMultilevelCorrected import CombinedMultilevelCorrected
from app.services.algorithms.quantisers.CombinedMultilevel import CombinedMultilevel
from yuliana.util import get_blocks


def savitzky_golay(samples):
    sg = SavitzkyGolay.SavitzkyGolay()
    return sg.run(samples)


def _kalman_whole(samples, block_size):
    def gpt_exact_modified_kalman(y_u, NB, SB, v_u):
        # Constants as given in the algorithm
        A = 2.13
        H = 2.13
        Q = 0.0001
        R = 4.6

        # Initial guesses
        x_0 = 0
        P_0 = 1

        # Initialize lists to store results
        z_u = []

        # Begin the Modified Kalman Filter process
        for i in range(NB):  # Loop from i = 1 to NB
            # Step 1: Initialization for the first block
            x_hat_k0_i = A * x_0
            P_k0_i = A * A * P_0 + Q
            K_k0_i = P_k0_i / (P_k0_i + R)
            P_k0_i = P_k0_i * (1 - K_k0_i)
            x_k_hat_k0_i = x_hat_k0_i + K_k0_i * (y_u[i][0] - H * x_hat_k0_i)

            # Step 2: Enhanced Modified Kalman output for the first block
            z_k0_i = x_k_hat_k0_i
            z_u_i = z_k0_i + 0.2 * v_u[i]
            z_u.append(z_u_i)

            # Step 3: Loop for each measurement within the block
            for j in range(1, SB):  # Loop from j = 2 to SB
                x_hat_kj_i = A * x_k_hat_k0_i
                P_kj_i = A * A * P_k0_i + Q
                K_kj_i = P_kj_i / (P_kj_i + R)
                P_kj_i = P_kj_i * (1 - K_kj_i)
                x_k_hat_kj_i = x_hat_kj_i + K_kj_i * (y_u[i][j] - H * x_hat_kj_i)

                # Enhanced Modified Kalman output for the current block
                z_kj_i = x_k_hat_kj_i
                z_u_j = z_kj_i + 0.2 * v_u[i]
                z_u.append(z_u_j)

        return z_u

    y_u = get_blocks(samples, block_size)
    v_u = [np.var(block) for block in y_u]
    NB = len(y_u)
    SB = block_size
    return gpt_exact_modified_kalman(y_u, NB, SB, v_u)


def kalman_diy(samples):
    kalman = Kalman()
    return kalman.run(samples)


def kalman_yuliana(y_u):
    # Constants as given in the algorithm
    A = 2.13
    H = 2.13
    Q = 0.0001
    R = 4.6

    # Initial guesses
    x_0 = 0
    P_0 = 1

    # Initialize lists to store results
    z_u = []

    SB = len(y_u)
    v_u = np.var(y_u)

    # Step 1: Initialization for the first block
    x_hat_k0_i = A * x_0
    P_k0_i = A * A * P_0 + Q
    K_k0_i = P_k0_i / (P_k0_i + R)
    P_k0_i = P_k0_i * (1 - K_k0_i)
    x_k_hat_k0_i = x_hat_k0_i + K_k0_i * (y_u[0] - H * x_hat_k0_i)

    # Step 2: Enhanced Modified Kalman output for the first block
    z_k0_i = x_k_hat_k0_i
    z_u_i = z_k0_i + 0.2 * v_u
    z_u.append(z_u_i)

    # Step 3: Loop for each measurement within the block
    for j in range(1, SB):  # Loop from j = 2 to SB
        x_hat_kj_i = A * x_k_hat_k0_i
        P_kj_i = A * A * P_k0_i + Q
        K_kj_i = P_kj_i / (P_kj_i + R)
        P_kj_i = P_kj_i * (1 - K_kj_i)
        x_k_hat_kj_i = x_hat_kj_i + K_kj_i * (y_u[j] - H * x_hat_kj_i)

        # Enhanced Modified Kalman output for the current block
        z_kj_i = x_k_hat_kj_i
        z_u_j = z_kj_i + 0.2 * v_u
        z_u.append(z_u_j)

    return z_u


def polynomial_regression_diy(samples):
    x_values = np.arange(len(samples))
    coeffs = np.polyfit(x_values, samples, 2)  # degree 2
    fitted_y_values = np.polyval(coeffs, x_values)
    return fitted_y_values


def polynomial_regression_yuliana(samples, m=2):

    # Initialize the result list for enhanced polynomial regression
    y_u = []

    # Initialize matrices and vectors
    c = np.zeros((m + 1, m + 1))
    b = np.zeros(m + 1)
    a = np.zeros(m + 1)

    # Step 2: Loop over polynomial order
    for j in range(1, m + 2):
        # Step 3: Compute matrix C elements
        for k in range(1, j + 1):
            d = j + k - 2
            sum_c = 0

            # Step 4: Loop to compute sum for matrix C
            for index in range(1, len(samples) + 1):
                sum_c += index**d

            # Fill in symmetric elements
            c[j - 1, k - 1] = sum_c
            c[k - 1, j - 1] = sum_c

        # Step 5: Compute vector B elements
        sum_b = 0
        for index, sample in enumerate(samples):
            sum_b += index ** (j - 1) * sample

        b[j - 1] = sum_b

    # Step 6: Solve for a using c and b
    a = np.linalg.solve(c, b)

    # Step 7: Compute enhanced polynomial regression for each block
    for index in range(1, len(samples) + 1):
        # Compute the polynomial regression value
        y_u_l = sum(a[p] * index**p for p in range(m + 1))
        y_u.append(y_u_l)

    return y_u


def combined_multilevel_quantisation(samples):
    return CombinedMultilevel().run(samples)


def combined_multilevel_quantisation_corrected(samples):
    return CombinedMultilevelCorrected().run(samples)
