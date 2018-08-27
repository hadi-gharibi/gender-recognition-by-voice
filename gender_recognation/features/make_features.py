from gender_recognation.features.wave_file import Wave
from gender_recognation.features.feature_extraction import FeatureExtraction
import pandas as pd
import os

fe = FeatureExtraction()


def path_to_spectrum(path, LPF=True, cutoff=280):
    snd = Wave.read_wave(path)
    if LPF: snd.low_pass_filter(cutoff=cutoff)
    return snd


def feature_extractor(snd):
    amp, freq, power = snd.amps, snd.fs, snd.power

    mean_freq = fe.mean_f(amp, freq)
    std_freq = fe.std_f(amp, freq)
    median_freq = fe.median_f(amp, freq)
    first_q = fe.first_quantile_f(amp, freq)
    third_q = fe.first_quantile_f(amp, freq)
    range_q = fe.inter_quantile_range_f(amp, freq)
    skewness = fe.skewness_f(amp, freq)
    kurtosis = fe.kurtosis_f(amp, freq)
    peak_freq = fe.peak_f(power, freq)

    return [mean_freq, std_freq, median_freq, first_q, third_q, range_q, skewness, kurtosis, peak_freq]


def df_feature_extractor(df):
    path = df.path
    snd = path_to_spectrum(path)
    return feature_extractor(snd)


if __name__ == '__main__':
    module_path = os.path.dirname(gender_recognation.__file__)
    df = pd.read_csv(os.path.join(module_path, 'data', 'csv', 'waves.csv'))

    df[['mean_freq', 'std_freq', 'median_freq', 'first_q', 'third_q', 'range_q', 'skewness', 'kurtosis', 'peak_freq']]=\
        df.apply(df_feature_extractor,axis=1, result_type="expand")

    df = df.to_csv(os.path.join(module_path, 'data', 'csv', 'features.csv'))