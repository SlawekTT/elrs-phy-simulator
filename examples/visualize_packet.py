import matplotlib.pyplot as plt
from elrs_phy.signal import LoRaSignal
from elrs_phy.frame import ELRSFrame

def main():
    # Konfiguracja
    phy = LoRaSignal(sf=7, bw=500000, fs=2000000)
    frame_gen = ELRSFrame(phy)
    
    # Dane
    packet_data = [12, 64, 127, 0]
    iq_signal = frame_gen.build_packet(packet_data)
    noisy_signal = phy.add_awgn(iq_signal, snr_db=12)

    # Wizualizacja
    plt.figure(figsize=(12, 8))
    plt.specgram(noisy_signal, Fs=phy.fs, NFFT=512, noverlap=448, cmap='magma', sides='twosided')
    plt.title("ELRS Packet Generation - Production Ready Example")
    plt.show()

if __name__ == "__main__":
    main()