import numpy as np

def fir_taps(sr, cutoff_hp, pass_width, stop_width, atten=53):
    delta_f = min(cutoff_hp, pass_width, stop_width) / sr
    num_taps = int(np.ceil((atten - 8) / (2.285 * delta_f)))
    if num_taps % 2 == 0:
        num_taps += 1
    taps = np.arange(-num_taps//2, num_taps//2 + 1)
    return taps, num_taps

def fir_coefficients(sr, cutoff_hp, cutoff_bp, pass_width=5, cutoff_bs=50, stop_width=2):
    taps, num_taps = fir_taps(sr, cutoff_hp, pass_width, stop_width)
    # Highpass filter coefficients
    hp_coeffs = np.sinc(2 * cutoff_hp * (taps / sr))
    hp_coeffs = -hp_coeffs
    hp_coeffs[num_taps//2] += 1

    # Bandpass filter coefficients
    bp_low_cut = cutoff_bp - pass_width / 2
    bp_high_cut = cutoff_bp + pass_width / 2
    bp_low_coeffs = np.sinc(2 * bp_low_cut * (taps / sr))
    bp_high_coeffs = np.sinc(2 * bp_high_cut * (taps / sr))
    bp_coeffs = bp_high_coeffs - bp_low_coeffs

    # Bandstop filter coefficients
    bs_low_cut = cutoff_bs - stop_width / 2
    bs_high_cut = cutoff_bs + stop_width / 2
    bs_low_coeffs = np.sinc(2 * bs_low_cut * (taps / sr))
    bs_high_coeffs = np.sinc(2 * bs_high_cut * (taps / sr))
    bs_coeffs = bs_low_coeffs - bs_high_coeffs

    # Apply a Hamming window
    window = np.hamming(num_taps + 1)
    hp_coeffs *= window
    bp_coeffs *= window
    bs_coeffs *= window

    # Combine the filters
    combined_coeffs = hp_coeffs + bp_coeffs + bs_coeffs
    combined_coeffs /= np.sum(combined_coeffs)

    return combined_coeffs