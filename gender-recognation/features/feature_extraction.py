import numpy as np

class FeatureExtraction:
    ''''
    Isolated class from the data
    We don't need to define the class each time we need to compute the features on new data
    '''

    def mean_f(self, amp, freq):
        return np.average(freq, weights =amp)

    def _moment_order_k(self, amp, freq, k):
        avg = self.mean_f(amp, freq)
        dev = amp * (freq - avg) ** k
        return dev.sum() / (amp.sum())

    def var_f(self, amp, freq):
        return self._moment_order_k(amp, freq, 2)

    def _std_f(self, amp, freq):
        return np.sqrt(self.var_f(amp, freq))

    def _weighted_percentile(self,data, percents, weights=None):
        '''
        percents in units of 1%
        weights specifies the frequency (count) of data.
        '''
        if weights is None:
            return np.percentile(data, percents)
        ind = np.argsort(data)
        d = data[ind]
        w = weights[ind]
        p = 1. * w.cumsum() / w.sum() * 100
        y = np.interp(percents, p, d)
        return y

    def median_f(self, amp, freq):
        return self._weighted_percentile(freq, 50, weights=amp)

    def first_quantile_f(self, amp, freq):
        return self._weighted_percentile(freq, 25, weights=amp)

    def third_quantile_f(self, amp, freq):
        return self._weighted_percentile(freq, 75, weights=amp)

    def inter_quantile_range_f(self,amp, freq):
        return self.third_quantile_f(amp, freq) - self.first_quantile_f(amp, freq)

    def skewness_f(self, amp, freq):
        m3 = self._moment_order_k(amp, freq, 3)
        sigma3 = np.power(self._std_f(amp, freq), 3)
        return m3 / sigma3

    def kurtosis_f(self, amp, freq):
        m4 = self._moment_order_k(amp, freq, 4)
        sigma4 = np.power(self._std_f(amp, freq), 4)
        return m4 / sigma4

    def peak_f(self, power, freq):
        return freq[power.argmax()]