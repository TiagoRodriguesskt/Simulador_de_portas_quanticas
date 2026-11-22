"""Testes do simulador quântico (qubit_lab/core)."""

import numpy as np
import pytest

from qubit_lab.core import (
    PORTAS, Circuito, Estado, Fase, carregar_fases, eh_unitaria, formatar,
    potencia, problemas, resolver,
)

R2 = 1 / np.sqrt(2)


# ------------------------------------------------------------------ portas ---
@pytest.mark.parametrize("nome", list(PORTAS))
def test_toda_porta_eh_unitaria(nome):
    assert eh_unitaria(PORTAS[nome].matriz)


@pytest.mark.parametrize("nome", list(PORTAS))
@pytest.mark.parametrize("t", [0.0, 0.25, 0.5, 0.9, 1.0])
def test_potencia_fracionaria(nome, t):
    m = PORTAS[nome].matriz
    u = potencia(m, t)
    assert eh_unitaria(u)
    if t == 0:
        assert np.allclose(u, np.eye(len(m)))
    if t == 1:
        assert np.allclose(u, m)


def test_metade_mais_metade_eh_a_porta_inteira():
    for nome in ["X", "H", "Z", "CNOT"]:
        m = PORTAS[nome].matriz
        meia = potencia(m, 0.5)
        assert np.allclose(meia @ meia, m)


def test_identidades_classicas():
    unit = lambda *nomes: Circuito(1, [(n, (0,)) for n in nomes]).unitaria()
    assert np.allclose(unit("H", "H"), np.eye(2))            # H·H = I
    assert np.allclose(unit("H", "Z", "H"), PORTAS["X"].matriz)   # HZH = X
    assert np.allclose(unit("H", "X", "H"), PORTAS["Z"].matriz)   # HXH = Z
    assert np.allclose(unit("S", "S"), PORTAS["Z"].matriz)        # S² = Z
    assert np.allclose(unit("T", "T"), PORTAS["S"].matriz)        # T² = S


# ------------------------------------------------------------------ estado ---
def test_hadamard_cria_superposicao():
    e = Estado.zeros(1).aplicar(PORTAS["H"], [0])
    assert np.allclose(e.vetor, [R2, R2])
    assert np.allclose(e.probabilidades(), [0.5, 0.5])


@pytest.mark.parametrize("portas, esperado", [
    ([], (0, 0, 1)),            # |0⟩  polo norte
    (["X"], (0, 0, -1)),        # |1⟩  polo sul
    (["H"], (1, 0, 0)),         # |+⟩  eixo x
    (["X", "H"], (-1, 0, 0)),   # |−⟩
    (["H", "S"], (0, 1, 0)),    # |+i⟩ eixo y
])
def test_coordenadas_de_bloch(portas, esperado):
    c = Circuito(1, [(p, (0,)) for p in portas])
    assert np.allclose(c.executar().bloch(0), esperado)


def test_ordem_dos_qubits_big_endian():
    e = Estado.zeros(2).aplicar(PORTAS["X"], [1])
    assert e.probabilidade("01") == pytest.approx(1)
    e = Estado.zeros(2).aplicar(PORTAS["X"], [0])
    assert e.probabilidade("10") == pytest.approx(1)


def test_cnot_respeita_controle_e_alvo():
    cnot = PORTAS["CNOT"]
    assert Estado.da_base("10").aplicar(cnot, [0, 1]).probabilidade("11") == pytest.approx(1)
    assert Estado.da_base("01").aplicar(cnot, [0, 1]).probabilidade("01") == pytest.approx(1)
    assert Estado.da_base("01").aplicar(cnot, [1, 0]).probabilidade("11") == pytest.approx(1)


def test_toffoli_eh_um_and_reversivel():
    for a in "01":
        for b in "01":
            e = Estado.da_base(a + b + "0").aplicar(PORTAS["TOFFOLI"], [0, 1, 2])
            esperado = a + b + str(int(a) & int(b))
            assert e.probabilidade(esperado) == pytest.approx(1)


