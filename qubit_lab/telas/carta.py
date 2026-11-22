"""Carta de porta nova: aparece antes da fase que apresenta uma porta."""

from __future__ import annotations

import numpy as np
import pygame

from ..core import Circuito, Estado, formatar
from ..core.capitulos import APRESENTACAO
from ..core.portas import porta as buscar_porta
from ..core.portas import partes, simbolo
from ..textos import carta
from ..ui import estilo as E
from ..ui.bloch import desenhar_esfera
from ..ui.simbolos import desenhar_multi, largura_rotulo, rotulo
from ..ui.widgets import Botao
from .base import Cabecalho, Tela


def _entrada(z: complex) -> str:
    for valor, txt in [(0, "0"), (1, "1"), (-1, "−1"), (1j, "i"), (-1j, "−i")]:
        if abs(z - valor) < 1e-9:
            return txt
    if abs(abs(z) - 1) < 1e-9:
        k = round(np.angle(z) / (np.pi / 4))
        return {1: "e^(iπ/4)", 2: "i", 3: "e^(3iπ/4)", -1: "e^(−iπ/4)", -3: "e^(−3iπ/4)"}.get(k, f"{z:.2g}")
    if abs(abs(z.real) - 0.5) < 1e-9 and abs(abs(z.imag) - 0.5) < 1e-9:   # √SWAP: (1 ± i)/2
        return f"{'−' if z.real < 0 else ''}(1{'+' if z.imag > 0 else '−'}i)/2"
    if abs(abs(z) - 1 / np.sqrt(2)) < 1e-9:          # CH, CRx: ±1/√2 ou ±i/√2 sem fator comum
        u = _entrada(z * np.sqrt(2))
        return {"1": "1/√2", "−1": "−1/√2", "i": "i/√2", "−i": "−i/√2"}.get(u, f"{z:.2g}")
    return f"{z.real:.2g}"


def formatar_matriz(m: np.ndarray):
    """Devolve (fator, linhas): H → ("1/√2", [["1", "1"], ["1", "−1"]])."""
    # √X e parecidas: todas as entradas da forma (±1 ± i)/2
    if np.allclose(np.abs(m.real), 0.5) and np.allclose(np.abs(m.imag), 0.5):
        meio = lambda z: f"{'−' if z.real < 0 else ''}1{'+' if z.imag > 0 else '−'}i"
        return "1/2", [[meio(z) for z in linha] for linha in m]
    mods = np.abs(m[np.abs(m) > 1e-9])
    fator = ""
    if np.allclose(mods, mods[0]) and abs(mods[0] - 1 / np.sqrt(2)) < 1e-9:
        fator, m = "1/√2", m * np.sqrt(2)
    return fator, [[_entrada(z) for z in linha] for linha in m]


def larguras_colunas(linhas, tam, minima):
    """Largura de cada coluna da matriz: a padrão, ou mais, se a coluna tiver uma entrada comprida."""
    f = E.fonte(tam, True)
    return [max(minima, max(f.size(linha[j])[0] for linha in linhas) + 12) for j in range(len(linhas[0]))]


def tamanho_matriz(linhas, tam, minima, livre):
    """Fonte e larguras das colunas; a fonte diminui até a matriz caber em `livre` pixels."""
    while True:
        cols = larguras_colunas(linhas, tam, minima)
        if sum(cols) + 10 <= livre or tam <= 9:
            return tam, cols
        tam -= 1
        minima = int(minima * 0.92)


