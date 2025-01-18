#### Here we are using adaptive LMS filter and then plotting the adaptive LMS,
# R-peaks and the momentary heart beat are plotted.
import numpy as np
import matplotlib.pyplot as plt
from FilterCoefficients import *
from Utility import Utility
from FIRFilter import FIRFilter

def detect_r_peaks(signal, sampling_rate, threshold=0.5):
    peaks = []
    for i in range(1, len(signal) - 1):
        if signal[i] > threshold and signal[i] > signal[i - 1] and signal[i] > signal[i + 1]:
            peaks.append(i)
    return peaks

# 5. Main Execution for ECG Processing with Real-Time Data Reading
def main():
    # File paths for the ECG data files
    ecg_clean_file = './data-files/ecg_lying.dat'
    # ecg_noisy_file = './data-files/ecg_standing.dat'
    ecg_noisy_file = './processed-data-files/fir-filtered.dat'

    # FIR Filter parameters
    sampling_rate = 1000  # Hz
    # highpass_cutoff = 0.5  # Hz for high-pass filter
    # bandpass_cutoffs = [0.5, 50]  # Hz for band-pass filter
    highpass_cutoff = 40  # Hz for high-pass filter
    bandpass_cutoffs = [5, 50]  # Hz for band-pass filter

    pass_width = 3
    cutoff_bandstop = 50
    stop_width = 2

    # coefficients = calculate_fir_coefficients(sampling_rate, highpass_cutoff, bandpass_cutoffs)
    coefficients = fir_coefficients(sampling_rate, highpass_cutoff, bandpass_cutoffs[1], pass_width, cutoff_bandstop, stop_width)

    # Initialize filters
    fir_filter = FIRFilter(coefficients)
    # fir_filter_with_lms = FIRFilterWithLMS(coefficients)
    fir_filter_with_lms = FIRFilter(coefficients)
    learning_rate = 0.01

    # Simulated noise reference signal (50Hz + DC)
    noise_signal = (0.1 * np.sin(2 * np.pi * 50 * np.linspace(0, 1, 10000))).tolist()

    # Process data in real-time
    filtered_ecg = []
    adaptive_filtered_ecg = []
    noise_index = 0  # Index for noise signal

    for noisy_sample in Utility.read_dat_realtime(ecg_noisy_file):
        # FIR filtering
        filtered_sample = fir_filter.dofilter(noisy_sample)
        filtered_ecg.append(filtered_sample)

        # Adaptive LMS filtering
        # if noise_index < len(noise_signal):
        #     adaptive_sample = fir_filter_with_lms.do_filter_adaptive(noisy_sample, noise_signal[noise_index], learning_rate)
        #     adaptive_filtered_ecg.append(adaptive_sample)
        #     noise_index += 1

        # if noise_index < len(noise_signal):
        # adaptive_sample = fir_filter_with_lms.do_filter_adaptive(noisy_sample, noise_signal[noise_index], learning_rate)
        adaptive_sample = fir_filter_with_lms.doFilterAdaptive(noisy_sample, noise_signal[noise_index], learning_rate)
        adaptive_filtered_ecg.append(adaptive_sample)
            # noise_index += 1

    # R-Peak Detection and Heart Rate Calculation
    r_peaks = detect_r_peaks(adaptive_filtered_ecg, sampling_rate)
    rr_intervals = np.diff(r_peaks) / sampling_rate  # RR intervals in seconds
    heart_rate = 60 / rr_intervals  # Convert to beats per minute (BPM)

    # Plot Results
    plt.figure(figsize=(12, 8))

    # Plot Original and Filtered ECG
    plt.subplot(3, 1, 1)
    plt.plot(filtered_ecg, label='FIR Filtered ECG')
    plt.title('FIR Filtered ECG')
    plt.legend()

    plt.subplot(3, 1, 2)
    plt.plot(adaptive_filtered_ecg, label='Adaptive LMS Filtered ECG', color='green')
    plt.plot(r_peaks, [adaptive_filtered_ecg[p] for p in r_peaks], 'ro', label='R-peaks')
    plt.title('Adaptive LMS Filtered ECG with R-peaks')
    plt.legend()
# Plot adaptive filtering result
    if adaptive_filtered_ecg:
        plt.figure()
        plt.plot(adaptive_filtered_ecg, label='Adaptive LMS Filtered ECG')
        plt.legend()
        plt.xlabel('Sample')
        plt.ylabel('Amplitude')
        plt.title('LMS Adaptive Filtering of ECG')
        plt.show()
        
 # Plot Heart Rate
    plt.subplot(3, 1, 3)
    plt.plot(np.cumsum(rr_intervals), heart_rate, '-o', label='Heart Rate (BPM)')
    plt.xlabel('Time (s)')
    plt.ylabel('Heart Rate (BPM)')
    plt.title('Momentary Heart Rate')
    plt.legend()
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    main()
