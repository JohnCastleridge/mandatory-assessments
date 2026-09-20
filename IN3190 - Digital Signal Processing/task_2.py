from filters import h1, h2, h3
from task_1 import parse
import numpy as np
import matplotlib.pyplot as plt
import pytest


# task 2a
def plot_impulse_responses(h1: np.ndarray, h2: np.ndarray, h3: np.ndarray) -> None:
    """
    Plots the impulse responses of three FIR filters.

    Parameters:
    h1, h2, h3: numpy arrays
        Impulse responses of the three FIR filters.

    Returns:
    None
    """
    fig, ax = plt.subplots(3, 1, figsize=(10, 8))
    ax[0].stem(h1)
    ax[0].set_title("Impulse Response of Filter h1[n]", fontsize=16)

    ax[1].stem(h2)
    ax[1].set_title("Impulse Response of Filter h2[n]", fontsize=16)

    ax[2].stem(h3)
    ax[2].set_title("Impulse Response of Filter h3[n]", fontsize=16)

    plt.tight_layout()
    plt.show()


# task 2b
def convolve(x: np.ndarray, h: np.ndarray, ylen_choice: bool) -> np.ndarray:
    """
    Computes the convolution of two discrete-time signals x[n] and h[n].

    Parameters:
    x: numpy array
        Input signal x[n].
    h: numpy array
        Impulse response h[n].
    ylen_choice: bool
        If True, the length of the output signal y[n] is M + N - 1.
        If False, the length of the output signal y[n] is M.

    Returns:
    numpy array
        Convolution result y[n].
    """
    M, N = len(x), len(h)

    y = np.zeros(M + N - 1)
    for n in range(M + N - 1):
        for k in range(M):
            if 0 <= n - k < N:
                y[n] += x[k] * h[n - k]

    if ylen_choice:
        return y
    else:
        start_idx = (N - 1) // 2
        return y[start_idx : start_idx + M]


@pytest.mark.parametrize(
    "x, h, ylen_choice",
    [
        (np.array([1, 2, 3, 4, 5, 6]), np.array([-1, 0, 1]), True),
        (np.array([1, 2, 3, 4, 5, 6]), np.array([-1, 0, 1]), False),
    ],
)
def test_convolution(x: np.ndarray, h: np.ndarray, ylen_choice: bool):
    """
    Verifies my convolve function against NumPy's built-in np.convolve.
    """
    my_result = convolve(x, h, ylen_choice)
    np_mode = "full" if ylen_choice else "same"
    expected_result = np.convolve(x, h, mode=np_mode)

    np.testing.assert_allclose(
        my_result, expected_result, err_msg=f"Failed with ylen_choice={ylen_choice}"
    )


# task 2c
def DTFT(h: np.ndarray, N: int, fs: int) -> tuple[np.ndarray, np.ndarray]:
    """
    Computes the Discrete-Time Fourier Transform (DTFT) of a discrete-time signal h[n].

    Parameters:
    h: numpy array
        Input signal h[n].
    N: int
        Number of frequency points to compute the DTFT.
    fs: int
        Sampling frequency.

    Returns:
    H: numpy array
        DTFT of the input signal h[n].
    omega: numpy array
        Frequency points corresponding to the DTFT values, scaled to Hz.
    """

    omega = np.linspace(0, 2 * np.pi, N, endpoint=False)
    H = np.zeros(N, dtype=complex)
    for k in range(N):
        for n in range(len(h)):
            H[k] += h[n] * np.exp(-1j * omega[k] * n)

    return H, omega * (fs / (2 * np.pi))


# task 2d
def plot_DTFT(
    h1: np.ndarray, h2: np.ndarray, h3: np.ndarray, N: int = 1024, fs: int = 10
) -> None:
    """
    Plots the magnitude of the Discrete-Time Fourier Transform (DTFT) of three FIR filters.

    Parameters:
    h1, h2, h3: numpy arrays
        Impulse responses of the three FIR filters.
    N: int
        Number of frequency points to compute the DTFT. Default is 1024.
    fs: int
        Sampling frequency. Default is 10 Hz. (same as input data)

    returns:
    None
    """

    H1, frequency = DTFT(h1, N, fs=fs)
    H2, _ = DTFT(h2, N, fs=fs)
    H3, _ = DTFT(h3, N, fs=fs)

    fig, ax = plt.subplots(3, 1, figsize=(10, 8))
    ax[0].plot(frequency, np.abs(H1))
    ax[0].set_title("Frequency Response of Filter h1[n]", fontsize=16)
    ax[0].set_xlabel("Frequency (Hz)")
    ax[0].set_ylabel("Magnitude")

    ax[1].plot(frequency, np.abs(H2))
    ax[1].set_title("Frequency Response of Filter h2[n]", fontsize=16)
    ax[1].set_xlabel("Frequency (Hz)")
    ax[1].set_ylabel("Magnitude")

    ax[2].plot(frequency, np.abs(H3))
    ax[2].set_title("Frequency Response of Filter h3[n]", fontsize=16)
    ax[2].set_xlabel("Frequency (Hz)")
    ax[2].set_ylabel("Magnitude")

    plt.tight_layout()
    plt.show()


# task 2e
def filter_all():
    # READ DATA
    data_collection, times_collection, lats, lons, dt = parse()
    H1, H2, H3 = [], [], []
    for h, H in [(h1, H1), (h2, H2), (h3, H3)]:
        for data in data_collection:
            filtered_data = np.convolve(data, h, mode="same")
            H.append(filtered_data)
    H1, H2, H3 = np.array(H1), np.array(H2), np.array(H3)

    return H1, H2, H3, times_collection, lats, lons, dt


# task 2f
