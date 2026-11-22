"""Resolve uma fase por força bruta: testa todas as combinações de portas nos slots.

Com s slots e d portas disponíveis, cada slot pode ficar vazio ou receber uma
das d portas: são (d + 1)^s combinações. Para fases de jogo (poucos slots)
isso é instantâneo, igual ao solver do jogo clássico que testa 2^n chaves.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product

from .fase import Fase
from .portas import porta as buscar_porta

MAX_COMBINACOES = 200_000


@dataclass
class Solucao:
    solucoes: list[dict]          # cada uma: {índice do slot: porta}
    minimo_portas: int            # menor número de portas colocadas; -1 se impossível
    melhor: dict | None           # uma solução com o mínimo de portas
    total: int                    # combinações testadas

    @property
    def tem_solucao(self) -> bool:
        return self.minimo_portas >= 0


def opcoes_do_slot(fase: Fase, indice: int) -> list[str | None]:
    """Portas que cabem num slot (mesmo número de qubits que os alvos) + vazio.

    Numa fase "completo" (todos os slots preenchidos), o vazio não é opção.
    """
    n_alvos = len(fase.passos[indice].alvos)
    cabem = [p for p in fase.disponiveis if buscar_porta(p).n_qubits == n_alvos]
    return cabem if fase.completo else [None] + cabem


def resolver(fase: Fase) -> Solucao:
    slots = fase.slots
    opcoes = [opcoes_do_slot(fase, i) for i in slots]
    total = 1
    for o in opcoes:
        total *= len(o)
    if total > MAX_COMBINACOES:
        raise ValueError(f"Fase {fase.id} tem {total} combinações; o máximo é {MAX_COMBINACOES}.")

    solucoes, minimo, melhor = [], -1, None
    for combinacao in product(*opcoes):
        escolhas = {i: p for i, p in zip(slots, combinacao) if p is not None}
        if not fase.venceu(escolhas):
            continue
        solucoes.append(escolhas)
        if minimo == -1 or len(escolhas) < minimo:
            minimo, melhor = len(escolhas), escolhas
    return Solucao(solucoes, minimo, melhor, total)