def test_estado_de_bell_eh_emaranhado():
    bell = Circuito(2).adicionar("H", [0]).adicionar("CNOT", [0, 1]).executar()
    assert np.allclose(bell.vetor, [R2, 0, 0, R2])
    assert np.allclose(bell.bloch(0), 0) and np.allclose(bell.bloch(1), 0)
    assert bell.pureza(0) == pytest.approx(0.5)
    assert bell.esta_emaranhado()
    assert not Estado.zeros(2).aplicar(PORTAS["H"], [0]).esta_emaranhado()


def test_medicao_colapsa_e_segue_as_probabilidades():
    rng = np.random.default_rng(42)
    mais = Estado([1, 1])
    resultados = [mais.medir(0, rng)[0] for _ in range(4000)]
    assert 0.46 < np.mean(resultados) < 0.54
    r, depois = mais.medir(0, rng)
    assert depois.probabilidade(str(r)) == pytest.approx(1)


def test_medir_um_qubit_do_bell_define_o_outro():
    bell = Circuito(2).adicionar("H", [0]).adicionar("CNOT", [0, 1]).executar()
    rng = np.random.default_rng(7)
    for _ in range(50):
        r, depois = bell.medir(0, rng)
        assert depois.probabilidade_qubit(1, r) == pytest.approx(1)


def test_fidelidade_ignora_fase_global():
    a = Estado([1, 1])
    b = Estado([1j, 1j])
    assert a.fidelidade(b) == pytest.approx(1)
    assert a.fidelidade(Estado([1, -1])) == pytest.approx(0)


@pytest.mark.parametrize("vetor, texto", [
    ([1, 0], "|0⟩"),
    ([R2, R2], "(|0⟩ + |1⟩)/√2"),
    ([R2, -R2], "(|0⟩ − |1⟩)/√2"),
    ([R2, 1j * R2], "(|0⟩ + i|1⟩)/√2"),
    ([R2, 0, 0, R2], "(|00⟩ + |11⟩)/√2"),
    ([0.5, 0.5, 0.5, -0.5], "(|00⟩ + |01⟩ + |10⟩ − |11⟩)/2"),
    ([0.6, 0.8], "0.6|0⟩ + 0.8|1⟩"),
    ([0, 1j], "|1⟩"),
    ([0.6, -0.8j], "0.6|0⟩ − 0.8i|1⟩"),
    ([0.6, -0.8], "0.6|0⟩ − 0.8|1⟩"),
    # o tamanho da amplitude não some quando a fase é "bonita" (bug encontrado na fase 61)
    ([R2, 0.5 * np.exp(1j * np.pi / 4), 0.5 * np.exp(-1j * np.pi / 4), 0],
     "0.707|00⟩ + 0.5e^(iπ/4)|01⟩ + 0.5e^(−iπ/4)|10⟩"),
])
def test_formatar_em_notacao_de_dirac(vetor, texto):
    assert formatar(vetor) == texto


@pytest.mark.parametrize("vetor, texto", [
    ([0, 1j], "i|1⟩"),
    ([0, -1], "−|1⟩"),
    ([0, 0, 1j, 0], "i|10⟩"),
    ([-R2, R2], "−(|0⟩ − |1⟩)/√2"),
    ([1, 0], "|0⟩"),
])
def test_formatar_mantendo_a_fase_global(vetor, texto):
    assert formatar(vetor, manter_fase=True) == texto
    assert "i|" not in formatar([0, 0, 1j, 0])          # sem a opção, a fase global sai


def test_erros_claros():
    with pytest.raises(ValueError):
        Estado.zeros(1).aplicar(PORTAS["CNOT"], [0])
    with pytest.raises(ValueError):
        Circuito(1).adicionar("H", [3])
    with pytest.raises(ValueError):
        Circuito(1).adicionar("Q", [0])


