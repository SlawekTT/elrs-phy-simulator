import hashlib
import numpy as np

class FHSSManager:
    def __init__(self, binding_phrase: str, fs: int):
        self.phrase = binding_phrase
        self.fs = fs
        
        # Unikalny seed z hasła
        sha = hashlib.sha256(self.phrase.encode()).hexdigest()
        self.uid = int(sha[:8], 16)
        
        # 40 kanałów w paśmie 2.4GHz (zakres +/- 30MHz)
        self.channels = np.linspace(-30e6, 30e6, 40) 
        self.hopping_sequence = self._build_sequence()

    def _build_sequence(self):
        # Mieszanie oparte na seedzie
        np.random.seed(self.uid)
        return np.random.permutation(self.channels)

    def get_frequency_for_packet(self, packet_num: int) -> float:
        return self.hopping_sequence[packet_num % len(self.hopping_sequence)]