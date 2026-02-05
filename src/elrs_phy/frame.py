import numpy as np
from .signal import LoRaSignal

class ELRSFrame:
    """Klasa definiująca strukturę pakietu ELRS z zachowaniem ciągłości czasu."""
    
    def __init__(self, phy: LoRaSignal):
        self.phy = phy

    def build_packet(self, symbols: list) -> np.ndarray:
        """
        Składa ramkę ELRS: 17 Down, 2.25 Up, Payload (Down).
        Wszystko generowane względem czasu t=0 dla stabilności fazy.
        """
        segments = []

        # 1. Preambuła (17 Downchirpów)
        for _ in range(17):
            segments.append(self.phy.generate_chirp(direction='down'))

        # 2. Sync Word (2.25 Upchirpów)
        up_chirp = self.phy.generate_chirp(direction='up')
        segments.append(up_chirp)
        segments.append(up_chirp)
        # Fragment 0.25 symbolu
        n_quarter = self.phy.n_samples_per_symbol // 4
        segments.append(up_chirp[:n_quarter])

        # 3. Payload
        for sym in symbols:
            segments.append(self.phy.generate_chirp(symbol_val=sym, direction='down'))

        return np.concatenate(segments)