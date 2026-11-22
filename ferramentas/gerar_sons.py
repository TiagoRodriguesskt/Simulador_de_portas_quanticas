"""
Qubit Lab — gerador de sons "de física".

A ideia: o som é o próprio estado quântico.
- Cada estado da base tem uma nota: |0> = Lá (220 Hz), |1> = Mi (330 Hz, a quinta).
- O sinal de áudio é  s(t) = Σ_k Re( a_k(t) · W_k(t) ),  onde a_k são as amplitudes
  do qubit e W_k é a "voz" (onda complexa) do estado |k>.
  Como a potência do som é proporcional a |a_k|², o volume de cada nota segue a
  probabilidade de medir aquele estado.
- As portas são animadas como rotações contínuas na esfera de Bloch, então
  a interferência acontece "de verdade" no áudio.
- A fase relativa entre |0> e |1> vira posição no estéreo e brilho do timbre.

Uso (na raiz do projeto):  python ferramentas/gerar_sons.py
"""

import os
import wave

import numpy as np

SR = 44100                     # taxa de amostragem (amostras por segundo)
F0, F1 = 220.0, 330.0          # notas de |0> e |1>
# os .wav vão para assets/sons, ao lado da raiz do projeto
PASTA = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "sons")
rng = np.random.default_rng(7)

# ---------------------------------------------------------------- portas ---
I2 = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)

# Cada porta = rotação de 180° em torno de um eixo da esfera de Bloch.
EIXOS = { # type: ignore
    "X": np.array([1, 0, 0.0]),
    "Z": np.array([0, 0, 1.0]),
    "H": np.array([1, 0, 1.0]) / np.sqrt(2),
}


def rotacao(eixo, theta):
    """U(θ) = cos(θ/2)·I − i·sin(θ/2)·(n·σ), vetorizado em θ."""
    n_sigma = eixo[0] * X + eixo[1] * Y + eixo[2] * Z # type: ignore
    c = np.cos(theta / 2)[:, None, None] # type: ignore
    s = np.sin(theta / 2)[:, None, None] # type: ignore
    return c * I2 - 1j * s * n_sigma


def suave(x):
    """Curva 'smoothstep': começa e termina devagar, sem trancos."""
    return x * x * (3 - 2 * x)


def trajetoria(psi0, passos):
    """Gera as amplitudes a_k(t) amostra por amostra.

    passos: lista de ("espera", seg) ou ("porta", nome, seg) ou ("medir", k).
    """
    psi = np.array(psi0, dtype=complex)
    blocos = []
    for p in passos:
        if p[0] == "espera":
            n = int(p[1] * SR)
            blocos.append(np.tile(psi, (n, 1)))
        elif p[0] == "porta":
            _, nome, dur = p
            n = int(dur * SR)
            theta = np.pi * suave(np.linspace(0, 1, n))
            U = rotacao(EIXOS[nome], theta)
            traj = U @ psi
            blocos.append(traj)
            psi = traj[-1]
        elif p[0] == "medir":
            # colapso: o estado vira |k>, com uma transição de 30 ms
            k = p[1]
            alvo = np.zeros(2, dtype=complex)
            alvo[k] = psi[k] / abs(psi[k])          # mantém a fase da componente
            n = int(0.03 * SR)
            w = suave(np.linspace(0, 1, n))[:, None]
            blocos.append((1 - w) * psi + w * alvo)
            psi = alvo
    return np.concatenate(blocos)


