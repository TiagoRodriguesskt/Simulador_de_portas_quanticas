"""Portas quânticas: as matrizes unitárias do jogo.

Convenção de ordem dos qubits (big-endian): o qubit 0 é o da ESQUERDA no ket.
Em |01⟩, o qubit 0 vale 0 e o qubit 1 vale 1. Para portas de vários qubits,
a ordem de `alvos` segue a mesma regra: na CNOT, alvos=(controle, alvo);
na Fredkin (CSWAP), alvos=(controle, a, b).
"""

from dataclasses import dataclass

import numpy as np

RAIZ2 = np.sqrt(2)


@dataclass(frozen=True)
class Porta:
    nome: str            # identificador usado nas fases ("H", "CNOT", ...)
    titulo: str          # nome para mostrar na tela
    matriz: np.ndarray   # unitária 2^k × 2^k
    descricao: str       # uma frase para a carta da porta

    @property
    def n_qubits(self) -> int:
        """Quantos qubits a porta usa (1 para H, 2 para CNOT, 3 para Toffoli)."""
        return int(np.log2(self.matriz.shape[0]))


def _m(linhas):
    return np.array(linhas, dtype=complex)


# ------------------------------------------------------------- 1 qubit ---
I = _m([[1, 0], [0, 1]])
X = _m([[0, 1], [1, 0]])
Y = _m([[0, -1j], [1j, 0]])
Z = _m([[1, 0], [0, -1]])
H = _m([[1, 1], [1, -1]]) / RAIZ2
S = _m([[1, 0], [0, 1j]])
T = _m([[1, 0], [0, np.exp(1j * np.pi / 4)]])
SDG = S.conj().T                         # S† (S conjugada): gira para o outro lado
TDG = T.conj().T                         # T† (T conjugada)
SX = _m([[1 + 1j, 1 - 1j], [1 - 1j, 1 + 1j]]) / 2   # √X: aplicada duas vezes, dá o X


def controlada(u: np.ndarray, controles: int = 1) -> np.ndarray:
    """A porta `u` com controles na frente: só age quando todos os controles são 1.

    controlada(X) é a CNOT; controlada(Z, 2) é a CCZ. Na matriz, é a identidade
    com `u` no canto de baixo, que é onde ficam os kets com os controles em 1.
    """
    n = u.shape[0] * 2 ** controles
    m = np.eye(n, dtype=complex)
    m[n - u.shape[0]:, n - u.shape[0]:] = u
    return m


# ---------------------------------------------------- rotações (π/2) ---
# No jogo, as rotações têm o ângulo fixo de π/2 (um quarto de volta).
# Rθ = e^(−iθ·σ/2): o ângulo θ é o quanto o vetor gira na esfera de Bloch.
def rx(theta):
    c, s = np.cos(theta / 2), np.sin(theta / 2)
    return _m([[c, -1j * s], [-1j * s, c]])


def ry(theta):
    c, s = np.cos(theta / 2), np.sin(theta / 2)
    return _m([[c, -s], [s, c]])


def rz(theta):
    return np.diag([np.exp(-1j * theta / 2), np.exp(1j * theta / 2)])


def fase_p(theta):
    """P(θ): só a amplitude de |1⟩ gira. P(π/2) = S, P(π/4) = T, P(π) = Z."""
    return np.diag([1, np.exp(1j * theta)]).astype(complex)


RX, RY, RZ, P = rx(np.pi / 2), ry(np.pi / 2), rz(np.pi / 2), fase_p(np.pi / 2)


def u3(theta, phi, lam):
    """U(θ, φ, λ): a porta geral de um qubit. Qualquer porta de um qubit é uma U (a menos de fase global)."""
    c, s = np.cos(theta / 2), np.sin(theta / 2)
    return _m([[c, -np.exp(1j * lam) * s],
               [np.exp(1j * phi) * s, np.exp(1j * (phi + lam)) * c]])


def ising(pauli, theta):
    """R_PP(θ) = e^(−iθ·P⊗P/2): o giro de dois qubits juntos (XX, YY ou ZZ)."""
    pp = np.kron(pauli, pauli)
    return np.cos(theta / 2) * np.eye(4) - 1j * np.sin(theta / 2) * pp


# ------------------------------------------------------------ 2 qubits ---
CNOT = _m([[1, 0, 0, 0],
           [0, 1, 0, 0],
           [0, 0, 0, 1],
           [0, 0, 1, 0]])
CZ = np.diag([1, 1, 1, -1]).astype(complex)
CY = controlada(Y)
CH = controlada(H)
SWAP = _m([[1, 0, 0, 0],
           [0, 0, 1, 0],
           [0, 1, 0, 0],
           [0, 0, 0, 1]])