# ---------------------------------------------------------------- circuito ---
def test_animacao_termina_no_estado_certo_e_gira_aos_poucos():
    c = Circuito(1).adicionar("H", [0])
    quadros = c.animar(quadros_por_passo=20)
    assert len(quadros) == 21
    assert np.allclose(quadros[-1].vetor, c.executar().vetor)
    # o vetor de Bloch anda em passos pequenos, sem pular
    pontos = np.array([q.bloch(0) for q in quadros])
    assert np.max(np.linalg.norm(np.diff(pontos, axis=0), axis=1)) < 0.3
    # e fica sempre na superfície da esfera (estado puro)
    assert np.allclose(np.linalg.norm(pontos, axis=1), 1)


# ------------------------------------------------------------------- fases ---
FASES = carregar_fases()


def test_existem_fases():
    assert len(FASES) >= 7
    assert [f.id for f in FASES] == list(range(1, len(FASES) + 1))


@pytest.mark.parametrize("fase", FASES, ids=lambda f: f"fase{f.id:02d}")
def test_toda_fase_eh_valida(fase):
    assert problemas(fase) == []


@pytest.mark.parametrize("fase", FASES, ids=lambda f: f"fase{f.id:02d}")
def test_melhor_solucao_do_solver_vence(fase):
    s = resolver(fase)
    assert fase.venceu(s.melhor)


def test_fase_4_so_o_z_resolve():
    fase = next(f for f in FASES if f.id == 4)
    s = resolver(fase)
    assert s.solucoes == [{1: "Z"}]


def test_jogador_preenche_slots():
    fase = next(f for f in FASES if f.id == 4)
    assert not fase.venceu()
    fase.escolher(1, "X")
    assert not fase.venceu()
    fase.escolher(1, "Z")
    assert fase.venceu()
    with pytest.raises(ValueError):
        fase.escolher(1, "S")          # S só aparece na fase 8


def test_objetivo_de_um_qubit_e_de_bloch():
    deutsch = next(f for f in FASES if f.objetivo.tipo == "qubit")
    assert deutsch.venceu(resolver(deutsch).melhor)
    teleporte = next(f for f in FASES if f.objetivo.tipo == "bloch")
    final = teleporte.resultado(resolver(teleporte).melhor)
    # o qubit 2 recebeu o estado (|0⟩ + e^(iπ/4)|1⟩)/√2 que estava no qubit 0
    assert np.allclose(final.bloch(2), [R2, R2, 0])


def test_capitulos_e_portas_novas():
    from qubit_lab.core.capitulos import APRESENTACAO
    assert len(FASES) == 100                                   # o jogo completo
    assert {"S", "T", "TOFFOLI", "CZ", "Y", "SDG", "TDG", "SX", "SWAP", "ISWAP", "CSWAP",
            "CY", "CH", "CCZ", "RX", "RY", "RZ", "P", "CRX", "CRY", "CRZ", "CP",
            "RXX", "RYY", "RZZ", "SQSWAP", "U", "UX", "US", "CU", "CUH", "I", "MCX"} <= set(APRESENTACAO)
    # toda porta é apresentada numa fase que existe, e cada fase apresenta no máximo uma
    ids = {f.id for f in FASES}
    assert set(APRESENTACAO.values()) <= ids
    assert len(set(APRESENTACAO.values())) == len(APRESENTACAO)


def test_portas_conjugadas_desfazem_as_originais():
    for a, b in [("S", "SDG"), ("T", "TDG")]:
        assert np.allclose(PORTAS[a].matriz @ PORTAS[b].matriz, np.eye(2))
    unit = lambda *nomes: Circuito(1, [(n, (0,)) for n in nomes]).unitaria()
    assert np.allclose(unit("TDG", "TDG"), PORTAS["SDG"].matriz)          # T†·T† = S†
    assert np.allclose(unit("S", "S", "S"), PORTAS["SDG"].matriz)          # S† = S³
    assert np.allclose(1j * PORTAS["X"].matriz @ PORTAS["Z"].matriz, PORTAS["Y"].matriz)   # Y = iXZ


