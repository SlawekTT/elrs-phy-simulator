import numpy as np

class LoRaSignal:
    """Klasa odpowiedzialna za generowanie podstawowych sygnałów LoRa."""

    def __init__(self, sf: int, bw: int, fs: int):
        self.sf = sf
        self.bw = bw
        self.fs = fs
        # Liczba próbek na jeden symbol
        self.n_samples_per_symbol = int(fs * (2**sf) / bw)
        # WEKTOR CZASU DLA JEDNEGO SYMBOLU (OD 0 DO T_sym)
        # To tej linii prawdopodobnie Ci brakuje:
        self.t = np.arange(self.n_samples_per_symbol) / fs

    def generate_chirp(self, symbol_val: int = 0, direction: str = 'up') -> np.ndarray:
        """Generuje pojedynczy symbol LoRa (chirp) zawsze od t=0."""
        T = (2**self.sf) / self.bw
        k = (self.bw / T) if direction == 'up' else -(self.bw / T)
        f0 = -self.bw/2 if direction == 'up' else self.bw/2

        # Używamy self.t, który jest zdefiniowany w __init__
        phase = 2 * np.pi * (f0 * self.t + 0.5 * k * self.t**2)
        symbol = np.exp(1j * phase)

        if symbol_val > 0:
            shift = int((symbol_val / 2**self.sf) * self.n_samples_per_symbol)
            symbol = np.roll(symbol, -shift)
        
        return symbol
    
    @staticmethod
    def add_awgn(signal: np.ndarray, snr_db: float) -> np.ndarray:
        sig_pwr = np.mean(np.abs(signal)**2)
        noise_pwr = sig_pwr / (10**(snr_db / 10.0))
        noise = np.sqrt(noise_pwr/2) * (np.random.randn(len(signal)) + 1j*np.random.randn(len(signal)))
        return signal + noise