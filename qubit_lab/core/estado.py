"""O estado quântico do jogo: um vetor de 2^n amplitudes complexas.

Para n qubits, o vetor tem uma amplitude para cada ket da base:
n=1 → |0⟩, |1⟩;  n=2 → |00⟩, |01⟩, |10⟩, |11⟩;  e assim por diante.
A probabilidade de medir um ket é |amplitude|².
"""

from __future__ import annotations

import numpy as np

from .portas import Porta

TOL = 1e-9

# Matrizes de Pauli, para calcular as coordenadas na esfera de Bloch
_PX = np.array([[0, 1], [1, 0]], dtype=complex)
_PY = np.array([[0, -1j], [1j, 0]], dtype=complex)
_PZ = np.array([[1, 0], [0, -1]], dtype=complex)


class Estado:
    def __init__(self, vetor, normalizar: bool = True):
        v = np.asarray(vetor, dtype=complex).ravel()
        n = int(round(np.log2(v.size)))
        if v.size != 2 ** n or n < 1:
            raise ValueError(f"O vetor precisa ter 2, 4, 8... amplitudes (recebeu {v.size}).")
        norma = np.linalg.norm(v)
        if norma < TOL:
            raise ValueError("O vetor de estado não pode ser nulo.")
        if normalizar:
            v = v / norma
        self.vetor = v
        self.n_qubits = n

    # ---------------------------------------------------------- criação ---
    @classmethod
    def zeros(cls, n_qubits: int) -> Estado:
        """|00…0⟩: o estado inicial de toda fase."""
        v = np.zeros(2 ** n_qubits, dtype=complex)
        v[0] = 1
        return cls(v)

    @classmethod
    def da_base(cls, bits: str) -> Estado:
        """Um ket da base escrito como texto: Estado.da_base("10") = |10⟩."""
        v = np.zeros(2 ** len(bits), dtype=complex)
        v[int(bits, 2)] = 1
        return cls(v)

    def copia(self) -> Estado:
        return Estado(self.vetor.copy(), normalizar=False)

    # ------------------------------------------------------ evolução -----
    def aplicar(self, p: Porta | np.ndarray, alvos) -> Estado:
        """Aplica uma porta nos qubits `alvos` e devolve o NOVO estado.

        Truque: o vetor de 2^n números é visto como um "cubo" com n eixos de
        tamanho 2 (um eixo por qubit). A porta age só nos eixos dos alvos.
        """
        m = p.matriz if isinstance(p, Porta) else np.asarray(p, dtype=complex)
        alvos = tuple(alvos)
        k = len(alvos)
        if m.shape != (2 ** k, 2 ** k):
            raise ValueError(f"A porta usa {int(np.log2(m.shape[0]))} qubit(s), mas recebeu alvos {alvos}.")
        if len(set(alvos)) != k or any(not 0 <= a < self.n_qubits for a in alvos):
            raise ValueError(f"Alvos inválidos {alvos} para {self.n_qubits} qubit(s).")

        n = self.n_qubits
        cubo = self.vetor.reshape((2,) * n)
        porta_tensor = m.reshape((2,) * (2 * k))
        # contrai as colunas da porta com os eixos dos alvos
        novo = np.tensordot(porta_tensor, cubo, axes=(list(range(k, 2 * k)), list(alvos)))
        # tensordot coloca os eixos dos alvos na frente: devolve cada um ao seu lugar
        novo = np.moveaxis(novo, list(range(k)), list(alvos))
        return Estado(novo.reshape(-1), normalizar=False)

    # ---------------------------------------------------- observáveis ---
    def probabilidades(self) -> np.ndarray:
        """|aₖ|² para cada ket da base, na ordem |00…0⟩, |00…1⟩, …"""
        return np.abs(self.vetor) ** 2

    def probabilidade(self, bits: str) -> float:
        """Chance de medir exatamente o ket `bits` (ex.: "1", "01")."""
        return float(self.probabilidades()[int(bits, 2)])

    def probabilidade_qubit(self, qubit: int, valor: int = 1) -> float:
        """Chance de o qubit `qubit` dar `valor` ao ser medido sozinho."""
        cubo = self.probabilidades().reshape((2,) * self.n_qubits)
        return float(np.take(cubo, valor, axis=qubit).sum())

    def matriz_reduzida(self, qubit: int) -> np.ndarray:
        """Matriz densidade 2×2 de um qubit (traço parcial dos outros).

        Se o qubit estiver emaranhado, ela é "misturada" e o vetor de Bloch
        fica mais curto que 1: é assim que a esfera mostra o emaranhamento.
        """
        cubo = np.moveaxis(self.vetor.reshape((2,) * self.n_qubits), qubit, 0).reshape(2, -1)
        return cubo @ cubo.conj().T

    def bloch(self, qubit: int = 0) -> np.ndarray:
        """Coordenadas (x, y, z) do qubit na esfera de Bloch.

        |0⟩ → (0, 0, 1)   |1⟩ → (0, 0, −1)   |+⟩ → (1, 0, 0)   |+i⟩ → (0, 1, 0)
        """
        rho = self.matriz_reduzida(qubit)
        return np.real([np.trace(rho @ _PX), np.trace(rho @ _PY), np.trace(rho @ _PZ)])

    def pureza(self, qubit: int = 0) -> float:
        """Tr(ρ²): 1 se o qubit está "sozinho", 0,5 se totalmente emaranhado."""
        rho = self.matriz_reduzida(qubit)
        return float(np.real(np.trace(rho @ rho)))

    def esta_emaranhado(self) -> bool:
        return any(self.pureza(q) < 1 - 1e-6 for q in range(self.n_qubits))

    def fidelidade(self, outro: Estado) -> float:
        """|⟨outro|este⟩|²: 1 se forem o mesmo estado (ignorando a fase global)."""
        return float(abs(np.vdot(outro.vetor, self.vetor)) ** 2)

    # -------------------------------------------------------- medição ---
    def medir(self, qubit: int, rng: np.random.Generator | None = None):
        """Mede um qubit. Devolve (resultado, estado colapsado).

        O resultado é sorteado com as probabilidades de Born, e o estado
        depois da medição só mantém os kets compatíveis com o resultado.
        """
        rng = rng or np.random.default_rng()
        p1 = self.probabilidade_qubit(qubit, 1)
        resultado = int(rng.random() < p1)
        cubo = self.vetor.reshape((2,) * self.n_qubits).copy()
        indice = [slice(None)] * self.n_qubits
        indice[qubit] = 1 - resultado
        cubo[tuple(indice)] = 0
        return resultado, Estado(cubo.reshape(-1))

    # ---------------------------------------------------------- texto ---
    def __repr__(self) -> str:
        return f"Estado({formatar(self.vetor)})"


