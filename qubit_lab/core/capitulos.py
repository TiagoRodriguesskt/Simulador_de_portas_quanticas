"""Em que fase cada porta é apresentada ao jogador (a carta de porta nova).

Uma fase só pode usar portas apresentadas nela ou antes dela.
"""

APRESENTACAO = {
    "X": 1,
    "H": 2,
    "Z": 4,
    "CNOT": 6,
    "S": 8,
    "T": 11,
    "TOFFOLI": 15,
    "CZ": 19,
    "Y": 21,
    "SDG": 22,
    "TDG": 23,
    "SX": 26,
    "SWAP": 31,
    "ISWAP": 33,
    "CSWAP": 35,
    "CY": 36,
    "CH": 37,
    "CCZ": 39,
    "RX": 41,
    "RY": 42,
    "RZ": 43,
    "P": 44,
    "CP": 46,
    "CRZ": 47,
    "CRX": 49,
    "CRY": 50,
    "RXX": 51,
    "RYY": 52,
    "RZZ": 53,
    "SQSWAP": 58,
    "U": 63,
    "UX": 64,
    "US": 65,
    "CU": 66,
    "CUH": 67,
    "I": 68,
    "MCX": 69,
}


def portas_conhecidas(id_fase: int) -> set[str]:
    """Portas que o jogador já conhece ao chegar na fase `id_fase`."""
    return {nome for nome, fase in APRESENTACAO.items() if fase <= id_fase}


def porta_nova(id_fase: int) -> str | None:
    """A porta apresentada nesta fase, se houver."""
    for nome, fase in APRESENTACAO.items():
        if fase == id_fase:
            return nome
    return None
