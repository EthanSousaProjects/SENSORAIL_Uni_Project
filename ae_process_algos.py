"""

This file contains all the Algorithms found on the OpenAE website linked:
https://openae.io/features/latest/
This was taken on 25/11/2024.

Thank you to OpenAE.io for all these signal processing algorithms 
that we will use to compare our different signals.

"""

######################################
# Packages to import for all Functions
######################################
import numpy as np


######################################
# Functions of algorithums
######################################

def singal_to_Spectrum(
    signal: np.ndarray
    ):
    """
    Convert a singal (amplitude time domain) to a spectrum (frequency amplitude domain).

    Args:
        signal: The time domin representation of a signal

    Returns:
        spectrum: The amplitude against frequency representation of a signal
    """

    return np.fft.fft(signal)

def band_energy(
    spectrum: np.ndarray, samplerate: float, f_lower: float, f_upper: float
    ) -> float:
    """
    The energy in an arbitrary frequency band.

    Args:
        spectrum: The amplitude against frequency representation of a signal
        samplerate: The rate at which samples were taken
        f_lower: Lower frequency band
        f_upper: Upper frequency band

    Returns:
        float: Power spectrum sum
    """
    powerspectrum = np.abs(spectrum) ** 2
    n = len(powerspectrum)
    n_lower = int(2 * n * f_lower / samplerate)
    n_upper = int(2 * n * f_upper / samplerate)
    return np.sum(powerspectrum[n_lower:n_upper])

def band_energy_ratio(
    spectrum: np.ndarray, samplerate: float, f_lower: float, f_upper: float
    ) -> float:
    """
    The ratio of the band energy in an arbitrary frequency band and the total energy.
    Also known as partial power.

    Args:
        spectrum: The amplitude against frequency representation of a signal
        samplerate: The rate at which samples were taken
        f_lower: Lower frequency band
        f_upper: Upper frequency band

    Returns:
        float: Band enery ratio
    """
    powerspectrum = np.abs(spectrum) ** 2
    n = len(powerspectrum)
    n_lower = int(2 * n * f_lower / samplerate)
    n_upper = int(2 * n * f_upper / samplerate)
    return np.sum(powerspectrum[n_lower:n_upper]) / np.sum(powerspectrum)

def clearance_factor(
    signal: np.ndarray
    ) -> float:
    """
    Ratio of the peak amplitude and the squared mean of the square roots of the absolute amplitudes.
    Used for determining bearing health.

    Args:
        signal: The time domin representation of a signal
    
    Returns:
        float: Clearance factor
    """
    return np.max(np.abs(signal)) / (np.mean(np.sqrt(np.abs(signal))) ** 2)

def counts(
    signal: np.ndarray, threshold: float
    ) -> int:
    """
    The number of positive threshold crossings of a burst signal.
    Also known as ring down counts.

    Args:
        signal: The time domin representation of a signal
        threshold: Threshold amplitude signal must be greater than to be counted

    Returns:
        float: counts of how many times signal passes threshold
    """
    if len(signal) == 0:
        return 0
    result = 0
    was_above_threshold = signal[0] >= threshold
    for value in signal[1:]:
        is_above_threshold = value >= threshold
        if not was_above_threshold and is_above_threshold:
            result += 1
        was_above_threshold = is_above_threshold
    return result

def crest_factor(
    signal: np.ndarray
    ) -> float:
    """
    The ratio of the peak amplitude to the RMS of the signal.
    Used in fault detection of bearings and gear boxes.

    Args:
        signal: The time domin representation of a signal

    Returns:
        float: Creast factor
    """
    return np.max(np.abs(signal)) / np.sqrt(np.mean(signal**2))

def energy(
    signal: np.ndarray
    ) -> float:
    """
    Energy of signal which is the integral of the squared signal.

    Args:
        signal: The time domin representation of a signal

    Returns:
        float: Signal energy
    """
    return np.sum(signal**2)

def impulse_factor(
    signal: np.ndarray
    ) -> float:
    """
    The ratio of the peak amplitude and mean of the absolute values.

    Args:
        signal: The time domin representation of a signal

    Returns:
        float: Impulse factor
    """
    return np.max(np.abs(signal)) / np.mean(np.abs(signal))

