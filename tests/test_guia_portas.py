"""Testes do guia de estudo (docs/estudo_portas): conferem cada conta citada no guia.

Rode só estes com:  pytest tests/test_guia_portas.py -v
"""
import sys
from pathlib import Path

import numpy as np

# o arquivo das portas fica em docs/estudo_portas, fora do pacote do jogo
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "docs" / "estudo_portas"))
from portas_conferir import (  # noqa: E402
    CCZ, CNOT, CNOT_invertida, CP, CRz, CY, CZ, H, I, P, S, SWAP, SX, T, TOFFOLI,
    U, X, Y, Z, Rx, Rxx, Ry, Ryy, Rz, Rzz, bloch, emaranhado, iSWAP, ket0,
    ket1, mesma_a_menos_de_fase, plus, sqrtSWAP,
)


# ------------------------------------------------------------ 1 qubit ---
def test_x_vira_0_em_1():
    assert np.allclose(X @ ket0, ket1)


def test_h_leva_0_para_mais_x():
    assert np.allclose(bloch(H @ ket0), [1, 0, 0])


def test_h_vezes_h_e_identidade():
    assert np.allclose(H @ H, I)


def test_hzh_e_x():
    assert np.allclose(H @ Z @ H, X)


def test_h_e_ry_depois_de_z():
    assert np.allclose(Ry(np.pi / 2) @ Z, H)


def test_s_vezes_s_e_z():
    assert np.allclose(S @ S, Z)


def test_t_vezes_t_e_s():
    assert np.allclose(T @ T, S)


def test_raiz_de_x_leva_0_para_menos_y():
    assert np.allclose(bloch(SX @ ket0), [0, -1, 0])


def test_raiz_de_x_ao_quadrado_e_x():
    assert np.allclose(SX @ SX, X)


def test_p_e_rz_diferem_so_por_fase_global():
    assert mesma_a_menos_de_fase(P(0.9), Rz(0.9))


def test_u_vira_x_y_e_h():
    assert np.allclose(U(np.pi, 0, np.pi), X)
    assert np.allclose(U(np.pi, np.pi / 2, np.pi / 2), Y)
    assert np.allclose(U(np.pi / 2, 0, np.pi), H)


def test_rx_de_360_graus_e_menos_identidade():
    """O espinor: girar 2π dá -I, e só 4π volta a I."""
    assert np.allclose(Rx(2 * np.pi), -I)
    assert np.allclose(Rx(4 * np.pi), I)


# ----------------------------------------------------------- 2 qubits ---
def test_estado_de_bell():
    bell = CNOT @ np.kron(H, I) @ np.kron(ket0, ket0)
    assert np.allclose(bell, np.array([1, 0, 0, 1]) / np.sqrt(2))
    assert emaranhado(bell)


def test_cz_emaranha_mais_mais():
    assert emaranhado(CZ @ np.kron(plus, plus))


def test_mais_mais_nao_esta_emaranhado():
    assert not emaranhado(np.kron(plus, plus))


def test_cnot_vem_da_cz_com_hadamards():
    assert np.allclose(np.kron(I, H) @ CZ @ np.kron(I, H), CNOT)


def test_cy_vem_da_cnot_com_s():
    assert np.allclose(np.kron(I, S) @ CNOT @ np.kron(I, S.conj().T), CY)


def test_swap_e_tres_cnots():
    assert np.allclose(CNOT @ CNOT_invertida @ CNOT, SWAP)


def test_iswap_emaranha_mais_mais():
    assert emaranhado(iSWAP @ np.kron(plus, plus))


def test_raiz_de_swap_ao_quadrado_e_swap():
    assert np.allclose(sqrtSWAP @ sqrtSWAP, SWAP)


def test_cp_e_crz_com_fase_no_controle():
    assert np.allclose(np.kron(P(0.45), I) @ CRz(0.9), CP(0.9))


def test_rxx_cria_estado_tipo_bell():
    esperado = np.array([1, 0, 0, -1j]) / np.sqrt(2)
    assert np.allclose(Rxx(np.pi / 2) @ np.kron(ket0, ket0), esperado)


def test_rxx_e_ryy_formam_iswap_adaga():
    assert np.allclose(Rxx(np.pi / 2) @ Ryy(np.pi / 2), iSWAP.conj().T)


def test_rzz_com_duas_cnots():
    assert np.allclose(CNOT @ np.kron(I, Rz(0.7)) @ CNOT, Rzz(0.7))


# ----------------------------------------------------------- 3 qubits ---
def test_toffoli_e_um_and():
    k110 = np.zeros(8)
    k110[0b110] = 1
    assert np.argmax(abs(TOFFOLI @ k110)) == 0b111


def test_toffoli_vem_da_ccz_com_hadamards():
    HHH = np.kron(np.eye(4), H)
    assert np.allclose(HHH @ CCZ @ HHH, TOFFOLI)