ISWAP = _m([[1, 0, 0, 0],                 # troca os qubits e põe um i em |01⟩ e |10⟩
            [0, 0, 1j, 0],
            [0, 1j, 0, 0],
            [0, 0, 0, 1]])

# ------------------------------------------------------------ 3 qubits ---
TOFFOLI = np.eye(8, dtype=complex)
TOFFOLI[[6, 7]] = TOFFOLI[[7, 6]]          # troca |110⟩ ↔ |111⟩
CRX, CRY, CRZ, CP = controlada(RX), controlada(RY), controlada(RZ), controlada(P)
# só no glossário ("Outras portas"): exemplos com ângulos fixos
U = u3(np.pi / 2, 0, np.pi)                # U(π/2, 0, π) = H
UX = u3(np.pi, 0, np.pi)                   # U(π, 0, π) = X
US = u3(0, 0, np.pi / 2)                   # U(0, 0, π/2) = S
CU = controlada(u3(np.pi, 0, np.pi))       # CU(π, 0, π) = CNOT
CUH = controlada(u3(np.pi / 2, 0, np.pi))  # CU(π/2, 0, π) = CH
RXX, RYY, RZZ = (ising(m, np.pi / 2) for m in (X, Y, Z))
SQSWAP = _m([[1, 0, 0, 0],                 # √SWAP: aplicada duas vezes, dá a SWAP
             [0, (1 + 1j) / 2, (1 - 1j) / 2, 0],
             [0, (1 - 1j) / 2, (1 + 1j) / 2, 0],
             [0, 0, 0, 1]])
MCX = controlada(X, 3)                     # X com 3 controles (4 qubits)
CCZ = controlada(Z, 2)                     # só |111⟩ ganha o sinal de menos
CSWAP = np.eye(8, dtype=complex)           # Fredkin: SWAP controlada
CSWAP[[5, 6]] = CSWAP[[6, 5]]              # troca |101⟩ ↔ |110⟩


PORTAS = {
    p.nome: p
    for p in [
        Porta("X", "Pauli-X", X, "Meia volta em torno do eixo x: troca |0⟩ e |1⟩."),
        Porta("Y", "Pauli-Y", Y, "Meia volta em torno do eixo y."),
        Porta("Z", "Pauli-Z", Z, "Meia volta em torno do eixo z: inverte a fase de |1⟩."),
        Porta("H", "Hadamard", H, "Cria a superposição: leva os polos ao equador."),
        Porta("S", "Fase S", S, "Um quarto de volta em torno do eixo z."),
        Porta("T", "Fase T", T, "Um oitavo de volta em torno do eixo z."),
        Porta("SDG", "Fase S†", SDG, "Um quarto de volta em torno do eixo z, no sentido contrário da S."),
        Porta("TDG", "Fase T†", TDG, "Um oitavo de volta em torno do eixo z, no sentido contrário da T."),
        Porta("SX", "Raiz de X", SX, "Um quarto de volta em torno do eixo x: duas formam um X."),
        Porta("RX", "Rotação X", RX, "Um quarto de volta em torno do eixo x."),
        Porta("RY", "Rotação Y", RY, "Um quarto de volta em torno do eixo y."),
        Porta("RZ", "Rotação Z", RZ, "Um quarto de volta em torno do eixo z."),
        Porta("P", "Fase P", P, "Gira a fase de |1⟩ em π/2: igual à S."),
        Porta("CNOT", "CNOT", CNOT, "Se o controle for 1, aplica X no alvo."),
        Porta("CZ", "CZ", CZ, "Se os dois qubits forem 1, inverte a fase."),
        Porta("CY", "CY", CY, "Se o controle for 1, aplica Y no alvo."),
        Porta("CH", "CH", CH, "Se o controle for 1, aplica H no alvo."),
        Porta("CRX", "Rx controlada", CRX, "Se o controle for 1, aplica Rx(π/2) no alvo."),
        Porta("CRY", "Ry controlada", CRY, "Se o controle for 1, aplica Ry(π/2) no alvo."),
        Porta("CRZ", "Rz controlada", CRZ, "Se o controle for 1, aplica Rz(π/2) no alvo."),
        Porta("CP", "Fase controlada", CP, "Se os dois qubits forem 1, gira a fase em π/2."),
        Porta("SWAP", "SWAP", SWAP, "Troca o estado de dois qubits."),
        Porta("ISWAP", "iSWAP", ISWAP, "Troca dois qubits e dá um i de fase quando eles são diferentes."),
        Porta("TOFFOLI", "Toffoli", TOFFOLI, "Se os dois controles forem 1, aplica X no alvo."),
        Porta("CCZ", "CCZ", CCZ, "Se os três qubits forem 1, inverte a fase."),
        Porta("CSWAP", "Fredkin", CSWAP, "Se o controle for 1, troca os outros dois qubits."),
        # --- portas que entraram depois das 50 primeiras fases (e a MCX, só no glossário) ---
        Porta("I", "Identidade", I, "Não faz nada: o qubit fica como está."),
        Porta("U", "Porta U", U, "A porta geral de um qubit, aqui com os ângulos (π/2, 0, π)."),
        Porta("UX", "Porta U", UX, "A porta geral de um qubit, aqui com os ângulos (π, 0, π)."),
        Porta("US", "Porta U", US, "A porta geral de um qubit, aqui com os ângulos (0, 0, π/2)."),
        Porta("CU", "U controlada", CU, "Se o controle for 1, aplica U(π, 0, π) no alvo."),
        Porta("CUH", "U controlada", CUH, "Se o controle for 1, aplica U(π/2, 0, π) no alvo."),
        Porta("RXX", "Ising XX", RXX, "Gira os dois qubits juntos em torno de XX."),
        Porta("RYY", "Ising YY", RYY, "Gira os dois qubits juntos em torno de YY."),
        Porta("RZZ", "Ising ZZ", RZZ, "Gira os dois qubits juntos em torno de ZZ."),
        Porta("SQSWAP", "Raiz de SWAP", SQSWAP, "Meia troca: duas formam uma SWAP."),
        Porta("MCX", "X multicontrolada", MCX, "Se os três controles forem 1, aplica X no alvo."),
    ]
}


