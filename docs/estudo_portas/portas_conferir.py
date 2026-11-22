"""Qubit Lab - as portas do guia de estudo, escritas em NumPy.

Este arquivo só DEFINE os estados, as portas e algumas ferramentas.
Os testes que conferem as contas do guia ficam em tests/test_guia_portas.py.
Para rodá-los (com o .venv ativado, na pasta do Qubit_Lab):

    pytest tests/test_guia_portas.py -v
"""
import numpy as np

# ---------- Estados ----------
ket0 = np.array([1, 0], dtype=complex)
ket1 = np.array([0, 1], dtype=complex)
plus = (ket0 + ket1) / np.sqrt(2)

# ---------- Portas de 1 qubit ----------
I = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]])
Z = np.array([[1, 0], [0, -1]], dtype=complex)
H = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
S = np.diag([1, 1j])
T = np.diag([1, np.exp(1j * np.pi / 4)])
SX = 0.5 * np.array([[1 + 1j, 1 - 1j], [1 - 1j, 1 + 1j]])


def rot(M, t):
    """exp(-i t/2 M), válido quando M·M = I (Paulis e produtos de Paulis)."""
    return np.cos(t / 2) * np.eye(len(M)) - 1j * np.sin(t / 2) * M


def Rx(t): return rot(X, t)
def Ry(t): return rot(Y, t)
def Rz(t): return rot(Z, t)
def P(l):  return np.diag([1, np.exp(1j * l)])


def U(t, f, l):
    return np.array([[np.cos(t/2), -np.exp(1j*l) * np.sin(t/2)],
                     [np.exp(1j*f) * np.sin(t/2), np.exp(1j*(f+l)) * np.cos(t/2)]])


# ---------- Ferramentas ----------
def bloch(psi):
    """Coordenadas (x, y, z) de 1 qubit na esfera de Bloch."""
    a, b = psi
    return np.round([2*(np.conj(a)*b).real, 2*(np.conj(a)*b).imag, abs(a)**2 - abs(b)**2], 3)


def emaranhado(psi):
    """Teste do guia para 2 qubits: produto se e só se a·d = b·c."""
    a, b, c, d = psi
    return not np.isclose(a * d, b * c)


def mesma_a_menos_de_fase(A, B):
    """True se A = e^{ia}·B, ou seja, se A e B diferem só por fase global."""
    k = np.argmax(abs(B))
    return np.allclose(A, A.flat[k] / B.flat[k] * B)


def controlada(Uu):
    """|0><0| ⊗ I + |1><1| ⊗ U"""
    P0, P1 = np.diag([1, 0]), np.diag([0, 1])
    return np.kron(P0, np.eye(len(Uu))) + np.kron(P1, Uu)


# ---------- Portas de 2 e 3 qubits ----------
CNOT, CY, CZ, CH = controlada(X), controlada(Y), controlada(Z), controlada(H)
SWAP = np.array([[1,0,0,0],[0,0,1,0],[0,1,0,0],[0,0,0,1]], dtype=complex)
iSWAP = np.array([[1,0,0,0],[0,0,1j,0],[0,1j,0,0],[0,0,0,1]])
sqrtSWAP = np.array([[1,0,0,0],[0,(1+1j)/2,(1-1j)/2,0],[0,(1-1j)/2,(1+1j)/2,0],[0,0,0,1]])
XX, YY, ZZ = np.kron(X, X), np.kron(Y, Y), np.kron(Z, Z)
def Rxx(t): return rot(XX, t)
def Ryy(t): return rot(YY, t)
def Rzz(t): return rot(ZZ, t)
def CP(l):  return controlada(P(l))
def CRz(t): return controlada(Rz(t))
TOFFOLI = controlada(CNOT)
CCZ = controlada(CZ)
CNOT_invertida = SWAP @ CNOT @ SWAP   # controle embaixo, alvo em cima