# ----------------------------------------------------------------- vozes ---
def voz(f, t, brilho=0.0):
    """Onda complexa de uma nota com timbre 'cristal frio'.

    Todas as parciais recebem a MESMA fase vinda da amplitude, então uma
    amplitude negativa inverte a onda inteira e pode cancelar outra igual.
    """
    w = np.exp(2j * np.pi * f * t)
    w += 0.45 * np.exp(2j * np.pi * (f + 0.7) * t)        # leve chorus
    w += 0.45 * np.exp(2j * np.pi * (f - 0.7) * t)
    w += 0.18 * np.exp(2j * np.pi * 2 * f * t)
    brilho_total = 0.04 + 0.35 * brilho
    trem = 0.6 + 0.4 * np.sin(2 * np.pi * 5.5 * t)        # cintilância
    w += brilho_total * trem * np.exp(2j * np.pi * 4 * f * t)
    w += 0.5 * brilho_total * np.exp(2j * np.pi * 6.01 * f * t)
    return w / 2.4


def sintetizar_1qubit(amp):
    """Transforma a trajetória a_k(t) de 1 qubit em áudio estéreo."""
    n = len(amp)
    t = np.arange(n) / SR
    a0, a1 = amp[:, 0], amp[:, 1]

    # fase relativa φ = arg(a1) − arg(a0); onde |a0| ~ 0 mantemos o último valor
    phi = np.angle(a1 * np.conj(a0))
    confiavel = (np.abs(a0) > 0.08) & (np.abs(a1) > 0.08)
    if not confiavel[0]:
        phi[0] = 0.0
        confiavel[0] = True
    idx = np.where(confiavel, np.arange(n), 0)
    np.maximum.accumulate(idx, out=idx)       # repete o último valor confiável
    phi = phi[idx]

    brilho = (1 - np.cos(phi)) / 2            # φ = π  -> timbre mais "gelado"
    pan = 0.7 * np.sin(phi)                   # φ = ±π/2 -> lados do fone

    s0 = np.real(a0 * voz(F0, t))
    s1 = np.real(a1 * voz(F1, t, brilho))

    gl = np.sqrt((1 - pan) / 2)               # pan de potência constante
    gr = np.sqrt((1 + pan) / 2)
    esq = s0 * np.sqrt(0.5) + s1 * gl
    dir_ = s0 * np.sqrt(0.5) + s1 * gr
    return np.stack([esq, dir_], axis=1)


# --------------------------------------------------------------- efeitos ---
def reverb(x, tempo=2.2, mix=0.28):
    """Reverb por convolução com ruído decaindo (sala fria e grande)."""
    n = int(tempo * SR)
    t = np.arange(n) / SR
    env = np.exp(-6.9 * t / tempo)
    saida = np.zeros((x.shape[0] + n - 1, 2))
    for c in range(2):
        ir = rng.standard_normal(n) * env
        ir[0] = 0
        ir /= np.sqrt(np.sum(ir ** 2))
        m = 1 << int(np.ceil(np.log2(x.shape[0] + n)))
        molhado = np.fft.irfft(np.fft.rfft(x[:, c], m) * np.fft.rfft(ir, m), m)
        saida[:, c] = molhado[: saida.shape[0]] * mix
    saida[: x.shape[0]] += x * (1 - mix)
    return saida


def envelope(x, entrada=0.25, saida=0.6):
    n = len(x)
    e = np.ones(n)
    a, r = int(entrada * SR), int(saida * SR)
    e[:a] = suave(np.linspace(0, 1, a))
    e[n - r:] = suave(np.linspace(1, 0, r))
    return x * e[:, None]


def silencio(seg):
    return np.zeros((int(seg * SR), 2))


def vidro_quebrando(dur=1.2):
    """Colapso: estilhaços de vidro (senos agudos curtos) + sopro de ruído."""
    n = int(dur * SR)
    t = np.arange(n) / SR
    s = np.zeros((n, 2))
    for _ in range(38):
        f = rng.uniform(2200, 7500)
        t0 = rng.exponential(0.05)
        d = rng.uniform(0.04, 0.35)
        tt = np.clip(t - t0, 0, None)
        g = np.where(t >= t0, np.exp(-tt / d), 0) * rng.uniform(0.2, 1.0)
        onda = np.sin(2 * np.pi * f * tt) * g
        p = rng.uniform(-0.9, 0.9)
        s[:, 0] += onda * np.sqrt((1 - p) / 2)
        s[:, 1] += onda * np.sqrt((1 + p) / 2)
    ruido = rng.standard_normal((n, 2))
    ruido = np.diff(ruido, axis=0, prepend=0)       # passa-altas simples
    s += ruido * np.exp(-t / 0.07)[:, None] * 0.6
    return s / np.max(np.abs(s)) * 0.55


