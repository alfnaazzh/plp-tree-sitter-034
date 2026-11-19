import os
from pathlib import Path


def tambah(a, b):
    """Menjumlahkan dua angka."""
    return a + b


def sapa(nama):
    print("Halo", nama)


def tanpa_param():
    return 0


class Kalkulator:
    def kali(self, x, y):
        print(x * y)
        return x * y


print(tambah(1, 2))