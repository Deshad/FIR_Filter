import matplotlib.pyplot as plt
from FIRFilter import FIRFilter
from FilterCoefficients import *
from Utility import Utility

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

    # Initialize filters
    fir_filter = FIRFilter(coefficients)
    fir_filter_with_lms = FIRFilter(coefficients)
    learning_rate = 0.01

    # Simulated noise reference signal (50Hz + DC)
    noise_signal = (0.1 * np.sin(2 * np.pi * 50 * np.linspace(0, 1, 10000))).tolist()

    # Process data in real-time
    filtered_ecg = []
    adaptive_filtered_ecg = []
    noise_index = 0  # Index for noise signal

    filtered_ecg_file = './processed-data-files/fir-filtered.dat'
    for noisy_sample in Utility.read_dat_realtime(filtered_ecg_file):
        # FIR filtering
        filtered_sample = fir_filter.dofilter(noisy_sample)
        filtered_ecg.append(filtered_sample)

        # Adaptive LMS filtering
        adaptive_sample = fir_filter_with_lms.doFilterAdaptive(noisy_sample, noise_signal[noise_index], learning_rate)
        adaptive_filtered_ecg.append(adaptive_sample)

    # Plot Results
    plt.figure(figsize=(9, 8))

    # Plot filtered ECG
    plt.subplot(3, 1, 1)
    Utility.plot_time_domain_y(filtered_ecg, label='FIR Filtered ECG', color='red', title='FIR Filtered ECG')

    # Plot adaptive filtering result
    plt.subplot(3, 1, 2)
    Utility.plot_time_domain_y(adaptive_filtered_ecg, label='Adaptive LMS Filtered ECG', color='blue', title='LMS Adaptive Filtered ECG')

    plt.tight_layout()
    Utility.save_svg('comparison-adaptive-lms-with-no-lms-2.svg', plt)
    plt.show()

    Utility.save_dat('lms-filtered-ecg.dat', adaptive_filtered_ecg)