# Como cada porta aparece na tela, quando o nome interno é diferente
SIMBOLOS = {"SDG": "S†", "TDG": "T†", "TOFFOLI": "CCX", "SX": "√X", "ISWAP": "iSWAP", "SQSWAP": "√SWAP"}


# Portas com ângulo: o nome na tela e o ângulo fixo
ANGULOS = {"RX": ("Rx", "π/2"), "RY": ("Ry", "π/2"), "RZ": ("Rz", "π/2"), "P": ("P", "π/2"),
           "CRX": ("CRx", "π/2"), "CRY": ("CRy", "π/2"), "CRZ": ("CRz", "π/2"), "CP": ("CP", "π/2"),
           # exemplos do glossário
           "U": ("U", "π/2,0,π"), "UX": ("U", "π,0,π"), "US": ("U", "0,0,π/2"),
           "CU": ("CU", "π,0,π"), "CUH": ("CU", "π/2,0,π"),
           "RXX": ("Rxx", "π/2"), "RYY": ("Ryy", "π/2"), "RZZ": ("Rzz", "π/2")}


def partes(nome: str) -> tuple[str, str | None]:
    """O símbolo dividido em base e ângulo: partes("RX") == ("Rx", "π/2"); partes("H") == ("H", None)."""
    if nome in ANGULOS:
        return ANGULOS[nome]
    return SIMBOLOS.get(nome, nome), None


def simbolo(nome: str) -> str:
    """O nome para escrever numa linha: simbolo("SDG") == "S†", simbolo("RX") == "Rx(π/2)"."""
    base, angulo = partes(nome)
    return f"{base}({angulo})" if angulo else base


def porta(nome: str) -> Porta:
    """Busca uma porta pelo nome, com uma mensagem clara se não existir."""
    try:
        return PORTAS[nome]
    except KeyError:
        raise ValueError(f"Porta desconhecida: {nome!r}. Opções: {', '.join(PORTAS)}") from None


def eh_unitaria(m: np.ndarray, tol: float = 1e-10) -> bool:
    """U é unitária se U†U = I (a porta preserva a probabilidade total)."""
    return np.allclose(m.conj().T @ m, np.eye(m.shape[0]), atol=tol)


def potencia(m: np.ndarray, t: float) -> np.ndarray:
    """U^t: a porta aplicada "pela metade", "um terço"... (0 ≤ t ≤ 1).

    Usada para ANIMAR: em t=0 nada aconteceu, em t=1 a porta inteira agiu,
    e no meio o estado percorre um caminho contínuo (giro na esfera de Bloch).

    Como U é unitária, U = V·diag(e^{iθ})·V†, e U^t = V·diag(e^{iθ·t})·V†.
    Os ângulos θ são escolhidos em (-π, π], o caminho mais curto.
    """
    autovalores, V = np.linalg.eig(m)
    # para matrizes normais (como as unitárias) os autovetores podem ser
    # ortonormalizados; o QR garante isso mesmo com autovalores repetidos
    V, _ = np.linalg.qr(V)
    autovalores = np.diag(V.conj().T @ m @ V)
    angulos = np.angle(autovalores)
    return V @ np.diag(np.exp(1j * angulos * t)) @ V.conj().T