def test_raiz_de_x():
    sx = PORTAS["SX"].matriz
    assert np.allclose(sx @ sx, PORTAS["X"].matriz)                      # √X·√X = X
    hsh = Circuito(1, [("H", (0,)), ("S", (0,)), ("H", (0,))]).unitaria()
    assert abs(np.vdot(hsh.ravel(), sx.ravel())) / 2 == pytest.approx(1)   # H·S·H = √X (fase global)
    assert np.allclose(Estado.zeros(1).aplicar(PORTAS["SX"], [0]).bloch(0), [0, -1, 0])


def test_familia_da_troca():
    swap, iswap, cswap = (PORTAS[n].matriz for n in ("SWAP", "ISWAP", "CSWAP"))
    tres_cnots = Circuito(2, [("CNOT", (0, 1)), ("CNOT", (1, 0)), ("CNOT", (0, 1))]).unitaria()
    assert np.allclose(tres_cnots, swap)                                          # 3 CNOTs = SWAP
    assert np.allclose(swap @ swap, np.eye(4))
    zz = np.kron(PORTAS["Z"].matriz, PORTAS["Z"].matriz)
    assert np.allclose(iswap @ iswap, zz)                                         # iSWAP² = Z⊗Z
    ss = np.kron(PORTAS["S"].matriz, PORTAS["S"].matriz)
    assert np.allclose(ss @ swap @ PORTAS["CZ"].matriz, iswap)                    # iSWAP = SWAP+CZ+S⊗S
    # |+⟩|0⟩ → |0⟩|+i⟩
    e = Estado([1, 0, 1, 0]).aplicar(PORTAS["ISWAP"], [0, 1])
    assert np.allclose(e.bloch(0), [0, 0, 1]) and np.allclose(e.bloch(1), [0, 1, 0])
    # Fredkin: só troca com o controle em 1, e mantém o número de 1s
    assert Estado.da_base("101").aplicar(PORTAS["CSWAP"], [0, 1, 2]).probabilidade("110") == pytest.approx(1)
    assert Estado.da_base("001").aplicar(PORTAS["CSWAP"], [0, 1, 2]).probabilidade("001") == pytest.approx(1)
    assert np.allclose(cswap @ cswap, np.eye(8))


def test_controladas():
    from qubit_lab.core.portas import controlada
    assert np.allclose(controlada(PORTAS["X"].matriz), PORTAS["CNOT"].matriz)
    assert np.allclose(controlada(PORTAS["X"].matriz, 2), PORTAS["TOFFOLI"].matriz)
    unit = lambda passos: Circuito(max(max(a) for _, a in passos) + 1, passos).unitaria()
    # S† no alvo, CNOT, S no alvo = CY
    cy = unit([("SDG", (1,)), ("CNOT", (0, 1)), ("S", (1,))])
    assert np.allclose(cy, PORTAS["CY"].matriz)
    # H no alvo, CCZ, H no alvo = Toffoli
    tof = unit([("H", (2,)), ("CCZ", (0, 1, 2)), ("H", (2,))])
    assert np.allclose(tof, PORTAS["TOFFOLI"].matriz)
    # CH com o controle em |+⟩: 50%, 25%, 25%
    e = Estado([1, 0, 1, 0]).aplicar(PORTAS["CH"], [0, 1])
    assert np.allclose(e.probabilidades(), [0.5, 0, 0.25, 0.25])
    # CCZ é simétrica: tanto faz a ordem dos qubits
    ccz = PORTAS["CCZ"].matriz
    assert np.allclose(unit([("CCZ", (2, 0, 1))]), ccz)


def _igual_a_menos_de_fase(a, b):
    return abs(np.vdot(a.ravel(), b.ravel())) / len(a) == pytest.approx(1)


