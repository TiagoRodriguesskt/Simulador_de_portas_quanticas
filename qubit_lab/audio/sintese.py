"""Som em tempo real: transforma a animação de um circuito em áudio.

É o mesmo princípio de ferramentas/gerar_sons.py, agora para qualquer
circuito do jogo:  s(t) = Σₖ Re( aₖ(t) · Wₖ(t) )
onde aₖ são as amplitudes do estado e Wₖ é o acorde do ket |k⟩.

Notas de cada qubit (o qubit 0 é o mais grave):
    qubit 0:  |0⟩ = Lá 220 Hz   |1⟩ = Mi 330 Hz
    qubit 1:  uma oitava acima  (440 / 660 Hz)
    qubit 2:  duas oitavas acima (880 / 1320 Hz)
"""

from __future__ import annotations

from functools import lru_cache

import numpy as np

NOTAS = (220.0, 330.0)
PESO_QUBIT = (1.0, 0.7, 0.5)


def frequencia(qubit: int, bit: int) -> float:
    return NOTAS[bit] * (2 ** qubit)


def voz(f: float, t: np.ndarray, brilho=0.0) -> np.ndarray:
    """Onda complexa com timbre de "cristal frio".

    Todas as parciais recebem a mesma fase vinda da amplitude: uma amplitude
    negativa inverte a onda inteira, e duas ondas opostas se cancelam.
    """
    w = np.exp(2j * np.pi * f * t)
    w += 0.45 * np.exp(2j * np.pi * (f + 0.7) * t)
    w += 0.45 * np.exp(2j * np.pi * (f - 0.7) * t)
    w += 0.18 * np.exp(2j * np.pi * 2 * f * t)
    b = 0.04 + 0.35 * np.asarray(brilho)
    w += b * (0.6 + 0.4 * np.sin(2 * np.pi * 5.5 * t)) * np.exp(2j * np.pi * 4 * f * t)
    return w / 2.4


def acorde(bits: str, t: np.ndarray) -> np.ndarray:
    """A "voz" de um ket da base: uma nota por qubit, somadas."""
    w = np.zeros_like(t, dtype=complex)
    for q, b in enumerate(bits):
        w += PESO_QUBIT[min(q, 2)] * voz(frequencia(q, int(b)), t)
    return w / sum(PESO_QUBIT[: len(bits)])


@lru_cache(maxsize=4)
def _resposta_reverb(sr: int, tempo: float = 1.6):
    rng = np.random.default_rng(3)
    n = int(tempo * sr)
    env = np.exp(-6.9 * np.arange(n) / sr / tempo)
    irs = []
    for _ in range(2):
        ir = rng.standard_normal(n) * env
        ir[0] = 0
        irs.append(ir / np.sqrt(np.sum(ir ** 2)))
    return irs


def reverb(x: np.ndarray, sr: int, mix: float = 0.25) -> np.ndarray:
    irs = _resposta_reverb(sr)
    n = len(irs[0])
    saida = np.zeros((x.shape[0] + n - 1, 2))
    m = 1 << int(np.ceil(np.log2(saida.shape[0])))
    for c in range(2):
        molhado = np.fft.irfft(np.fft.rfft(x[:, c], m) * np.fft.rfft(irs[c], m), m)
        saida[:, c] = molhado[: saida.shape[0]] * mix
    saida[: x.shape[0]] += x * (1 - mix)
    return saida


def sintetizar(quadros, fps: float, sr: int = 44100, cauda: float = 0.8) -> np.ndarray:
    """Gera o áudio (float, estéreo, entre −1 e 1) de uma lista de estados.

    quadros: estados da animação (Circuito.animar), um a cada 1/fps segundos.
    cauda:   segundos extras segurando o estado final antes de sumir.
    """
    amps = np.array([q.vetor for q in quadros])            # (n_quadros, 2^n)
    n_qubits = quadros[0].n_qubits
    dur = len(quadros) / fps + cauda
    t = np.arange(int(dur * sr)) / sr
    t_quadros = np.arange(len(quadros)) / fps
    # amplitude de cada ket, amostra por amostra (interpolação linear)
    a = np.stack([np.interp(t, t_quadros, amps[:, k].real) + 1j * np.interp(t, t_quadros, amps[:, k].imag)
                  for k in range(amps.shape[1])], axis=1)

    if n_qubits == 1:
        # um qubit: a fase relativa vira posição no estéreo e brilho do timbre
        a0, a1 = a[:, 0], a[:, 1]
        phi = np.angle(a1 * np.conj(a0))
        confiavel = (np.abs(a0) > 0.08) & (np.abs(a1) > 0.08)
        if not confiavel[0]:
            phi[0], confiavel[0] = 0.0, True
        idx = np.where(confiavel, np.arange(len(t)), 0)
        np.maximum.accumulate(idx, out=idx)
        phi = phi[idx]
        s0 = np.real(a0 * voz(NOTAS[0], t))
        s1 = np.real(a1 * voz(NOTAS[1], t, (1 - np.cos(phi)) / 2))
        pan = 0.7 * np.sin(phi)
        esq = s0 * np.sqrt(0.5) + s1 * np.sqrt((1 - pan) / 2)
        dir_ = s0 * np.sqrt(0.5) + s1 * np.sqrt((1 + pan) / 2)
        x = np.stack([esq, dir_], axis=1)
    else:
        s = np.zeros_like(t)
        for k in range(amps.shape[1]):
            if np.max(np.abs(a[:, k])) > 1e-4:
                s += np.real(a[:, k] * acorde(format(k, f"0{n_qubits}b"), t))
        x = np.stack([s, s], axis=1)

    # entrada e saída suaves
    n_in, n_out = int(0.06 * sr), int(min(0.6, cauda) * sr)
    env = np.ones(len(t))
    env[:n_in] = np.linspace(0, 1, n_in)
    env[-n_out:] = np.linspace(1, 0, n_out)
    x = reverb(x * env[:, None], sr)
    pico = np.max(np.abs(x))
    return x / pico * 0.6 if pico > 0 else x


def para_int16(x: np.ndarray) -> np.ndarray:
    return np.ascontiguousarray((np.clip(x, -1, 1) * 32767).astype(np.int16))
