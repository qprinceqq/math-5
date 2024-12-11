import random
import numpy as np

class ReedSolomon:
    def __init__(self, n, k):
        """
        n: Total number of symbols in the codeword (length of codeword)
        k: Number of data symbols (length of data)
        """
        if n <= k:
            raise ValueError("n must be greater than k")
        self.n = n
        self.k = k
        self.generator = self.generate_polynomial(n - k)

    def generate_polynomial(self, degree):
        """
        Generates a generator polynomial of given degree.
        """
        poly = [1]
        for i in range(degree):
            poly = np.convolve(poly, [1, pow(2, i, 256)]) % 256
        return np.array(poly, dtype=int)

    def encode(self, data):
        """
        Encodes the data using Reed-Solomon encoding.
        """
        if len(data) != self.k:
            raise ValueError("Data length must be equal to k")

        data_poly = np.array(data + [0] * (self.n - self.k), dtype=int)
        remainder = np.polydiv(data_poly, self.generator)[1] % 256
        codeword = (data_poly[:self.k] + remainder.tolist()) % 256
        return np.concatenate((data_poly[:self.k], remainder)).astype(int).tolist()

    def decode(self, received):
        """
        Decodes the received codeword and attempts error correction.
        """
        if len(received) != self.n:
            raise ValueError("Received message length must be equal to n")

        received = np.array(received, dtype=int)
        syndrome = np.polydiv(received, self.generator)[1] % 256

        if not np.any(syndrome):
            print("No errors detected.")
            return received[:self.k].tolist()

        print("Error detected. Implementing correction is non-trivial and requires additional algorithms.")
        return received[:self.k].tolist()

# Example usage
if __name__ == "__main__":
    n = 15  # Length of codeword
    k = 11  # Length of data
    rs = ReedSolomon(n, k)

    # Original data
    data = [random.randint(0, 255) for _ in range(k)]
    print("Original Data:", data)

    # Encoding
    encoded = rs.encode(data)
    print("Encoded Codeword:", encoded)

    # Simulating an error
    received = encoded.copy()
    received[2] = (received[2] + 1) % 256  # Introduce a small error
    print("Received Codeword (with error):", received)

    # Decoding
    decoded = rs.decode(received)
    print("Decoded Data:", decoded)
