"""Confere se uma fase é justa e jogável antes de ela entrar no jogo.

Regras (as mesmas ideias do validador do jogo clássico):
1. Toda porta citada existe e tem o número certo de alvos.
2. A fase só usa portas já apresentadas (capitulos.py).
3. Com os slots vazios, a fase NÃO está vencida (o detector começa apagado).
4. Existe pelo menos uma solução.
5. Toda porta disponível cabe em algum slot (nada inútil na bandeja).
"""

from __future__ import annotations

from .capitulos import portas_conhecidas
from .circuito import Passo
from .fase import Fase
from .portas import PORTAS
from .portas import porta as buscar_porta
from .solver import opcoes_do_slot, resolver


def problemas(fase: Fase) -> list[str]:
    """Lista de problemas encontrados; lista vazia = fase válida."""
    erros = []
    conhecidas = portas_conhecidas(fase.id)

    usadas = {p.porta for p in fase.passos if isinstance(p, Passo)} | set(fase.disponiveis)
    for nome in sorted(usadas):
        if nome not in PORTAS:
            erros.append(f"porta desconhecida: {nome}")
        elif nome not in conhecidas:
            erros.append(f"usa {nome} antes de ela ser apresentada")

    for i, p in enumerate(fase.passos):
        if any(not 0 <= a < fase.n_qubits for a in p.alvos):
            erros.append(f"passo {i}: alvos {p.alvos} fora dos {fase.n_qubits} qubit(s)")

    if not fase.slots:
        erros.append("a fase não tem nenhum slot para o jogador")

    if erros:                  # sem portas válidas não dá para simular
        return erros

    for nome in fase.disponiveis:
        n = buscar_porta(nome).n_qubits
        if not any(nome in opcoes_do_slot(fase, i) for i in fase.slots):
            erros.append(f"{nome} ({n} qubit(s)) não cabe em nenhum slot")

    if fase.venceu({}):
        erros.append("a fase já começa vencida, com os slots vazios")

    if not resolver(fase).tem_solucao:
        erros.append("a fase não tem solução")

    return erros


def validar(fase: Fase) -> None:
    """Como `problemas`, mas lança um erro com a lista, se houver."""
    lista = problemas(fase)
    if lista:
        raise ValueError(f"Fase {fase.id} ({fase.titulo}) inválida:\n- " + "\n- ".join(lista))
