import threading
import time

# Funkcja, która będzie wykonywana przez wątki
def print_numbers(thread_name, delay, count):
    for i in range(count):
        time.sleep(delay)  # Symulacja jakiejś pracy (opóźnienie)
        print(f"{thread_name} - {i+1}")
        
# Tworzymy dwa wątki
thread1 = threading.Thread(target=print_numbers, args=("Wątek 1", 1, 5))
thread2 = threading.Thread(target=print_numbers, args=("Wątek 2", 1.5, 5))

# Uruchamiamy wątki
thread1.start()
thread2.start()

# Czekamy na zakończenie wątków
thread1.join()
thread2.join()

print("Wszystkie wątki zakończone.")

