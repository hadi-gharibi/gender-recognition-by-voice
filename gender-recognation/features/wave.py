import numpy as np
import os
from wave import open as open_wave

def normalize(ys, amp=1.0):
    """Normalizes a wave array so the maximum amplitude is +amp or -amp.
    ys: wave array
    amp: max amplitude (pos or neg) in result
    returns: wave array
    """
    high, low = abs(max(ys)), abs(min(ys))
    return amp * ys / max(high, low)


class Wave:
    def __init__(self, ys, framerate):
        self.framerate = framerate
        self.ys = ys
        self.make_spectrum()

    @classmethod
    def read_wave(self, filename):
        """
        Reads a wave file.
        filename: string
        returns: Wave object
        """
        fp = open_wave(filename, 'r')

        nframes = fp.getnframes()
        sampwidth = np.int16
        framerate = fp.getframerate()

        z_str = fp.readframes(nframes)

        fp.close()
        ys = np.fromstring(z_str, dtype=sampwidth)

        ys = normalize(ys)
        return Wave(ys, framerate)

    def make_spectrum(self):
        """
        Computes the spectrum using FFT.
        hs: array of amplitudes (real)
        fs: array of frequencies
        framerate: frames per second
        full: boolean to indicate full or real FFT
        """
        n = len(self.ys)
        d = 1 / self.framerate

        self.hs = np.fft.rfft(self.ys)
        self.hs /= np.sqrt(len(self.hs))
        self.fs = np.fft.rfftfreq(n, d)

    def low_pass_filter(self, cutoff=280, factor=0):
        """
        Attenuate frequencies above the cutoff.
        cutoff: frequency in Hz
        factor: what to multiply the magnitude by
        """
        self.hs[abs(self.fs) > cutoff] *= factor

    @property
    def max_freq(self):
        """Returns the Nyquist frequency for this spectrum."""
        return self.framerate / 2

    @property
    def amps(self):
        """Returns a sequence of amplitudes (read-only property)."""
        return np.absolute(self.hs)

    @property
    def power(self):
        """Returns a sequence of powers (read-only property)."""
        return self.amps ** 2