def k_factor(
    signal: np.ndarray
    ) -> float:
    """
    The product of the peak amplitude and the RMS.

    Args:
        signal: The time domin representation of a signal

    Returns:
        float: K-factor
    """
    return np.max(np.abs(signal)) * np.sqrt(np.mean(signal**2))

def central_moment(
    signal: np.ndarray,
    order: int
    ) -> float:
    """
    Function used in other AE processing functions.

    Args:
        order: integer of the central moment order
    Returns:
        float: Central moment
    """
    return np.mean((signal - signal.mean()) ** order)

def kurtosis(
    signal: np.ndarray
    ) -> float:
    """
    Describes the tailedness or the presence of outliers in the data.

    Args:
        signal: The time domin representation of a signal

    Returns:
        float: Kurtosis
    """

    return central_moment(signal,4) / central_moment(signal,2) ** 2

def margin_factor(
    signal: np.ndarray
    ) -> float:
    """
    Ratio of the peak amplitude and square mean of the square root of the absolute values.
    Used in fault detection of bearings.

    Args:
        signal: The time domin representation of a signal

    Returns:
        float: Margin factor
    """
    return np.max(np.abs(signal)) / (np.mean(np.sqrt(np.abs(signal))) ** 2)

def peak_amplitude(
    signal: np.ndarray
    ) -> float:
    """
    The maximum absolute amplitude of a signal.

    Args:
        signal: The time domin representation of a signal

    Returns:
        float: Peak amplitude
    """
    return np.max(np.abs(signal))

def rms(
    signal: np.ndarray
    ) -> float:
    """
    Quadratic mean of the signal which is a measure of the average energy of a signal.
    Used in wear and leak detection.

    Args:
        signal: The time domin representation of a signal

    Returns:
        float: RMS of the signal
    """
    return np.sqrt(np.mean(signal**2))

def shape_factor(
    signal: np.ndarray
    ) -> float:
    """
    The ratio between the RMS and the mean of absolute values.

        Args:
        signal: The time domin representation of a signal

    Returns:
        float: Shape factor
    """
    return np.sqrt(np.mean(signal**2)) / np.mean(np.abs(signal))

def skewness(
    signal: np.ndarray
    ) -> float:
    """
    Statistical measure of that quantifies theasymmetry of the probability distribution of a dataset.
    Provides information about the direction and degree of skew.

    Args:
        signal: The time domin representation of a signal

    Returns:
        float: Skewness
    """
    return central_moment(signal,3) / central_moment(signal,2) ** (3 / 2)

def spectral_centroid(
    spectrum: np.ndarray, samplerate: float
    ) -> float:
    """
    Indicates where the centre of mass of the spectrum is.
    Commonly associated with the brightness of the sound.

    Args:
        spectrum: The amplitude against frequency representation of a signal
        samplerate: The rate at which samples were taken

    Returns:
        float: Spectral centroid
    """
    ps = np.abs(spectrum) ** 2
    ps_sum = 0.0
    ps_sum_weighted = 0.0
    for i, magnitude in enumerate(ps):
        ps_sum += magnitude
        ps_sum_weighted += magnitude * i
    return 0.5 * samplerate / (len(ps) - 1) * (ps_sum_weighted / ps_sum)

def spectral_kurtosis(
    spectrum: np.ndarray, samplerate: float
    ) -> float:
    """
    Spectral kurtosis is a measure of the "tailedness" or peakedness of the power spectrum around its mean.\n
    High kurtosis: Indicates a distribution with heavy tails and a sharp peak.\n
    Low kurtosis: Indicates a flatter distribution.\n
    Normal kurtosis (value of 3): Indicates a normal distribution.

    Args:
        spectrum: The amplitude against frequency representation of a signal
        samplerate: The rate at which samples were taken

    Returns:
        float: Spectral kurtosis
    """
    f_centroid = spectral_centroid(spectrum, samplerate)
    ps = np.abs(spectrum) ** 2
    ps_sum = 0.0
    ps_sum_weighted_2 = 0.0
    ps_sum_weighted_4 = 0.0
    for i, magnitude in enumerate(ps):
        f = 0.5 * samplerate / (len(ps) - 1) * i
        ps_sum += magnitude
        ps_sum_weighted_2 += magnitude * (f - f_centroid) ** 2
        ps_sum_weighted_4 += magnitude * (f - f_centroid) ** 4
    return (ps_sum_weighted_4 / ps_sum) / np.sqrt(ps_sum_weighted_2 / ps_sum) ** 4