def test_rotacoes():
    m = {n: PORTAS[n].matriz for n in PORTAS}
    I2, I4 = np.eye(2), np.eye(4)
    pot = np.linalg.matrix_power
    # Rx
    assert _igual_a_menos_de_fase(m["RX"], m["SX"])
    assert _igual_a_menos_de_fase(pot(m["RX"], 2), m["X"])
    assert np.allclose(pot(m["RX"], 4), -I2)                       # volta inteira = −I
    # Ry
    assert np.allclose(m["RY"] @ m["Z"], m["H"])                     # Z, depois Ry = H
    assert _igual_a_menos_de_fase(pot(m["RY"], 2), m["Y"])
    assert np.allclose(m["RY"].imag, 0)
    assert np.allclose(pot(m["RY"], 4), -I2)
    # Rz e P
    assert _igual_a_menos_de_fase(m["RZ"], m["S"]) and not np.allclose(m["RZ"], m["S"])
    assert np.allclose(m["H"] @ m["RZ"] @ m["H"], m["RX"])
    assert np.allclose(pot(m["RZ"], 4), -I2)
    assert np.allclose(m["P"], m["S"]) and np.allclose(pot(m["P"], 2), m["Z"])
    assert np.allclose(m["RZ"], np.exp(-1j * np.pi / 4) * m["P"])


def test_rotacoes_controladas():
    m = {n: PORTAS[n].matriz for n in PORTAS}
    pot = np.linalg.matrix_power
    no_controle = lambda u: np.kron(u, np.eye(2))
    assert np.allclose(pot(m["CP"], 2), m["CZ"])
    assert np.allclose(m["CP"], no_controle(m["T"]) @ m["CRZ"])     # CRz e depois T no controle = CP
    assert not _igual_a_menos_de_fase(m["CP"], m["CRZ"])              # controladas, não são iguais
    assert np.allclose(pot(m["CRX"], 2), no_controle(m["SDG"]) @ m["CNOT"])
    for n in ("CRX", "CRY", "CRZ"):
        assert np.allclose(pot(m[n], 4), no_controle(m["Z"]))       # quatro = Z no controle
    # CRy e CH: iguais com o alvo em |0⟩, diferentes com o alvo em |1⟩
    for k, igual in (("10", True), ("11", False)):
        a = Estado.da_base(k).aplicar(PORTAS["CRY"], [0, 1]).vetor
        b = Estado.da_base(k).aplicar(PORTAS["CH"], [0, 1]).vetor
        assert np.allclose(a, b) == igual
    assert np.allclose(m["CRY"].imag, 0)
    # CP é simétrica
    assert np.allclose(Circuito(2, [("CP", (1, 0))]).unitaria(), m["CP"])


