import numpy as np
import matplotlib.pyplot as plt
from elrs_phy.signal import LoRaSignal
from elrs_phy.frame import ELRSFrame
from elrs_phy.fhss import FHSSManager

def save_iq(signal, filename):
    # Konwersja na format 32-bit float (interleaved I, Q, I, Q...)
    iq_data = signal.astype(np.complex64)
    with open(filename, 'wb') as f:
        f.write(iq_data.tobytes())
    print(f"Sygnał zapisany do: {filename}")

def main():
    # 1. Parametry bazowe
    fs = 80_000_000  # 80 MHz - pasmo widzenia dla 2.4 GHz
    sf = 7
    bw = 500_000
    
    # Inicjalizacja komponentów
    phy = LoRaSignal(sf=sf, bw=bw, fs=fs)
    frame_gen = ELRSFrame(phy)
    
    # Manager FHSS - upewnij się, że fhss.py używa np.random.permutation
    fhss = FHSSManager(binding_phrase="tajne_hasło", fs=fs)
    
    total_signal_list = []
    
    print(f"Generowanie 15 pakietów ELRS dla frazy: '{fhss.phrase}'")

    # 2. Pętla generująca pakiety
    for packet_idx in range(15):
        # Pobieramy offset częstotliwości dla tego konkretnego pakietu
        freq_offset = fhss.get_frequency_for_packet(packet_idx)
        
        # BUDOWA PAKIETU: Zawsze od t=0 (brak start_time w argumentach!)
        # To gwarantuje, że pakiety będą poziome i stabilne
        packet_iq = frame_gen.build_packet(symbols=[packet_idx, 64, 100])
        
        # MODULACJA FHSS: Przesunięcie robimy na lokalnym czasie pakietu
        t_local = np.arange(len(packet_iq)) / fs
        shifted_packet = packet_iq * np.exp(1j * 2 * np.pi * freq_offset * t_local)
        
        # Dodajemy przesunięty pakiet do listy
        total_signal_list.append(shifted_packet)
        
        # Dodajemy przerwę (5ms ciszy), aby oddzielić pakiety na wykresie
        pause_samples = int(fs * 0.005)
        total_signal_list.append(np.zeros(pause_samples, dtype=complex))
        
        print(f"Pakiet {packet_idx:02d} nadany na: {freq_offset/1e6:+.2f} MHz")

    # Łączymy wszystko w jeden długi sygnał
    final_iq = np.concatenate(total_signal_list)
    
    # Dodajemy szum tła
    final_iq = phy.add_awgn(final_iq, snr_db=25)

    save_iq(final_iq, "elrs_fhss_capture.iq")
    
    # 3. Wizualizacja
    plt.figure(figsize=(14, 8))
    
    # Ustawienie NFFT=1024 i noverlap=512 dla optymalnej ostrości
    plt.specgram(
        final_iq, 
        Fs=fs, 
        NFFT=1024, 
        noverlap=512, 
        cmap='magma', 
        sides='twosided'
    )
    
    plt.title(f"ELRS FHSS Simulation - Skok co pakiet\nBinding: {fhss.phrase}")
    plt.xlabel("Czas [s]")
    plt.ylabel("Częstotliwość [Hz]")
    plt.ylim(-40e6, 40e6)
    plt.colorbar(label='Moc [dB]')
    
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()