def spectral_peak_frequency(
    spectrum: np.ndarray, samplerate: float
    ) -> float:
    """
    The frequency at which a signal or a waveform has its highest energy.
    The result is in the range of 0 Hz and the nyquist frequency.

    Args:
        spectrum: The amplitude against frequency representation of a signal
        samplerate: The rate at which samples were taken

    Returns:
        float: Spectral peak frequency
    """
    peak_bin = np.argmax(spectrum**2)
    return 0.5 * samplerate / (len(spectrum) - 1) * peak_bin

def spectral_rolloff(
    spectrum: np.ndarray, samplerate: float, rolloff: int
    ) -> float:
    """
    The frequency below which of the total energy of the spectrum is contained.
    Typical values for n (roll off) are 95, 90, 75 and 50.

    Args:
        spectrum: The amplitude against frequency representation of a signal
        samplerate: The rate at which samples were taken
        rolloff: roll-off point % limits [0,100]

    Returns:
        float: Spectral rolloff
    """
    ps = np.abs(spectrum) ** 2
    ps_sum_rolloff = (rolloff / 100) * np.sum(ps)
    ps_sum = 0.0
    for i, magnitude in enumerate(ps):
        ps_sum += magnitude
        if ps_sum >= ps_sum_rolloff:
            return 0.5 * samplerate / (len(ps) - 1) * i
    return 0.5 * samplerate

def spectral_skewness(
    spectrum: np.ndarray, samplerate: float
    ) -> float:
    """
    Measure of the asymmetry of the power spectrum around its mean, the spectral centroid.
    It indicates whether the bulk of the spectral power lies to the left or right of the centroid.
    Positive skewness: Indicates a spectrum with a tail extending towards higher frequencies.\n
    Negative skewness: Indicates a spectrum with a tail extending towards lower frequencies.\n
    Zero skewness: Indicates a symmetric spectrum around the centroid.\n

    Args:
        spectrum: The amplitude against frequency representation of a signal
        samplerate: The rate at which samples were taken

    Returns:
        float: Spectral skewness
    """
    f_centroid = spectral_centroid(spectrum, samplerate)
    ps = np.abs(spectrum) ** 2
    ps_sum = 0.0
    ps_sum_weighted_2 = 0.0
    ps_sum_weighted_3 = 0.0
    for i, magnitude in enumerate(ps):
        f = 0.5 * samplerate / (len(ps) - 1) * i
        ps_sum += magnitude
        ps_sum_weighted_2 += magnitude * (f - f_centroid) ** 2
        ps_sum_weighted_3 += magnitude * (f - f_centroid) ** 3
    return (ps_sum_weighted_3 / ps_sum) / np.sqrt(ps_sum_weighted_2 / ps_sum) ** 3

def spectral_variance(
    spectrum: np.ndarray, samplerate: float
    ) -> float:
    """
    Quantifies the spread or dispersion of the spectral content around its center of mass, the spectral centroid.
    
    Args:
        spectrum: The amplitude against frequency representation of a signal
        samplerate: The rate at which samples were taken

    Returns:
        float: spectral_variance
    
    """
    f_centroid = spectral_centroid(spectrum, samplerate)
    ps = np.abs(spectrum)
    ps_sum = 0.0
    ps_sum_weighted = 0.0
    for i, magnitude in enumerate(ps):
        f = 0.5 * samplerate / (len(ps) - 1) * i
        ps_sum += magnitude
        ps_sum_weighted += magnitude * (f - f_centroid) ** 2
    return ps_sum_weighted / ps_sum

def zero_crossing_rate(
    signal: np.ndarray, samplerate: float
    ) -> int:
    """
    Rate at which a signal changes from positive to zero to negative or from negative to zero to positive.

    Args:
        signal: The time domin representation of a signal
        samplerate: The rate at which samples were taken
    
    Returns:
        int: zero crossing rate
    """
    if len(signal) == 0:
        return 0
    crossings = 0
    was_positive = signal[0] >= 0
    for value in signal[1:]:
        is_positive = value >= 0
        if was_positive != is_positive:
            crossings += 1
        was_positive = is_positive
    return samplerate * crossings / len(signal)