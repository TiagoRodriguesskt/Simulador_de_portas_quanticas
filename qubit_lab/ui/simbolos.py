"""Desenho das portas de vários qubits, igual na bancada, nas cartas, no álbum e no glossário.

    ●  controle            ⊕  alvo da CNOT/Toffoli
    ✕  um dos qubits trocados (SWAP, iSWAP, Fredkin)
    [Y] caixa com a letra: o alvo de uma porta controlada genérica (CY, CH, ...)

Portas controladas novas não precisam de código aqui: um nome como "CY" ou "CCH"
(C's na frente de uma porta de 1 qubit) vira controles + caixa automaticamente.

Todas as funções recebem a coordenada x da porta e a altura `ys` de cada fio,
na mesma ordem dos `alvos` (na CNOT: controle, alvo; na Fredkin: controle, a, b).
"""

import pygame

from ..core.portas import ANGULOS, PORTAS, partes
from . import estilo as E

# quais fios recebem um ponto de controle, um ⊕ ou um ✕, pela posição em `alvos`
FORMAS = {
    "CNOT": ["controle", "mais"],
    "TOFFOLI": ["controle", "controle", "mais"],
    "CZ": ["controle", "controle"],
    "SWAP": ["troca", "troca"],
    "ISWAP": ["troca", "troca"],
    "CSWAP": ["controle", "troca", "troca"],
    "CCZ": ["controle", "controle", "controle"],     # como a CZ: simétrica, só pontos
    "SQSWAP": ["troca", "troca"],                     # com uma plaquinha "√" no meio
    "MCX": ["controle", "controle", "controle", "mais"],
    "CUH": ["controle", "caixa:U"],                  # CU com outros ângulos
    # Ising: um bloco só cobrindo os dois fios, com o nome dentro
    "RXX": ["bloco", "bloco"],
    "RYY": ["bloco", "bloco"],
    "RZZ": ["bloco", "bloco"],
}

# texto da plaquinha no meio da linha das trocas
PLAQUINHAS = {"ISWAP": "i", "SQSWAP": "√"}


def formas(nome):
    """As formas de cada fio; para "CY", "CH", "CCH"...: controles + uma caixa com a letra."""
    if nome in FORMAS:
        return FORMAS[nome]
    alvo = nome.lstrip("C")
    controles = len(nome) - len(alvo)
    if controles and alvo in PORTAS and PORTAS[alvo].n_qubits == 1:
        return ["controle"] * controles + ["caixa:" + alvo]
    raise ValueError(f"Não sei desenhar a porta {nome!r} de vários qubits")


def _partes(nome):
    """`nome` pode ser o nome de uma porta ("RX") ou já o par (base, ângulo)."""
    return nome if isinstance(nome, tuple) else partes(nome)


def _tamanhos(nome, tam):
    """Tamanho da fonte da base e do ângulo: o ângulo vai menor, embaixo."""
    return tam, max(10, round(tam * 0.68))


def largura_rotulo(nome, tam) -> int:
    """Quantos pixels o rótulo da porta ocupa na horizontal."""
    base, angulo = _partes(nome)
    t_base, t_ang = _tamanhos(nome, tam)
    larg = E.fonte(t_base, True, True).size(base)[0]
    if angulo:
        larg = max(larg, E.fonte(t_ang, True, True).size(angulo)[0])
    return larg


def rotulo(tela, nome, centro, tam, cor):
    """O nome da porta: "H" numa linha; "Rx" com o ângulo "π/2" menor, embaixo."""
    base, angulo = _partes(nome)
    x, y = centro
    if not angulo:
        E.texto(tela, base, centro, tam, cor, mono=True, negrito=True, ancora="center")
        return
    t_base, t_ang = _tamanhos(nome, tam)
    E.texto(tela, base, (x, y - round(t_ang * 0.45)), t_base, cor, mono=True, negrito=True, ancora="center")
    E.texto(tela, angulo, (x, y + round(t_base * 0.55)), t_ang, cor, mono=True, ancora="center")