def test_outras_portas_relacoes():
    from qubit_lab.core.portas import ising, rx, rz, u3
    m = {n: PORTAS[n].matriz for n in PORTAS}
    k = np.kron
    unit = lambda passos, n=2: Circuito(n, passos).unitaria()
    # I
    for a, b in [("X", "X"), ("H", "H"), ("S", "SDG")]:
        assert np.allclose(m[a] @ m[b], m["I"])
    assert np.allclose(rx(2 * np.pi), -m["I"])
    # U
    assert np.allclose(m["U"], m["H"]) and np.allclose(u3(np.pi, 0, np.pi), m["X"])
    for lam in (0.3, np.pi / 4, 2.0):
        assert np.allclose(u3(0, 0, lam), np.diag([1, np.exp(1j * lam)]))       # U(0,0,λ) = P(λ)
    for theta in (0.4, np.pi / 2, 2.5):
        assert np.allclose(u3(theta, -np.pi / 2, np.pi / 2), rx(theta))         # U(θ,−π/2,π/2) = Rx(θ)
    # CU
    assert np.allclose(m["CU"], m["CNOT"])
    from qubit_lab.core.portas import controlada
    assert np.allclose(controlada(u3(np.pi / 2, 0, np.pi)), m["CH"])
    # Ising
    X, Y, Z, H = m["X"], m["Y"], m["Z"], m["H"]
    bell = lambda fase: np.array([1, 0, 0, fase]) / np.sqrt(2)
    assert np.allclose(m["RXX"] @ [1, 0, 0, 0], bell(-1j))
    assert np.allclose(m["RYY"] @ [1, 0, 0, 0], bell(1j))
    for nome, pauli in (("RXX", X), ("RYY", Y), ("RZZ", Z)):
        assert np.allclose(ising(pauli, np.pi), -1j * k(pauli, pauli))
    assert np.allclose(k(H, H) @ m["RZZ"] @ k(H, H), m["RXX"])
    assert np.allclose(m["RXX"] @ m["RYY"], m["ISWAP"].conj().T)               # Rxx·Ryy = iSWAP†
    for a in ("RXX", "RYY", "RZZ"):
        for b in ("RXX", "RYY", "RZZ"):
            assert np.allclose(m[a] @ m[b], m[b] @ m[a])                      # comutam
    for theta in (0.7, np.pi / 2):
        cnot_rz = m["CNOT"] @ k(m["I"], rz(theta)) @ m["CNOT"]
        assert np.allclose(cnot_rz, ising(Z, theta))                          # CNOT, Rz, CNOT = Rzz
    assert np.allclose(np.abs(np.diag(m["RZZ"])), 1) and np.allclose(m["RZZ"], np.diag(np.diag(m["RZZ"])))
    # √SWAP
    assert np.allclose(m["SQSWAP"] @ m["SQSWAP"], m["SWAP"])
    assert np.allclose(np.linalg.matrix_power(m["SQSWAP"], 3), m["SQSWAP"].conj().T)   # três = √SWAP†
    assert np.allclose(m["SWAP"] @ m["SQSWAP"] @ m["SQSWAP"], np.eye(4))
    for ket, igual in (("01", True), ("10", True), ("00", False)):           # igual à Rxx só às vezes
        a = Estado.da_base(ket).aplicar(PORTAS["SQSWAP"], [0, 1])
        b = Estado.da_base(ket).aplicar(PORTAS["RXX"], [0, 1])
        assert (a.fidelidade(b) == pytest.approx(1)) == igual
    cz = unit([("SQSWAP", (0, 1)), ("Z", (0,)), ("SQSWAP", (0, 1)), ("S", (0,)), ("SDG", (1,))])
    assert _igual_a_menos_de_fase(cz, m["CZ"])
    # MCX
    assert np.allclose(m["MCX"] @ m["MCX"], np.eye(16))
    hz = unit([("H", (3,)), ("MCX", (0, 1, 2, 3)), ("H", (3,))], 4)
    assert np.allclose(hz, np.diag([1] * 15 + [-1]))                          # Z multicontrolada
    assert Estado.da_base("1110").aplicar(PORTAS["MCX"], [0, 1, 2, 3]).probabilidade("1111") == pytest.approx(1)


def test_portas_u_disfarcadas():
    from qubit_lab.core.portas import controlada, u3
    m = {n: PORTAS[n].matriz for n in PORTAS}
    assert np.allclose(m["U"], m["H"]) and np.allclose(m["UX"], m["X"]) and np.allclose(m["US"], m["S"])
    assert np.allclose(m["CU"], m["CNOT"]) and np.allclose(m["CUH"], m["CH"])
    assert np.allclose(u3(np.pi, np.pi / 2, np.pi / 2), m["Y"])
    assert np.allclose(controlada(u3(np.pi, np.pi / 2, np.pi / 2)), m["CY"])
    assert np.allclose(u3(0, 0, np.pi / 4), m["T"]) and np.allclose(u3(0, 0, np.pi), m["Z"])
    assert np.allclose(u3(0, 0, 0), m["I"])
    assert np.allclose(m["CUH"] @ m["CUH"], np.eye(4))


def test_fase_completo_exige_todos_os_slots():
    fase = next(f for f in FASES if f.id == 68)
    assert fase.completo
    assert not fase.venceu({})                       # vazio já está no alvo, mas não vale
    assert fase.venceu({1: "I"})
    assert not fase.venceu({1: "H"})
    assert resolver(fase).solucoes == [{1: "I"}]
    assert problemas(fase) == []


