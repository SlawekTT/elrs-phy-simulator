import numpy as np

class ELRSConverter:
    """Narzędzia do konwersji danych binarnych na symbole LoRa."""

    @staticmethod
    def bytes_to_symbols(data: bytes, sf: int) -> list:
        """
        Konwertuje strumień bajtów na listę symboli LoRa.
        Każdy symbol ma wartość od 0 do (2^sf - 1).
        """
        # Konwersja bajtów na jeden długi ciąg bitów
        bits = "".join(f"{b:08b}" for b in data)
        
        symbols = []
        # Tniemy ciąg bitów na kawałki o długości SF
        for i in range(0, len(bits) - (len(bits) % sf), sf):
            chunk = bits[i:i+sf]
            symbols.append(int(chunk, 2))
            
        return symbols

    @staticmethod
    def apply_whitening(symbols: list, sf: int) -> list:
        """
        Proste wybielanie (XOR z sekwencją pseudolosową), 
        aby uniknąć powtarzających się wzorców.
        """
        seed = 0x12 # Uproszczony seed
        whitened = []
        for i, sym in enumerate(symbols):
            # Prosty generator lcg dla przykładu
            pseudo_rand = (i * 33 + seed) % (2**sf)
            whitened.append(sym ^ pseudo_rand)
        return whitened