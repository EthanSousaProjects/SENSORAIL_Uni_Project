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
def band_energy(
    spectrum: np.ndarray, samplerate: float, f_lower: float, f_upper: float
    ) -> float:
        """
        The energy in an arbitrary frequency band.

        Args:
            spectrum: The time domain signal
            samplerate: The rate at which samples were taken
            f_lower: Lower frequency band
            f_upper: Upper frequency band

        Returns:
            float: power spectrum sum

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
            spectrum: The time domain signal
            samplerate: The rate at which samples were taken
            f_lower: Lower frequency band
            f_upper: Upper frequency band

        Returns:
            float: band enery ratio

        """
        powerspectrum = np.abs(spectrum) ** 2
        n = len(powerspectrum)
        n_lower = int(2 * n * f_lower / samplerate)
        n_upper = int(2 * n * f_upper / samplerate)

        return np.sum(powerspectrum[n_lower:n_upper]) / np.sum(powerspectrum)

#TODO: Add in all the rest of the functions on the webpage. Maybe package this all up and contribute to their site