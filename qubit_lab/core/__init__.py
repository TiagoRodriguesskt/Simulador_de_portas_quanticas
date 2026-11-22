"""Núcleo do Qubit Lab: o simulador quântico, sem nenhuma parte gráfica.

    from qubit_lab.core import Estado, Circuito, PORTAS

    bell = Circuito(2).adicionar("H", [0]).adicionar("CNOT", [0, 1]).executar()
    print(bell)                 # Estado((|00⟩ + |11⟩)/√2)
    print(bell.bloch(0))        # [0. 0. 0.]  → emaranhado: vetor de Bloch "some"
"""

from .circuito import Circuito, Passo
from .estado import Estado, formatar
from .fase import Fase, Objetivo, Slot, carregar_fases
from .portas import PORTAS, Porta, eh_unitaria, porta, potencia
from .solver import Solucao, resolver
from .validador import problemas, validar

__all__ = [
    "Circuito", "Passo", "Estado", "formatar", "Fase", "Objetivo", "Slot",
    "carregar_fases", "PORTAS", "Porta", "eh_unitaria", "porta", "potencia",
    "Solucao", "resolver", "problemas", "validar",
]
