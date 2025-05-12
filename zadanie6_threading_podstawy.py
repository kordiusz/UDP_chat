import threading
import time

# ZADANIE 6
# Wątek wypisujący tekst po 1 sekundzie

def wypisz():
    time.sleep(1)
    print("Cześć z wątku!")

# t = threading.Thread(target=wypisz)
# t.start()
# t.join()
