
from collections import deque


def josephus_simple(n, m):
    tecnicos = deque(range(1, n + 1))
    guardias = []

    while len(tecnicos) > 1:
        tecnicos.rotate(-m)
        seleccionado = tecnicos.popleft()
        guardias.append(seleccionado)

    return guardias, tecnicos[0]


if __name__ == "__main__":
    guardias, suplente = josephus_simple(5, 1)

    print("Orden de guardias:", guardias)
    print("Suplente:", suplente)