def test_formulas_escritas_a_mao_batem_com_o_alvo():
    """A `formula` só muda o texto; o vetor do alvo tem que ser o mesmo estado que ela descreve."""
    f73 = next(f for f in FASES if f.id == 73)
    esperado = np.ones(16); esperado[-1] = -1                     # (|0000⟩ + … + |1110⟩ − |1111⟩)/4
    assert f73.objetivo.alvo.fidelidade(Estado(esperado)) == pytest.approx(1)
    f74 = next(f for f in FASES if f.id == 74)
    controles = np.ones(8); controles[-1] = -1                     # (|000⟩ + … − |111⟩)/√8
    menos = np.array([1, -1])                                      # ⊗ |−⟩
    assert f74.objetivo.alvo.fidelidade(Estado(np.kron(controles, menos))) == pytest.approx(1)
    for f in FASES:                                                # só estados longos usam fórmula
        if f.objetivo.formula:
            assert f.n_qubits >= 4, f.id


def test_algoritmos():
    # a QFT do jogo (H, CP, H, SWAP) é a transformada de Fourier discreta
    qft = Circuito(2, [("H", (0,)), ("CP", (1, 0)), ("H", (1,)), ("SWAP", (0, 1))]).unitaria()
    assert np.allclose(qft, np.array([[1j ** (j * k) for k in range(4)] for j in range(4)]) / 2)
    # troca de emaranhamento (fase 92): Bell nos qubits 0 e 3, com 1 e 2 em |+⟩
    v = np.zeros(16)
    for a in (0, 1):
        for b in (0, 1):
            for c in (0, 1):
                v[a * 8 + b * 4 + c * 2 + a] = 1
    f92 = next(f for f in FASES if f.id == 92)
    assert f92.objetivo.alvo.fidelidade(Estado(v)) == pytest.approx(1)
    # codificação superdensa: nada, X, Z, XZ → 00, 01, 10, 11
    for portas, bits in [([], "00"), (["X"], "01"), (["Z"], "10"), (["X", "Z"], "11")]:
        c = Circuito(2, [("H", (0,)), ("CNOT", (0, 1))] + [(p, (0,)) for p in portas]
                     + [("CNOT", (0, 1)), ("H", (0,))])
        assert c.executar().probabilidade(bits) == pytest.approx(1)


def test_orcamento_de_portas():
    f = next(f for f in FASES if f.id == 94)
    assert f.max_portas == 2
    assert f.venceu({7: "Z", 8: "S"})                      # duas portas: dentro do orçamento
    assert not f.venceu({6: "S", 7: "S", 8: "S"})          # três S chegam ao alvo, mas estouram
    assert f.objetivo.cumprido(f.resultado({6: "S", 7: "S", 8: "S"}))
    assert f.estourou_orcamento({6: "S", 7: "S", 8: "S"})


def test_correcao_de_erro():
    """Fases 99 e 100: o qubit 0 volta ao estado original, mesmo com o erro no meio."""
    for fid in (99, 100):
        f = next(f for f in FASES if f.id == fid)
        s = resolver(f)
        assert f.venceu(s.melhor)
        assert "TOFFOLI" in s.melhor.values()               # a correção usa a Toffoli
        sem_correcao = {k: v for k, v in s.melhor.items() if v != "TOFFOLI"}
        assert not f.venceu(sem_correcao)                   # sem a Toffoli, o erro fica


def test_simbolos_de_exibicao():
    from qubit_lab.core.portas import simbolo
    assert simbolo("SDG") == "S†" and simbolo("TDG") == "T†" and simbolo("H") == "H"
    assert simbolo("SX") == "√X" and simbolo("ISWAP") == "iSWAP" and simbolo("CSWAP") == "CSWAP"
    from qubit_lab.core.portas import partes
    assert simbolo("RX") == "Rx(π/2)" and simbolo("CP") == "CP(π/2)"
    assert partes("CRY") == ("CRy", "π/2") and partes("H") == ("H", None)


def test_validador_pega_fase_ruim():
    ruim = Fase.de_dict({
        "id": 1, "qubits": 1,
        "circuito": [{"slot": True, "alvos": [0]}],
        "disponiveis": ["H"],                         # H só é apresentada na fase 2
        "objetivo": {"tipo": "probabilidade", "ket": "0"},   # já começa vencida
    })
    erros = problemas(ruim)
    assert any("antes de ela ser apresentada" in e for e in erros)
