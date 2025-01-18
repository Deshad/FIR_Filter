import sys
import pathlib
import os
import matplotlib.pyplot
import numpy as np

class Utility:
    OUTPUT_DIRS = {
        'svg': pathlib.Path('./image-files'),
        'dat': pathlib.Path('./processed-data-files')
    }

    def read_dat_realtime(file_path):
        with open(file_path, 'rb') as f:
            lines = f.readlines()
            line_count = 0
            while line_count < len(lines):
                sample = lines[line_count]
                line_count += 1
                yield float(sample)

    def save_svg(file_name: str, plt:matplotlib.pyplot):
        output_path = Utility.OUTPUT_DIRS['svg'].joinpath(file_name) 
        # if not os.path.exists(output_path):
        Utility.create_output_dir(Utility.OUTPUT_DIRS['svg'])
        plt.savefig(Utility.OUTPUT_DIRS['svg'].joinpath(file_name), format='svg')
    
    def create_output_dir(dir_path:str):
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
    
    def save_dat(file_name: str, signal_amplitudes:list[float]):
        try:
            output_path = Utility.OUTPUT_DIRS['dat'].joinpath(file_name) 
            Utility.create_output_dir(Utility.OUTPUT_DIRS['dat'])
            with open(output_path, 'w') as f:
                for amplitude in signal_amplitudes:
                    f.write(str(amplitude)+'\n')
        except FileNotFoundError:
            print('File not found', file=sys.stderr)
        except IOError:
            print('File not accessible', file=sys.stderr)

    def plot_frequency_domain(signal, sr, title, color):
        fft = np.fft.fft(signal)
        freq = np.fft.fftfreq(len(signal), d=1/sr)
        pos_indices = freq >= 0
        freq = freq[pos_indices]
        fft = np.abs(fft[pos_indices])
        matplotlib.pyplot.plot(freq, fft, color=color, label=title, alpha=0.7)
    
    def plot_time_domain(x, y, label, color, title, alpha=1.0):
        matplotlib.pyplot.plot(x, y, label=label, color=color, alpha=alpha)
        matplotlib.pyplot.title(title)
        matplotlib.pyplot.xlabel("Time (s)")
        matplotlib.pyplot.ylabel("Amplitude")
        matplotlib.pyplot.legend()
        matplotlib.pyplot.grid()
    
    def plot_time_domain_y(y, label, color, title):
        matplotlib.pyplot.plot(y, label=label, color=color)
        matplotlib.pyplot.title(title)
        matplotlib.pyplot.xlabel('Sample')
        matplotlib.pyplot.ylabel('Amplitude')
        matplotlib.pyplot.legend()
        matplotlib.pyplot.grid()
        