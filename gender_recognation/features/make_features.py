from gender_recognation.features.wave_file import Wave
from gender_recognation.features.feature_extraction import FeatureExtraction
import pandas as pd
import os
import gender_recognation
from tqdm import *
import multiprocessing
import numpy as np

fe = FeatureExtraction()


def path_to_spectrum(path):
    snd = Wave.read_wave(path)
    #if LPF: snd.low_pass_filter(cutoff=cutoff)
    return snd


def feature_extractor(snd):
    amp, freq, power = snd.amps, snd.fs, snd.power

    mean_freq = fe.mean_f(amp, freq)
    std_freq = fe.std_f(amp, freq)
    median_freq = fe.median_f(amp, freq)
    first_q = fe.first_quantile_f(amp, freq)
    third_q = fe.third_quantile_f(amp, freq)
    range_q = fe.inter_quantile_range_f(amp, freq)
    skewness = fe.skewness_f(amp, freq)
    kurtosis = fe.kurtosis_f(amp, freq)
    peak_freq = fe.peak_f(power, freq)

    # LPF
    snd.low_pass_filter(cutoff=280)
    amp, freq, power = snd.amps, snd.fs, snd.power
    lp_mean_freq = fe.mean_f(amp, freq)
    lp_std_freq = fe.std_f(amp, freq)
    lp_median_freq = fe.median_f(amp, freq)
    lp_first_q = fe.first_quantile_f(amp, freq)
    lp_third_q = fe.third_quantile_f(amp, freq)
    lp_range_q = fe.inter_quantile_range_f(amp, freq)
    lp_skewness = fe.skewness_f(amp, freq)
    lp_kurtosis = fe.kurtosis_f(amp, freq)
    lp_peak_freq = fe.peak_f(power, freq)

    return [lp_mean_freq, lp_std_freq, lp_median_freq, lp_first_q, lp_third_q, lp_range_q, lp_skewness, lp_kurtosis,
            lp_peak_freq, mean_freq, std_freq, median_freq, first_q, third_q, range_q, skewness, kurtosis, peak_freq]


def df_feature_extractor(path):

    snd = path_to_spectrum(path)
    return pd.Series(feature_extractor(snd))


def _apply_df(args):
    df_, func, kwargs = args
    return df_.apply(func, **kwargs)


def apply_by_multiprocessing(df, func, **kwargs):
    workers = kwargs.pop('workers')
    chunks = kwargs.pop('chunks')
    pool = multiprocessing.Pool(processes=workers)
    result = list(tqdm(pool.imap(_apply_df, [(d, func, kwargs)
                                             for d in np.array_split(df, chunks)]), total=chunks))
    pool.close()
    return pd.concat(result)


if __name__ == '__main__':
    module_path = os.path.dirname(gender_recognation.__file__)
    df = pd.read_csv(os.path.join(module_path, 'data', 'csv', 'waves.csv'))

    df[['lp_mean_freq', 'lp_std_freq', 'lp_median_freq', 'lp_first_q', 'lp_third_q', 'lp_range_q', 'lp_skewness',
        'lp_kurtosis', 'lp_peak_freq''mean_freq', 'std_freq', 'median_freq', 'first_q', 'third_q', 'range_q',
        'skewness', 'kurtosis', 'peak_freq']] =\
        apply_by_multiprocessing(df.path, df_feature_extractor, workers=4,chunks=5000)


    df = df.to_csv(os.path.join(module_path, 'data', 'csv', 'features.csv'))