def sino(f, dur=2.5):
    """Sino de vidro com parciais inarmônicas (para a vitória)."""
    t = np.arange(int(dur * SR)) / SR
    razoes = [1, 2.76, 5.40, 8.93]
    s = sum(np.sin(2 * np.pi * f * r * t) * np.exp(-t * (1.2 + 1.5 * i)) / (i + 1)
            for i, r in enumerate(razoes))
    return s


def salvar(nome, x, alvo_db=-1.0):
    x = x / (np.max(np.abs(x)) + 1e-12) * 10 ** (alvo_db / 20)
    dados = (x * 32767).astype("<i2")
    os.makedirs(PASTA, exist_ok=True)
    caminho = os.path.join(PASTA, nome)
    with wave.open(caminho, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(dados.tobytes())
    print(f"  {caminho}  ({len(x) / SR:.1f} s)")


# ---------------------------------------------------------------- cenas ---
KET0, KET1 = [1, 0], [0, 1]


def cena(psi0, passos):
    return reverb(envelope(sintetizar_1qubit(trajetoria(psi0, passos))))


def gerar_todos():
    print("Gerando sons do Qubit Lab:")

    # 1 e 2: as notas da base
    salvar("01_estado_0.wav", cena(KET0, [("espera", 2.5)]))
    salvar("02_estado_1.wav", cena(KET1, [("espera", 2.5)]))

    # 3: Hadamard — de uma nota para o acorde da superposição
    salvar("03_hadamard_superposicao.wav",
           cena(KET0, [("espera", 1.2), ("porta", "H", 1.0), ("espera", 2.5)]))

    # 4: interferência — H e H de novo: o Mi aparece e se cancela sozinho
    salvar("04_interferencia_HH.wav",
           cena(KET0, [("espera", 1.0), ("porta", "H", 1.0), ("espera", 1.5),
                       ("porta", "H", 1.0), ("espera", 2.0)]))

    # 5: a fase — H, Z, H. O Z quase não muda as notas (só o brilho e o estéreo),
    #    mas a última H revela a diferença: agora sobra o Mi, não o Lá.
    salvar("05_fase_Z_revelada.wav",
           cena(KET0, [("espera", 1.0), ("porta", "H", 1.0), ("espera", 1.0),
                       ("porta", "Z", 1.5), ("espera", 1.0),
                       ("porta", "H", 1.0), ("espera", 2.0)]))

    # 6: colapso — superposição, medição, vidro quebrando, sobra uma nota
    psi_mais = np.array([1, 1]) / np.sqrt(2)
    antes = sintetizar_1qubit(trajetoria(psi_mais, [("espera", 2.0)])) # type: ignore
    depois = sintetizar_1qubit(trajetoria(KET1, [("espera", 2.5)])) # type: ignore
    corte = int(0.04 * SR)
    seq = np.concatenate([antes, depois]) # type: ignore
    seq = envelope(seq)
    seq[len(antes) - corte: len(antes) + corte] *= np.concatenate( # type: ignore
        [np.linspace(1, 0.2, corte), np.linspace(0.2, 1, corte)])[:, None]
    seq[len(antes) + corte:] *= 0.8 # type: ignore
    vidro = vidro_quebrando()
    ini = len(antes) - int(0.01 * SR) # pyright: ignore[reportUnknownArgumentType]
    seq[ini: ini + len(vidro)] += vidro
    salvar("06_colapso.wav", reverb(seq, mix=0.35))

    # 7: emaranhamento — 2 qubits. Qubit A: Lá/Mi; qubit B: uma oitava acima.
    #    |00> -> H em A -> (|00>+|10>)/√2 -> CNOT -> (|00>+|11>)/√2
    #    No estado de Bell as duas vozes pulsam juntas, no mesmo ritmo.
    t = np.arange(int(7.5 * SR)) / SR
    def nota2(a, b):
        return (voz([F0, F1][a], t) + voz(2 * [F0, F1][b], t) * 0.7) # type: ignore
    tH0, tH1, tC0, tC1 = 1.0, 2.0, 3.5, 4.5
    h = suave(np.clip((t - tH0) / (tH1 - tH0), 0, 1))
    c = suave(np.clip((t - tC0) / (tC1 - tC0), 0, 1))
    amp00 = np.cos(h * np.pi / 4)
    amp10 = np.sin(h * np.pi / 4) * np.cos(c * np.pi / 2)
    amp11 = np.sin(h * np.pi / 4) * np.sin(c * np.pi / 2)
    pulso = 1 - 0.45 * c * (0.5 - 0.5 * np.cos(2 * np.pi * 2.0 * t))
    s = np.real(amp00 * nota2(0, 0) + amp10 * nota2(1, 0) + amp11 * nota2(1, 1)) * pulso
    estereo = np.stack([s, s], axis=1)
    salvar("07_emaranhamento.wav", reverb(envelope(estereo)))

    # 8: detector acende — arpejo de quintas em sinos de vidro + brilho
    dur = 4.0
    n = int(dur * SR)
    out = np.zeros((n, 2))
    notas = [F0 * 2, F1 * 2, F0 * 4, F1 * 4]
    for i, f in enumerate(notas):
        ini = int(i * 0.12 * SR)
        b = sino(f, dur - i * 0.12)[: n - ini] # type: ignore
        p = -0.6 + 0.4 * i
        out[ini:, 0] += b * np.sqrt((1 - p) / 2)
        out[ini:, 1] += b * np.sqrt((1 + p) / 2)
    t = np.arange(n) / SR
    brilho = rng.standard_normal((n, 2))
    brilho = np.diff(brilho, axis=0, prepend=0) * np.exp(-((t - 0.5) ** 2) / 0.08)[:, None]
    out += brilho * 0.15
    salvar("08_detector_acende.wav", reverb(out, tempo=3.0, mix=0.35))

    # 9: ambiente do criostato (loop de 10 s, sem emenda)
    #    zumbido da rede (60 Hz) + "suspiro" ritmado do pulse-tube (1,4 Hz)
    dur = 10.0
    n = int(dur * SR)
    t = np.arange(n) / SR
    zumbido = 0.25 * np.sin(2 * np.pi * 60 * t) + 0.1 * np.sin(2 * np.pi * 120 * t)
    ruido = rng.standard_normal((n, 2))
    espectro = np.fft.rfft(ruido, axis=0)       # filtragem circular -> loop perfeito
    freqs = np.fft.rfftfreq(n, 1 / SR)
    grave = np.exp(-((freqs - 180) / 120) ** 2)
    agudo = np.exp(-((freqs - 6000) / 2500) ** 2)
    ruido_grave = np.fft.irfft(espectro * grave[:, None], n, axis=0)
    ruido_agudo = np.fft.irfft(espectro * agudo[:, None], n, axis=0)
    ruido_grave /= np.max(np.abs(ruido_grave))
    ruido_agudo /= np.max(np.abs(ruido_agudo))
    chuff = (0.5 - 0.5 * np.cos(2 * np.pi * 1.4 * t)) ** 6
    amb = (ruido_grave * chuff[:, None] * 0.9
           + ruido_agudo * 0.05
           + zumbido[:, None] * 0.5)
    salvar("09_ambiente_criostato.wav", amb, alvo_db=-6.0)


if __name__ == "__main__":
    gerar_todos()
