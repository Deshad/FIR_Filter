import numpy as np
import matplotlib.pyplot as plt
from Utility import Utility
from FIRFilter import FIRFilter
from FilterCoefficients import *

if __name__ == '__main__':
    # Sampling rate and filter parameters
    sampling_rate = 1000
    cutoff_highpass = 40
    cutoff_bandpass = 50
    pass_width = 3
    cutoff_bandstop = 50
    stop_width = 2

    # Get filter coefficients
    coefficients = fir_coefficients(sampling_rate, cutoff_highpass, cutoff_bandpass, pass_width, cutoff_bandstop, stop_width)

    # Apply filter to noisy ECG sample-by-sample
    fir_filter_noisy = FIRFilter(coefficients)
    filtered_noisy_ecg = []
    
    # for sample in noisy_ecg:
    for sample in Utility.read_dat_realtime('./data-files/ecg_standing.dat'):
        filtered_sample = fir_filter_noisy.dofilter(sample)
        filtered_noisy_ecg.append(filtered_sample)
    filtered_noisy_ecg = np.array(filtered_noisy_ecg)

    # Plotting the signals
    plt.figure(figsize=(12, 10))

    # Generate time vectors
    time_vector_noisy = np.arange(len(filtered_noisy_ecg)) / sampling_rate

    # Frequency domain plots
    plt.subplot(3, 1, 1)
    # Load noisy ECG signals for plotting
    noisy_ecg = np.loadtxt('./data-files/ecg_standing.dat')
    clean_ecg = np.loadtxt('./data-files/ecg_lying.dat')
    Utility.plot_frequency_domain(noisy_ecg, sampling_rate, "Original Noisy ECG", "red")
    Utility.plot_frequency_domain(clean_ecg, sampling_rate, "Clean ECG", "green")
    Utility.plot_frequency_domain(filtered_noisy_ecg, sampling_rate, "Filtered ECG", "blue")
    

    # Time domain plots
    plt.xlim(0,70)
    plt.title("Frequency Domain")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude")
    plt.legend()
    plt.grid()

    plt.subplot(3, 1, 2)
    Utility.plot_time_domain(time_vector_noisy, noisy_ecg, 'Original Noisy ECG', 'red', 'Noisy ECG - Time Domain', alpha=0.6)

    plt.subplot(3, 1, 3)
    Utility.plot_time_domain(time_vector_noisy, filtered_noisy_ecg, 'Filtered ECG', 'blue', 'Filtered ECG - Time Domain')

    plt.tight_layout()
    Utility.save_svg('fir-filtering-other-2.svg', plt)
    plt.show()

    Utility.save_dat('fir-filtered.dat', filtered_noisy_ecg)