# --------------------------------------------------------------- formatação ---
_FRACOES = [(1.0, ""), (1 / np.sqrt(2), "√2"), (0.5, "2"), (1 / np.sqrt(3), "√3"),
            (1 / np.sqrt(8), "2√2")]


def _coeficiente(z: complex) -> str:
    """Escreve 1, −1, i ou −i (para fases "bonitas"); senão um número curto."""
    for valor, texto in [(1, ""), (-1, "−"), (1j, "i"), (-1j, "−i")]:
        if abs(z - valor) < 1e-6:
            return texto
    fase = np.angle(z)
    for k, texto in [(1, "e^(iπ/4)"), (3, "e^(3iπ/4)"), (-1, "e^(−iπ/4)"), (-3, "e^(−3iπ/4)")]:
        if abs(fase - k * np.pi / 4) < 1e-6:
            # o tamanho conta: ½·e^(iπ/4) é "0.5e^(iπ/4)", não só "e^(iπ/4)"
            return texto if abs(abs(z) - 1) < 1e-4 else f"{round(abs(z), 3):g}{texto}"
    re, im = round(z.real, 3), round(z.imag, 3)
    if abs(im) < 1e-6:
        texto = f"{re:g}"
    elif abs(re) < 1e-6:
        texto = f"{im:g}i"
    else:
        texto = f"({re:g}{im:+g}i)"
    return texto.replace("-", "−")         # o mesmo sinal de menos do resto do texto


def formatar(vetor, manter_fase: bool = False) -> str:
    """Escreve o estado em notação de Dirac, como no livro.

    [0.707, 0.707]          → (|0⟩ + |1⟩)/√2
    [0.707, 0, 0, 0.707]    → (|00⟩ + |11⟩)/√2
    [0.6, 0.8]              → 0.6|0⟩ + 0.8|1⟩

    A fase global não muda nenhuma medida, então ela é tirada: [0, 1j] → |1⟩.
    Com manter_fase=True ela aparece na frente, como nas tabelas das portas:
    [0, 1j] → i|1⟩ (iSWAP|01⟩ = i|10⟩, Z|1⟩ = −|1⟩).
    """
    texto = _formatar_sem_fase(vetor)
    if not manter_fase:
        return texto
    v = np.asarray(vetor, dtype=complex)
    primeiro = next((a for a in v if abs(a) > 1e-6), 1)
    prefixo = _coeficiente(primeiro / abs(primeiro))
    if not prefixo:
        return texto
    if texto.startswith("(") or "|" not in texto[texto.index("⟩") + 1:]:
        return prefixo + texto           # i|10⟩, −(|0⟩ − |1⟩)/√2
    return f"{prefixo}({texto})"         # e^(iπ/4)(0.6|0⟩ + 0.8|1⟩)


def _formatar_sem_fase(vetor) -> str:
    v = np.asarray(vetor, dtype=complex)
    n = int(round(np.log2(v.size)))
    termos = [(format(i, f"0{n}b"), a) for i, a in enumerate(v) if abs(a) > 1e-6]
    if not termos:
        return "0"

    # fase global: deixa o primeiro coeficiente real e positivo
    fase_global = termos[0][1] / abs(termos[0][1])
    termos = [(b, a / fase_global) for b, a in termos]
    mods = [abs(a) for _, a in termos]

    divisor = None
    if np.allclose(mods, mods[0], atol=1e-6):
        for valor, texto in _FRACOES:
            if abs(mods[0] - valor) < 1e-6:
                divisor = texto
                break

    partes = []
    for i, (bits, a) in enumerate(termos):
        c = _coeficiente(a / mods[0]) if divisor is not None else _coeficiente(a)
        sinal_negativo = c.startswith("−")
        c = c[1:] if sinal_negativo else c
        if i == 0:
            partes.append(("−" if sinal_negativo else "") + f"{c}|{bits}⟩")
        else:
            partes.append((" − " if sinal_negativo else " + ") + f"{c}|{bits}⟩")
    corpo = "".join(partes)
    if divisor is None or divisor == "" or len(termos) == 1:
        return corpo
    return f"({corpo})/{divisor}"
