"""Circuito quântico: uma sequência de passos aplicados ao estado.

Diferente do jogo clássico (um grafo de portas), aqui o circuito é uma linha
do tempo: cada passo aplica uma porta em certos qubits, da esquerda para a direita.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .estado import Estado
from .portas import porta as buscar_porta
from .portas import potencia


@dataclass(frozen=True)
class Passo:
    porta: str          # nome da porta ("H", "CNOT", …)
    alvos: tuple        # qubits em que ela age, ex.: (0,) ou (0, 1)

    def __post_init__(self):
        object.__setattr__(self, "alvos", tuple(self.alvos))
        p = buscar_porta(self.porta)
        if p.n_qubits != len(self.alvos):
            raise ValueError(f"{self.porta} usa {p.n_qubits} qubit(s), mas recebeu alvos {self.alvos}.")


class Circuito:
    def __init__(self, n_qubits: int, passos=()):
        self.n_qubits = n_qubits
        self.passos: list[Passo] = []
        for p in passos:
            if isinstance(p, Passo):
                self.adicionar(p.porta, p.alvos)
            else:
                self.adicionar(*p)          # aceita também tuplas ("H", (0,))

    def adicionar(self, nome: str, alvos) -> Circuito:
        """Acrescenta um passo; devolve o próprio circuito (para encadear)."""
        passo = Passo(nome, alvos)
        if any(not 0 <= a < self.n_qubits for a in passo.alvos):
            raise ValueError(f"Alvos {passo.alvos} fora do circuito de {self.n_qubits} qubit(s).")
        self.passos.append(passo)
        return self

    def executar(self, inicial: Estado | None = None) -> Estado:
        """Roda o circuito inteiro e devolve o estado final."""
        estado = inicial.copia() if inicial else Estado.zeros(self.n_qubits)
        for p in self.passos:
            estado = estado.aplicar(buscar_porta(p.porta), p.alvos)
        return estado

    def estados(self, inicial: Estado | None = None) -> list[Estado]:
        """O estado antes do circuito e depois de cada passo (n_passos + 1 estados)."""
        estado = inicial.copia() if inicial else Estado.zeros(self.n_qubits)
        lista = [estado]
        for p in self.passos:
            estado = estado.aplicar(buscar_porta(p.porta), p.alvos)
            lista.append(estado)
        return lista

    def animar(self, quadros_por_passo: int = 30, inicial: Estado | None = None) -> list[Estado]:
        """Estados intermediários para animar a esfera de Bloch e o som.

        Cada porta U é aplicada aos poucos, como U^t com t indo de 0 a 1,
        então o vetor de Bloch GIRA continuamente em vez de pular.
        """
        estado = inicial.copia() if inicial else Estado.zeros(self.n_qubits)
        quadros = [estado]
        for p in self.passos:
            matriz = buscar_porta(p.porta).matriz
            for i in range(1, quadros_por_passo + 1):
                t = i / quadros_por_passo
                t = t * t * (3 - 2 * t)                 # começa e termina devagar
                quadros.append(estado.aplicar(potencia(matriz, t), p.alvos))
            estado = estado.aplicar(matriz, p.alvos)    # termina exatamente no estado certo
            quadros[-1] = estado
        return quadros

    def unitaria(self) -> np.ndarray:
        """A matriz do circuito inteiro (útil para comparar circuitos)."""
        dim = 2 ** self.n_qubits
        colunas = []
        for i in range(dim):
            base = np.zeros(dim, dtype=complex)
            base[i] = 1
            colunas.append(self.executar(Estado(base)).vetor)
        return np.array(colunas).T

    def __len__(self):
        return len(self.passos)

    def __repr__(self):
        texto = " → ".join(f"{p.porta}{list(p.alvos)}" for p in self.passos) or "vazio"
        return f"Circuito({self.n_qubits} qubit(s): {texto})"