def caixa(tela, cor, centro, nome, escala=1.0, fundo=None):
    """A caixa da porta-alvo de uma controlada, com o nome dentro (e o ângulo, se houver)."""
    base, angulo = _partes(nome)
    tam = max(11, round((22 if len(base) <= 1 else 16) * escala))
    if angulo:
        tam = max(12, round(16 * escala))
    lado = round((44 if angulo else 40) * escala)
    r = pygame.Rect(0, 0, max(lado, largura_rotulo(nome, tam) + round(12 * escala)), lado)
    r.center = centro
    E.painel(tela, r, fundo or E.PAINEL_CLARO, cor, raio=max(4, round(8 * escala)),
             largura_borda=max(2, round(2 * escala)))
    rotulo(tela, nome, r.center, tam, cor)


def cruz(tela, cor, centro, meio, largura=3):
    """O ✕ da troca; `meio` é metade do tamanho."""
    x, y = centro
    pygame.draw.line(tela, cor, (x - meio, y - meio), (x + meio, y + meio), largura)
    pygame.draw.line(tela, cor, (x - meio, y + meio), (x + meio, y - meio), largura)


def desenhar_multi(tela, nome, x, ys, cor, escala=1.0, fundo=None):
    """Porta de vários qubits: linha vertical ligando os fios e uma forma em cada um.

    escala 1.0 é o tamanho da bancada; a carta usa um pouco maior.
    """
    fundo = fundo or E.FUNDO_FUNDO
    largura = max(2, round(3 * escala))
    if formas(nome)[0] == "bloco":
        _bloco(tela, nome, x, ys, cor, escala)
        return
    pygame.draw.line(tela, cor, (x, min(ys)), (x, max(ys)), largura)
    for forma, y in zip(formas(nome), ys):
        if forma == "controle":
            pygame.draw.circle(tela, cor, (x, y), round(9 * escala))
        elif forma == "mais":
            r = round(20 * escala)
            pygame.draw.circle(tela, fundo, (x, y), r)
            pygame.draw.circle(tela, cor, (x, y), r, largura)
            pygame.draw.line(tela, cor, (x - r, y), (x + r, y), largura)
            pygame.draw.line(tela, cor, (x, y - r), (x, y + r), largura)
        elif forma == "troca":
            cruz(tela, cor, (x, y), round(11 * escala), largura + 1)
        elif forma.startswith("caixa:"):
            # o ângulo é o da controlada: CU(π,0,π) mostra "U" com "π,0,π", não o ângulo da U sozinha
            alvo = forma[6:]
            angulo = partes(nome)[1] if nome in ANGULOS else partes(alvo)[1]
            caixa(tela, cor, (x, y), (partes(alvo)[0], angulo), escala)
    if nome in PLAQUINHAS:
        # o "i" da iSWAP ou o "√" da √SWAP, numa plaquinha no meio da linha entre os dois ✕
        trocas = [y for f, y in zip(FORMAS[nome], ys) if f == "troca"]
        meio_y = (trocas[0] + trocas[1]) // 2
        r = round(12 * escala)
        pygame.draw.circle(tela, fundo, (x, meio_y), r)
        pygame.draw.circle(tela, cor, (x, meio_y), r, max(1, largura - 1))
        E.texto(tela, PLAQUINHAS[nome], (x, meio_y), max(11, round(17 * escala)), cor, mono=True, negrito=True,
                ancora="center")


def _bloco(tela, nome, x, ys, cor, escala):
    """Uma caixa alta cobrindo todos os fios da porta (Ising XX, YY, ZZ)."""
    tam = max(12, round(16 * escala))
    meia_altura = round(20 * escala)
    larg = max(round(44 * escala), largura_rotulo(nome, tam) + round(14 * escala))
    r = pygame.Rect(0, 0, larg, max(ys) - min(ys) + 2 * meia_altura)
    r.center = (x, (min(ys) + max(ys)) // 2)
    E.painel(tela, r, E.PAINEL_CLARO, cor, raio=max(4, round(8 * escala)), largura_borda=max(2, round(2 * escala)))
    rotulo(tela, nome, r.center, tam, cor)


def largura_relativa(nome) -> float:
    """Largura da carta na bandeja, em relação a uma carta quadrada (H, X...)."""
    base, angulo = partes(nome)
    if angulo:
        return 1.4 if len(base) <= 2 else 1.5          # Rx(π/2), CRx(π/2)
    return 1.2 if len(base) >= 4 else 1.0              # CNOT, SWAP, iSWAP, CSWAP
