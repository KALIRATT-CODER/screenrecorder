from recorder import ScreenRecorder
from audio import AudioRecorder
from mouse import MouseTracker
from saver import Saver
import time

if __name__ == "__main__":
    print("[*] Démarrage de l'enregistrement...")

    screen = ScreenRecorder(fps=10)
    audio = AudioRecorder()
    mouse = MouseTracker()
    saver = Saver(screen, audio, mouse, interval=300)

    screen.start()
    audio.start()
    mouse.start()
    saver.start()

    print("[*] Enregistrement en cours. Ctrl+C pour arrêter.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[*] Arrêt...")
        saver.stop()
        screen.stop()
        audio.stop()
        mouse.stop()
        print("[+] Terminé. Fichiers dans le dossier recordings/")