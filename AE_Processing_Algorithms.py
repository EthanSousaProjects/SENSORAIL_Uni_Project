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

#TODO: Add in a signal to spectrum function (believe it's the FFT thing Tom should know/ has done)

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


#TODO: Add in all the rest of the functions on the webpage. Maybe package this all up and contribute to their site