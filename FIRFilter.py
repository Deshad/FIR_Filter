import numpy as np

class FIRFilter:
    def __init__(self, coefficients):
        self.coefficients = np.array(coefficients)
        self.delay_line = np.zeros(len(coefficients))
        
        # Initialise weights for adaptive LMS filter
        self.weights = np.zeros(len(coefficients))

    def dofilter(self, v):
        self.delay_line[1:] = self.delay_line[:-1]
        self.delay_line[0] = v
        return np.dot(self.delay_line, self.coefficients)
    
    def doFilterAdaptive(self, signal, noise, learningRate):
        # Update delay line with noise
        self.delay_line[1:] = self.delay_line[:-1]
        self.delay_line[0] = noise
        # Compute adaptive filter output
        y = np.dot(self.weights, self.delay_line)
        e = signal - y  # Error signal
        # Update weights using LMS algorithm
        self.weights += 2 * learningRate * e * self.delay_line
        return e