def x_colunas(x0, cols):
    """O centro de cada coluna, a partir da borda esquerda da matriz."""
    centros, x = [], x0 + 10
    for c in cols:
        centros.append(x + c // 2)
        x += c
    return centros


def desenhar_simbolo(tela, nome, centro, tamanho=110):
    """O símbolo da porta como aparece no circuito."""
    x, y = centro
    p = buscar_porta(nome)
    if p.n_qubits == 1:
        tam = int(tamanho * (0.42 if partes(nome)[1] else 0.55))
        # rótulo comprido (U com três ângulos): a caixa alarga em vez de deixar o texto vazar
        r = pygame.Rect(0, 0, max(tamanho, largura_rotulo(nome, tam) + tamanho // 5), tamanho)
        r.center = centro
        E.painel(tela, r, E.PAINEL_CLARO, E.OURO, raio=14, largura_borda=2)
        rotulo(tela, nome, centro, tam, E.OURO)
        return
    # portas de vários qubits: um fio por qubit, de cima para baixo (mesmo desenho da bancada)
    ys = fios_simbolo(p.n_qubits, y, tamanho)
    desenhar_multi(tela, nome, x, ys, E.OURO, escala=max(0.75, min(1.1, tamanho / 100)))


def kets_que_mudam(p):
    """As entradas da base que a porta altera (na Toffoli: 110 e 111; na Fredkin: 101 e 110)."""
    kets = [format(i, f"0{p.n_qubits}b") for i in range(2 ** p.n_qubits)]
    return [k for k in kets
            if not np.allclose(Estado.da_base(k).aplicar(p, range(p.n_qubits)).vetor, Estado.da_base(k).vetor)]


def fios_simbolo(n, centro_y, tamanho=110):
    """Alturas dos fios no desenho da carta."""
    if n == 1:
        return [centro_y]
    return [int(centro_y - tamanho // 2 + i * tamanho / (n - 1)) for i in range(n)]


def demo_da_porta(nome: str, quadros: int = 60):
    """Animação da porta agindo num estado em que o efeito dela aparece na esfera."""
    n = buscar_porta(nome).n_qubits
    if nome in ("Z", "S", "T", "SDG", "TDG", "RZ", "P", "US"):
        inicial = Estado([1, 1])                          # gira no equador: precisa sair do polo
    elif nome == "I":
        inicial = Estado([np.cos(0.6), np.sin(0.6) * np.exp(0.9j)])   # um estado qualquer: nada se mexe
    elif nome in ("RXX", "RYY"):
        inicial = Estado.zeros(2)                         # |00⟩ vira um estado de Bell
    elif nome == "SQSWAP":
        inicial = Estado.da_base("10")                    # meia troca: os dois ficam emaranhados
    elif nome == "MCX":
        inicial = Estado([0] * 6 + [1] + [0] * 7 + [1, 0])   # |+110⟩: o alvo segue o qubit 0
    elif nome in ("CZ", "CP", "CRZ", "RZZ"):
        inicial = Estado([1, 1, 1, 1])                    # |++⟩: só a fase muda
    elif nome == "CCZ":
        inicial = Estado([1] * 8)                         # |+++⟩
    elif n == 2:
        inicial = Estado([1, 0, 1, 0])                    # |+0⟩
    elif n == 3:
        inicial = Estado([0, 0, 1, 0, 0, 0, 1, 0])        # |+10⟩
    else:
        inicial = Estado.zeros(n)
    return Circuito(n).adicionar(nome, list(range(n))).animar(quadros, inicial=inicial)


def quadro_em_loop(demo, t: float):
    """Ciclo de 3 s: 0,5 s parado, 1,5 s girando, 1 s parado no fim."""
    u = min(1.0, max(0.0, ((t % 3.0) - 0.5) / 1.5))
    return demo[int(u * (len(demo) - 1))]


class Carta(Tela):
    def __init__(self, app, nome_porta: str, id_fase: int | None = None, colapso=None, voltar=None):
        """id_fase: a fase que vem depois da carta. Sem fase (álbum), `voltar` é a tela de retorno."""
        super().__init__(app)
        self.colapso = colapso
        self.voltar = voltar
        self.nome = nome_porta
        self.id_fase = id_fase
        self.porta = buscar_porta(nome_porta)
        self.textos = carta(nome_porta)
        self.cab = Cabecalho(app, f"fase {id_fase}" if id_fase else "álbum de portas",
                             "Nova porta" if id_fase else self.porta.titulo)
        n = self.porta.n_qubits
        self.kets = [format(i, f"0{n}b") for i in range(2 ** n)]
        # entradas do "Experimente": os kets da base e uma superposição
        # (com 4 qubits, 16 botões não cabem: só alguns kets que mostram a porta trabalhando)
        base = self.kets if n < 4 else ["0000", "0110", "1110", "1111"]
        self.entradas = [(f"|{k}⟩", Estado.da_base(k)) for k in base]
        if n == 1:
            self.entradas.append(("|+⟩", Estado([1, 1])))
        elif nome_porta in ("CZ", "CP", "CRZ", "RZZ"):
            self.entradas.append(("|++⟩", Estado([1, 1, 1, 1])))
        elif nome_porta == "CCZ":
            self.entradas.append(("|+++⟩", Estado([1] * 8)))
        elif n == 2:
            self.entradas.append(("|+0⟩", Estado([1, 0, 1, 0])))
        elif n == 3:
            self.entradas.append(("|+10⟩", Estado([0, 0, 1, 0, 0, 0, 1, 0])))
        elif n == 4:
            self.entradas.append(("|+110⟩", Estado([0] * 6 + [1] + [0] * 7 + [1, 0])))
        self.entrada = 0
        larg = {1: 64, 2: 72, 3: 62}.get(n, 84)
        self.b_kets = [Botao((0, 0, larg, 44), rot) for rot, _ in self.entradas]

        self.demo = demo_da_porta(nome_porta)
        self.t_demo = 0.0
        self.b_ouvir = Botao((1050, 318, 52, 52), "▶", "primario")
        if id_fase is None:
            rotulo = "Voltar ao álbum"
        elif voltar is not None:
            rotulo = "Voltar para a bancada"
        else:
            rotulo = "Entendi, para a bancada"
        self.b_continuar = Botao((958, 640, 250, 52), rotulo, "primario")
        ordem = sorted(APRESENTACAO, key=APRESENTACAO.get)
        self.numero = ordem.index(nome_porta) + 1 if nome_porta in ordem else 0
        self.total = len(ordem)

    def _continuar(self):
        from .bancada import Bancada
        if self.id_fase is not None:
            self.app.progresso.ver_porta(self.nome)
        if self.voltar is not None:              # aberta pelo álbum ou pelo "?" da bancada
            self.app.ir(self.voltar)
            return
        self.app.ir(Bancada(self.app, self.id_fase, colapso=self.colapso))

    def _ouvir(self):
        self.t_demo = 0.0
        self.app.audio.tocar_estado([self.demo[0]] * 20 + self.demo + [self.demo[-1]] * 20, fps=60)

    def atualizar(self, dt):
        self.t_demo = (self.t_demo + dt) % 3.0

    def _quadro_demo(self):
        """Ciclo de 3 s: 0,5 s parado, 1,5 s girando, 1 s parado no fim."""
        u = min(1.0, max(0.0, (self.t_demo - 0.5) / 1.5))
        return self.demo[int(u * (len(self.demo) - 1))]

    def evento(self, e):
        if self.cab.evento(e):
            return
        if e.type == pygame.KEYDOWN:
            if e.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                self._continuar()
            elif e.key == pygame.K_ESCAPE:
                if self.voltar is not None:
                    self.app.ir(self.voltar)
                else:
                    from .menu import Menu
                    self.app.ir(Menu(self.app))
            elif pygame.K_0 <= e.key <= pygame.K_9 and e.key - pygame.K_0 < len(self.entradas):
                self.entrada = e.key - pygame.K_0
            elif e.key == pygame.K_SPACE:
                self._ouvir()
        if self.b_continuar.clicou(e):
            self._continuar()
        elif self.b_ouvir.clicou(e):
            self._ouvir()
        for i, b in enumerate(self.b_kets):
            if b.clicou(e):
                self.entrada = i

    def desenhar(self, tela):
        self.cab.desenhar(tela)
        p = self.porta

        # --- a carta ---------------------------------------------------
        c = pygame.Rect(72, 92, 400, 600)
        E.painel(tela, c, E.PAINEL, E.OURO, raio=18, largura_borda=2)
        E.texto(tela, "NOVA PORTA" if self.id_fase else "CARTA DO ÁLBUM", (c.x + 24, c.y + 22), 12, E.OURO,
                negrito=True)
        E.texto(tela, f"nº {self.numero:02d} / {self.total:02d}", (c.right - 24, c.y + 22), 12,
                E.TEXTO_MEDIO, mono=True, ancora="topright")
        area = pygame.Rect(c.x + 24, c.y + 52, c.width - 48, 190)
        E.painel(tela, area, E.FUNDO_FUNDO, E.BORDA)
        for yy in fios_simbolo(p.n_qubits, area.centery):
            pygame.draw.line(tela, E.COBRE, (area.x, yy), (area.right, yy), 3)
        desenhar_simbolo(tela, self.nome, area.center)

        E.texto(tela, p.titulo, (c.x + 24, c.y + 262), 30, E.TEXTO, negrito=True)
        E.texto(tela, self.textos["subtitulo"], (c.x + 24, c.y + 304), 16, E.GELO)

        if p.n_qubits >= 4:                     # 16 × 16 não cabe na carta: descreve em palavras
            self._desenhar_kets_e_matriz_grande(tela, c, p)
            self._desenhar_explicacoes(tela)
            return
        fator, linhas = formatar_matriz(p.matriz)
        rot_matriz = f"{partes(self.nome)[0]} ="
        livre = c.width - 48 - E.fonte(16, True).size(rot_matriz)[0] - 14 - (52 if fator else 0) - 10
        tam, cols = tamanho_matriz(linhas, {1: 18, 2: 14, 3: 11}[p.n_qubits],
                                       {1: 46, 2: 34, 3: 25}[p.n_qubits], livre)
        altura = len(linhas) * (tam + 8)
        y_m = c.y + 352                         # topo da matriz
        y_meio = y_m + altura // 2 - 2
        x0 = c.x + 24
        E.texto(tela, rot_matriz, (x0, y_meio), 16, E.TEXTO, mono=True, ancora="midleft")
        x0 += E.fonte(16, True).size(rot_matriz)[0] + 14
        if fator:
            E.texto(tela, fator, (x0, y_meio), 16, E.TEXTO, mono=True, ancora="midleft")
            x0 += 52
        pygame.draw.line(tela, E.TEXTO_MEDIO, (x0, y_m - 4), (x0, y_m + altura), 2)
        direita = x0 + sum(cols) + 10
        centros = x_colunas(x0, cols)
        pygame.draw.line(tela, E.TEXTO_MEDIO, (direita, y_m - 4), (direita, y_m + altura), 2)
        for i, linha in enumerate(linhas):
            for j, entrada in enumerate(linha):
                cor = E.AMBAR if entrada.startswith("−") else E.TEXTO
                E.texto(tela, entrada, (centros[j], y_m + i * (tam + 8)),
                        tam, cor, mono=True, ancora="midtop")

        y = y_m + altura + 22
        mostrar = self.kets if p.n_qubits < 3 else kets_que_mudam(p)
        for k in mostrar:
            saida = Estado.da_base(k).aplicar(p, range(p.n_qubits))
            E.texto(tela, f"{simbolo(self.nome)}|{k}⟩ = {formatar(saida.vetor, manter_fase=True)}", (c.x + 24, y), 14,
                    E.TEXTO_SUAVE, mono=True)
            y += 24

        self._desenhar_explicacoes(tela)

    def _desenhar_kets_e_matriz_grande(self, tela, c, p):
        n = 2 ** p.n_qubits
        E.texto_quebrado(tela, f"A matriz é {n} × {n}: a identidade, menos no canto de baixo, onde fica "
                         f"um X.", pygame.Rect(c.x + 24, c.y + 346, c.width - 48, 50), 14, E.TEXTO_MEDIO)
        y = c.y + 404
        for k in kets_que_mudam(p):
            saida = Estado.da_base(k).aplicar(p, range(p.n_qubits))
            E.texto(tela, f"{simbolo(self.nome)}|{k}⟩ = {formatar(saida.vetor, manter_fase=True)}",
                    (c.x + 24, y), 14, E.TEXTO_SUAVE, mono=True)
            y += 24
        E.texto(tela, f"as outras {n - len(kets_que_mudam(p))} entradas não mudam", (c.x + 24, y + 4), 13,
                E.TEXTO_MEDIO)

    def _desenhar_explicacoes(self, tela):
        # --- explicações ------------------------------------------------
        p = self.porta
        x = 500
        r = pygame.Rect(x, 92, 708, 120)
        E.painel(tela, r, E.FUNDO_FUNDO, E.BORDA)
        E.rotulo_secao(tela, "Analogia", (r.x + 20, r.y + 16), E.OURO)
        E.texto_quebrado(tela, self.textos["analogia"], pygame.Rect(r.x + 20, r.y + 40, r.width - 40, 80), 15)

        r = pygame.Rect(x, 228, 520, 160)
        E.painel(tela, r, E.FUNDO_FUNDO, E.BORDA)
        E.rotulo_secao(tela, "Na esfera de Bloch", (r.x + 20, r.y + 16), E.OURO)
        q = self._quadro_demo()
        if p.n_qubits == 1:
            desenhar_esfera(tela, (r.x + 90, r.y + 92), 52, q.bloch(0), rotulos=True)
            x_txt = r.x + 170
        else:
            n = p.n_qubits
            raio, passo = (40, 96) if n == 2 else (30, 70)
            for i in range(n):
                cx = r.x + 52 + i * passo
                desenhar_esfera(tela, (cx, r.y + 92), raio, q.bloch(i), rotulos=False)
                E.texto(tela, f"qubit {i}", (cx, r.y + 142), 11, E.TEXTO_MEDIO, mono=True, ancora="center")
            x_txt = r.x + 52 + (n - 1) * passo + raio + 30
        E.texto_quebrado(tela, self.textos["esfera"], pygame.Rect(x_txt, r.y + 44, r.right - x_txt - 20, 110), 14)

        r = pygame.Rect(x + 536, 228, 172, 160)
        E.painel(tela, r, E.FUNDO_FUNDO, E.BORDA)
        E.rotulo_secao(tela, "Ouça", (r.x + 18, r.y + 16), E.OURO)
        self.b_ouvir.rect.topleft = (r.x + 18, r.y + 44)
        self.b_ouvir.desenhar(tela)
        E.texto_quebrado(tela, "Espaço também toca", pygame.Rect(r.x + 18, r.y + 108, 140, 40), 13,
                         E.TEXTO_MEDIO)

        r = pygame.Rect(x, 404, 708, 210)
        E.painel(tela, r, E.FUNDO_FUNDO, E.BORDA)
        E.rotulo_secao(tela, "Experimente", (r.x + 20, r.y + 16), E.OURO)
        E.texto(tela, f"Escolha a entrada (ou tecle 0 a {len(self.entradas) - 1}):", (r.x + 20, r.y + 44), 14,
                E.TEXTO_SUAVE)
        for i, b in enumerate(self.b_kets):
            b.rect.topleft = (r.x + 20 + i * (b.rect.width + 8), r.y + 76)
            b.estilo = "normal"
            b.desenhar(tela)
            if i == self.entrada:
                pygame.draw.rect(tela, E.GELO, b.rect, 2, border_radius=10)
        rotulo, entrada = self.entradas[self.entrada]
        saida = entrada.aplicar(p, range(p.n_qubits))
        y_s = r.y + 150
        E.texto(tela, f"{simbolo(self.nome)}{rotulo}  =  {formatar(saida.vetor, manter_fase=True)}",
                (r.x + 20, y_s), 20, E.TEXTO, mono=True, ancora="midleft")
        probs = saida.probabilidades()
        textos_prob = [f"P({k}) = {pr:.0%}" for k, pr in zip(self.kets, probs) if pr > 1e-9]
        E.texto(tela, "   ".join(textos_prob), (r.x + 20, y_s + 32), 14, E.TEXTO_MEDIO, mono=True,
                ancora="midleft")

        self.b_continuar.desenhar(tela)
