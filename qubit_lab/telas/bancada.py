"""A bancada: a tela onde a fase é jogada.

Fluxo:
1. O jogador escolhe uma porta na bandeja (clique ou teclas 1–9) e clica num slot.
2. "Ativar" (ou Enter) roda o circuito: a esfera de Bloch gira porta a porta,
   um pulso de energia percorre os fios e o som do estado toca junto.
3. No fim, o detector mostra a chance de acender. Com 100%, a fase é vencida.

No Modo Colapso (qubit_lab/colapso.py) a mesma tela esconde o estado sob o
gelo, conta vidas e permite espiar uma vez por fase.
"""

from __future__ import annotations

import math

import numpy as np
import pygame

from ..core import Estado, formatar
from ..core.circuito import Passo
from ..core.fase import Slot
from ..core.portas import porta as buscar_porta
from ..core.portas import partes, simbolo
from ..core.solver import opcoes_do_slot, resolver
from ..ui import estilo as E
from ..ui.bloch import desenhar_esfera
from ..ui.simbolos import desenhar_multi, largura_relativa, rotulo
from ..colapso import inicio_do_capitulo
from ..ui.widgets import Botao
from .base import Cabecalho, Tela

FPS_ANIMACAO = 60
QUADROS_POR_PORTA = 48            # 0,8 s girando em cada porta
QUADROS_VIAGEM = 18               # 0,3 s do pulso viajando entre as portas

PAINEL_ESQ = pygame.Rect(32, 88, 300, 548)
OBJETIVO = pygame.Rect(356, 88, 672, 52)
CIRCUITO = pygame.Rect(356, 156, 672, 380)
BANDEJA_Y = 556
PAINEL_DIR = pygame.Rect(1052, 88, 196, 548)
X_FIO_INICIO, X_FIO_FIM = 412, 1000


class Bancada(Tela):
    def __init__(self, app, id_fase: int, colapso=None):
        super().__init__(app)
        self.fase = app.nova_fase(id_fase)
        self.solucao = resolver(self.fase)
        self.colapso = colapso                 # SessaoColapso ou None (modo normal)
        self.espiou = False
        self.fim_de_jogo = False
        sobre = f"modo colapso · fase {self.fase.id}" if colapso else f"fase {self.fase.id} de {app.total_fases}"
        # no Modo Colapso não há explicação nem dicas: é a prova
        self.cab = Cabecalho(app, sobre, self.fase.titulo, ajuda=None if colapso else self.abrir_explicacao,
                             glossario=None if colapso else self.abrir_glossario)
        self.selecionada: str | None = None
        self.modo = "edicao"           # "edicao" → "animando" → "resultado"
        self.quadros = [Estado.zeros(self.fase.n_qubits)]
        self.indice = 0.0
        self.rastros = [[] for _ in range(self.fase.n_qubits)]
        self.venceu = False
        self.mensagem = ""
        self.pulso_x = []

        n = self.fase.n_qubits
        espaco = CIRCUITO.height - 120
        self.y_fios = [CIRCUITO.centery] if n == 1 else [
            int(CIRCUITO.y + 50 + i * espaco / (n - 1)) for i in range(n)]
        # Colunas: portas em qubits diferentes podem dividir a mesma coluna
        # (como nos diagramas de circuito). Cada passo vai para a primeira
        # coluna livre depois do último passo que usou os mesmos fios.
        ultima = [-1] * n
        colunas = []
        for p in self.fase.passos:
            fios = range(min(p.alvos), max(p.alvos) + 1)
            col = max(ultima[q] for q in fios) + 1
            for q in fios:
                ultima[q] = col
            colunas.append(col)
        n_col = max(colunas) + 1
        x_ini, x_fim = 480, 920
        passo_x = (x_fim - x_ini) / (n_col - 1) if n_col > 1 else 0
        self.tam = int(min(72, passo_x - 12)) if n_col > 1 else 72
        self.x_passos = [int((x_ini + x_fim) / 2) if n_col == 1 else int(x_ini + c * passo_x) for c in colunas]

        # Bandeja: as portas cabem entre o rótulo e o botão Ativar (até 7 portas)
        self.b_ativar = Botao((CIRCUITO.right - 128, BANDEJA_Y + 8, 128, 48), "Ativar", "primario")
        # Cartas com ângulo, como Rx(π/2), e de vários qubits (CNOT, SWAP...) são mais largas.
        x_ini, x_fim, folga = 440, self.b_ativar.rect.x - 16, 8
        fatores = [largura_relativa(nome) for nome in self.fase.disponiveis]
        espaco = x_fim - x_ini - folga * (len(fatores) - 1)
        self.tam_cartao = int(min(64, espaco / max(1, sum(fatores))))
        self.cartoes = {}
        x = x_ini
        for nome, f in zip(self.fase.disponiveis, fatores):
            larg = int(self.tam_cartao * f)
            self.cartoes[nome] = pygame.Rect(x, BANDEJA_Y + (64 - self.tam_cartao) // 2, larg, self.tam_cartao)
            x += larg + folga
        # Reiniciar e Espiar ficam no painel do detector, longe da bandeja
        self.b_reiniciar = Botao((PAINEL_DIR.x + 16, PAINEL_DIR.bottom - 64, PAINEL_DIR.width - 32, 48),
                                 "Reiniciar (R)")
        self.b_espiar = Botao((PAINEL_DIR.x + 16, PAINEL_DIR.bottom - 124, PAINEL_DIR.width - 32, 48), "Espiar")
        self.b_proxima = Botao((0, 0, 220, 52), "Próxima fase", "primario")
        self.b_menu_fim = Botao((0, 0, 140, 52), "Menu")

    # ------------------------------------------------------------ geometria ---
    def rect_passo(self, i: int) -> pygame.Rect:
        p = self.fase.passos[i]
        ys = [self.y_fios[a] for a in p.alvos]
        topo, base = min(ys) - self.tam // 2, max(ys) + self.tam // 2
        return pygame.Rect(self.x_passos[i] - self.tam // 2, topo, self.tam, base - topo)

    @property
    def escondido(self) -> bool:
        """No Modo Colapso, o estado fica sob o gelo até o resultado."""
        return self.colapso is not None and self.modo in ("edicao", "animando")

    # --------------------------------------------------------------- ações ---
    def selecionar(self, nome: str):
        self.selecionada = None if self.selecionada == nome else nome

    def clicar_slot(self, i: int):
        """Coloca a porta selecionada no slot; sem seleção, esvazia o slot."""
        if self.modo == "animando" or self.fim_de_jogo:
            return
        if self.selecionada and self.selecionada in opcoes_do_slot(self.fase, i):
            self.fase.escolher(i, self.selecionada)
        elif i in self.fase.escolhas:
            self.fase.escolher(i, None)
        else:
            return
        self._voltar_para_edicao()

    def reiniciar(self):
        self.fase.escolhas.clear()
        self.selecionada = None
        self._voltar_para_edicao()

    def _voltar_para_edicao(self):
        self.modo = "edicao"
        self.venceu = False
        self.mensagem = ""
        self.quadros = [Estado.zeros(self.fase.n_qubits)]
        self.indice = 0.0
        self.rastros = [[] for _ in range(self.fase.n_qubits)]

    def abrir_explicacao(self):
        """Abre a explicação da fase; ao voltar, a bancada continua como estava."""
        if self.modo == "animando" or self.colapso:
            return
        self.app.ir(self.app.explicacao(self.fase.id, voltar=self))

    def abrir_glossario(self):
        """Abre o glossário; ao voltar, a bancada continua como estava."""
        if self.modo == "animando" or self.colapso:
            return
        from .glossario import Glossario
        self.app.ir(Glossario(self.app, voltar=self, selecionado=self.selecionada))

    def espiar(self):
        """Modo Colapso: mede o resultado do circuito UMA vez (e o estado colapsa)."""
        if self.colapso is None or self.espiou or self.modo == "animando" or self.fim_de_jogo:
            return
        estado = self.fase.resultado()
        rng = np.random.default_rng()
        bits = ""
        for q in range(self.fase.n_qubits):
            r, estado = estado.medir(q, rng)
            bits += str(r)
        self.espiou = True
        self.modo = "espiada"
        self.quadros, self.indice = [estado], 0.0
        self.rastros = [[] for _ in range(self.fase.n_qubits)]
        self.mensagem = f"Espiada: uma única medição deu |{bits}⟩. O estado colapsou!"
        self.app.audio.tocar("colapso")

    def ativar(self):
        if self.modo == "animando" or self.fim_de_jogo:
            return
        circuito = self.fase.circuito()
        base = circuito.animar(QUADROS_POR_PORTA)
        x_portas = [self.x_passos[i] for i, p in enumerate(self.fase.passos)
                    if isinstance(p, Passo) or i in self.fase.escolhas]
        # Linha do tempo: o pulso viaja até a porta (estado parado) e, chegando
        # lá, a porta age (a esfera gira). No fim, o pulso segue até o detector.
        pontos = [X_FIO_INICIO] + x_portas + [X_FIO_FIM]
        self.quadros, self.pulso_x = [], []
        for k in range(len(x_portas) + 1):
            parado = base[k * QUADROS_POR_PORTA]
            viagem = QUADROS_VIAGEM if pontos[k + 1] != pontos[k] else 0   # mesma coluna: sem viagem
            for j in range(1, viagem + 1):
                self.quadros.append(parado)
                self.pulso_x.append(pontos[k] + (pontos[k + 1] - pontos[k]) * j / viagem)
            if k < len(x_portas):
                for j in range(1, QUADROS_POR_PORTA + 1):
                    self.quadros.append(base[k * QUADROS_POR_PORTA + j])
                    self.pulso_x.append(pontos[k + 1])
        self.indice = 0.0
        self.rastros = [[] for _ in range(self.fase.n_qubits)]
        self.modo = "animando"
        self.mensagem = ""
        self.app.audio.tocar_estado(self.quadros, FPS_ANIMACAO)

    def _terminar_animacao(self):
        final = self.quadros[-1]
        faltam = self.fase.faltam_slots()
        estourou = self.fase.estourou_orcamento()
        self.venceu = self.fase.objetivo.cumprido(final) and not faltam and not estourou
        self.modo = "resultado"
        if self.venceu:
            if self.colapso:
                self.colapso.renovar()
                self.app.progresso.registrar_colapso(self.fase.id)
            else:
                self.app.progresso.concluir(self.fase.id)
            self.app.audio.tocar("detector")
            return
        chance = self.fase.objetivo.chance(final)
        if faltam and self.fase.objetivo.cumprido(final):
            self.mensagem = "O estado está certo, mas esta fase pede uma porta em cada slot."
        elif estourou and self.fase.objetivo.cumprido(final):
            self.mensagem = (f"O estado está certo, mas o orçamento é de {self.fase.max_portas} portas. "
                             "Existe um caminho mais curto.")
        elif self.fase.objetivo.tipo in ("probabilidade", "qubit"):
            self.mensagem = (f"O detector acenderia em {chance:.0%} das vezes. "
                             "Sorte não basta: busque 100%.")
        else:
            self.mensagem = (f"O estado final se parece {chance:.0%} com o alvo. "
                             "Ajuste as portas e tente de novo.")
        if self.colapso:
            self.app.audio.tocar("colapso")
            if not self.colapso.perder_vida():
                self.fim_de_jogo = True
            else:
                self.mensagem = f"Uma vida queimou ({chance:.0%}). O gelo quebrou: veja o que aconteceu."

    def _proxima(self):
        if self.fase.id < self.app.total_fases:
            if self.colapso:
                self.app.jogar_colapso(self.fase.id + 1, self.colapso)
            else:
                self.app.jogar(self.fase.id + 1)
        else:
            from .menu import Menu
            self.app.ir(Menu(self.app))

    def _recomecar_capitulo(self):
        from ..colapso import SessaoColapso
        self.app.jogar_colapso(inicio_do_capitulo(self.fase.id), SessaoColapso())

    # -------------------------------------------------------------- eventos ---
    def evento(self, e):
        if self.cab.evento(e):
            return
        venceu_tela = self.modo == "resultado" and self.venceu
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:
                from .menu import Menu
                self.app.ir(Menu(self.app))
            elif e.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                if venceu_tela:
                    self._proxima()
                elif self.fim_de_jogo:
                    self._recomecar_capitulo()
                else:
                    self.ativar()
            elif e.key == pygame.K_e:
                self.espiar()
            elif e.key == pygame.K_i:
                self.abrir_explicacao()
            elif e.key == pygame.K_g:
                self.abrir_glossario()
            elif e.key == pygame.K_r:
                self.reiniciar()
            elif pygame.K_1 <= e.key <= pygame.K_9:
                k = e.key - pygame.K_1
                if k < len(self.fase.disponiveis):
                    self.selecionar(self.fase.disponiveis[k])
            return

        if venceu_tela or self.fim_de_jogo:
            if self.b_proxima.clicou(e):
                if venceu_tela:
                    self._proxima()
                else:
                    self._recomecar_capitulo()
            elif self.b_menu_fim.clicou(e):
                from .menu import Menu
                self.app.ir(Menu(self.app))
            return

        if self.colapso and self.b_espiar.clicou(e):
            self.espiar()
        elif self.b_ativar.clicou(e):
            self.ativar()
        elif self.b_reiniciar.clicou(e):
            self.reiniciar()
        elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            for nome, r in self.cartoes.items():
                if r.collidepoint(e.pos):
                    self.selecionar(nome)
                    return
            for i in self.fase.slots:
                if self.rect_passo(i).collidepoint(e.pos):
                    self.clicar_slot(i)
                    return

    def atualizar(self, dt):
        if self.modo != "animando":
            return
        self.indice += dt * FPS_ANIMACAO
        i = min(int(self.indice), len(self.quadros) - 1)
        for q in range(self.fase.n_qubits):
            self.rastros[q].append(self.quadros[i].bloch(q))
            del self.rastros[q][:-60]
        if self.indice >= len(self.quadros) - 1:
            self._terminar_animacao()

    @property
    def estado_atual(self) -> Estado:
        return self.quadros[min(int(self.indice), len(self.quadros) - 1)]

    # ------------------------------------------------------------- desenho ---
    def desenhar(self, tela):
        self.cab.desenhar(tela)
        self._desenhar_esferas(tela)
        self._desenhar_objetivo(tela)
        self._desenhar_circuito(tela)
        self._desenhar_bandeja(tela)
        self._desenhar_detector(tela)
        self._desenhar_rodape(tela)
        if self.modo == "resultado" and self.venceu:
            self._desenhar_vitoria(tela)
        elif self.fim_de_jogo:
            self._desenhar_fim_de_jogo(tela)

    def _desenhar_esferas(self, tela):
        r = PAINEL_ESQ
        E.painel(tela, r)
        n = self.fase.n_qubits
        estado = self.estado_atual
        E.rotulo_secao(tela, "Esfera de Bloch" if n == 1 else "Esferas de Bloch", (r.x + 20, r.y + 18))
        gelo = self.escondido
        if n == 1:
            desenhar_esfera(tela, (r.centerx, r.y + 170), 100, estado.bloch(0), self.rastros[0], apagada=gelo)
            y = r.y + 300
        else:
            raio = 56
            # 2 qubits: esferas grandes; 3: médias; 4: pequenas, todas numa fileira
            raio_n, passo_n, x0_n = {2: (raio, 144, 78), 3: (40, 96, 54)}.get(n, (30, 72, 42))
            for q in range(n):
                cx = r.x + x0_n + q * passo_n
                desenhar_esfera(tela, (cx, r.y + 140), raio_n, estado.bloch(q),
                                self.rastros[q], rotulos=n == 2, apagada=gelo)
                E.texto(tela, f"qubit {q}" if n < 4 else f"q{q}", (cx, r.y + (222 if n < 4 else 192)), 12, E.TEXTO_MEDIO,
                        mono=True, ancora="center")
            if estado.esta_emaranhado() and not gelo:
                E.texto(tela, "emaranhados", (r.centerx, r.y + 246), 13, E.OURO, negrito=True, ancora="center")
            y = r.y + 272

        txt = "|ψ⟩ = ?" if gelo else f"|ψ⟩ = {formatar(estado.vetor)}"
        tam = 16
        while E.fonte(tam, True).size(txt)[0] > r.width - 30 and tam > 11:
            tam -= 1
        if E.fonte(tam, True).size(txt)[0] > r.width - 30:
            txt, tam = "|ψ⟩: veja as probabilidades abaixo", 13   # estado longo demais para ler
        E.texto(tela, txt, (r.centerx, y), tam, E.TEXTO, mono=True, ancora="midtop")

        y += 40
        probs = estado.probabilidades()
        if n >= 4:                               # 16 resultados: duas colunas de 8
            self._desenhar_probs_em_colunas(tela, r, y, probs, gelo)
            return
        for k, p in enumerate(probs):
            bits = format(k, f"0{n}b")
            cor = E.misturar(E.GELO, E.AMBAR, bits.count("1") / n)
            E.texto(tela, f"|{bits}⟩", (r.x + 20, y), 13, cor, mono=True)
            barra = pygame.Rect(r.x + 20 + 14 * n + 34, y + 4, r.width - 110 - 14 * n, 8)
            pygame.draw.rect(tela, E.FUNDO_FUNDO, barra, border_radius=4)
            if p > 1e-6 and not gelo:
                pygame.draw.rect(tela, cor, (barra.x, barra.y, max(2, int(barra.width * p)), 8),
                                 border_radius=4)
            E.texto(tela, "?" if gelo else f"{p:.0%}", (r.right - 20, y), 13, E.TEXTO, mono=True, ancora="topright")
            y += 26

    def _desenhar_probs_em_colunas(self, tela, r, y0, probs, gelo):
        n = self.fase.n_qubits
        larg_col = (r.width - 40) // 2
        metade = (len(probs) + 1) // 2
        for k, p in enumerate(probs):
            col, lin = divmod(k, metade)
            x, y = r.x + 20 + col * (larg_col + 4), y0 + lin * 26
            bits = format(k, f"0{n}b")
            cor = E.misturar(E.GELO, E.AMBAR, bits.count("1") / n)
            E.texto(tela, f"|{bits}⟩", (x, y), 11, cor, mono=True)
            barra = pygame.Rect(x + 52, y + 4, larg_col - 90, 7)
            pygame.draw.rect(tela, E.FUNDO_FUNDO, barra, border_radius=3)
            if p > 1e-6 and not gelo:
                pygame.draw.rect(tela, cor, (barra.x, barra.y, max(2, int(barra.width * p)), 7), border_radius=3)
            E.texto(tela, "?" if gelo else f"{p:.0%}", (x + larg_col - 2, y), 11, E.TEXTO, mono=True,
                    ancora="topright")

    def _desenhar_objetivo(self, tela):
        E.painel(tela, OBJETIVO)
        E.rotulo_secao(tela, "Objetivo", (OBJETIVO.x + 18, OBJETIVO.centery - 7), E.OURO)
        texto = self.fase.objetivo.descrever()
        livre = OBJETIVO.right - 18 - (OBJETIVO.x + 110) - (100 if self.colapso else 0)
        tam = 15
        while E.fonte(tam).size(texto)[0] > livre and tam > 11:
            tam -= 1                              # estados longos (fase 56) encolhem para caber
        E.texto(tela, texto, (OBJETIVO.x + 110, OBJETIVO.centery), tam, ancora="midleft")
        if self.colapso:
            # as três lâmpadas de vida
            for k in range(3):
                c = (OBJETIVO.right - 26 - (2 - k) * 30, OBJETIVO.centery)
                if k < self.colapso.vidas:
                    pygame.draw.circle(tela, E.AMBAR, c, 10)
                    pygame.draw.circle(tela, E.OURO_CLARO, c, 10, 2)
                else:
                    pygame.draw.circle(tela, E.FUNDO_FUNDO, c, 10)
                    pygame.draw.circle(tela, E.ALERTA, c, 10, 2)
                    pygame.draw.line(tela, E.ALERTA, (c[0] - 5, c[1] - 5), (c[0] + 5, c[1] + 5), 2)
                    pygame.draw.line(tela, E.ALERTA, (c[0] - 5, c[1] + 5), (c[0] + 5, c[1] - 5), 2)

    def _desenhar_circuito(self, tela):
        E.painel(tela, CIRCUITO, E.FUNDO_FUNDO)
        mouse = pygame.mouse.get_pos()

        for q, y in enumerate(self.y_fios):
            pygame.draw.line(tela, E.COBRE, (X_FIO_INICIO, y), (X_FIO_FIM, y), 3)
            caixa = pygame.Rect(0, 0, 54, 36)
            caixa.center = (CIRCUITO.x + 40, y)
            E.painel(tela, caixa, E.FUNDO_FUNDO, E.BORDA, raio=8)
            E.texto(tela, "|0⟩", caixa.center, 18, E.GELO, mono=True, ancora="center")
            # medidor no fim do fio
            pygame.draw.circle(tela, E.PAINEL, (X_FIO_FIM + 2, y), 22)
            pygame.draw.circle(tela, E.BORDA_CLARA, (X_FIO_FIM + 2, y), 22, 1)
            pygame.draw.arc(tela, E.TEXTO_SUAVE, (X_FIO_FIM - 10, y - 8, 24, 24), 0.3, math.pi - 0.3, 2)
            pygame.draw.line(tela, E.TEXTO_SUAVE, (X_FIO_FIM + 2, y + 6), (X_FIO_FIM + 9, y - 4), 2)

        if self.modo == "animando":
            self._desenhar_pulso(tela)          # antes das portas: elas ficam por cima

        t = self.app.t
        for i, passo in enumerate(self.fase.passos):
            r = self.rect_passo(i)
            if isinstance(passo, Slot):
                escolhida = self.fase.escolhas.get(i)
                cabe = self.selecionada in opcoes_do_slot(self.fase, i) if self.selecionada else False
                if escolhida:
                    self._porta_em(tela, escolhida, passo.alvos, i, borda=E.GELO)
                    if r.collidepoint(mouse) and self.modo != "animando":
                        E.texto(tela, "clique para tirar" if not cabe else "clique para trocar",
                                (r.centerx, r.bottom + 6), 11, E.TEXTO_MEDIO, ancora="midtop")
                else:
                    pygame.draw.rect(tela, E.FUNDO_FUNDO, r, border_radius=10)
                    brilho = 0.55 + 0.45 * math.sin(t * 5) if cabe else 0.0
                    cor = E.misturar(E.misturar(E.GELO, E.FUNDO_FUNDO, 0.35), E.GELO, brilho)
                    E.tracejado(tela, cor, r)
                    grande = self.tam >= 60
                    E.texto(tela, "+", (r.centerx, r.centery - (8 if grande else 0)), 24, cor, ancora="center")
                    if len(passo.alvos) > 1:
                        legenda = f"{len(passo.alvos)} qubits"
                    else:
                        legenda = "solte aqui" if cabe else "vazio"
                    if grande or len(passo.alvos) > 1:
                        E.texto(tela, legenda, (r.centerx, r.centery + 18), 10, cor, ancora="center")
            else:
                self._porta_em(tela, passo.porta, passo.alvos, i, borda=E.OURO)

        if self.modo == "animando":
            # a porta que está agindo agora ganha um brilho
            k = min(int(self.indice), len(self.pulso_x) - 1)
            parado = k > 0 and self.pulso_x[k] == self.pulso_x[k - 1]
            for i, x in enumerate(self.x_passos):
                if parado and x == self.pulso_x[k]:
                    brilho = self.rect_passo(i).inflate(12, 12)
                    pygame.draw.rect(tela, E.OURO_CLARO, brilho, 2, border_radius=14)

        if self.mensagem:
            E.texto(tela, self.mensagem, (CIRCUITO.centerx, CIRCUITO.bottom - 22), 14, E.AMBAR,
                    ancora="center")
        elif self.modo == "edicao":
            dica = ("Escolha uma porta na bandeja e clique num slot." if not self.selecionada
                    else f"Porta {self.selecionada} selecionada: clique num slot.")
            E.texto(tela, dica, (CIRCUITO.centerx, CIRCUITO.bottom - 22), 13, E.TEXTO_MEDIO, ancora="center")

    def _porta_em(self, tela, nome, alvos, i, borda):
        p = buscar_porta(nome)
        x = self.x_passos[i]
        if p.n_qubits == 1:
            r = pygame.Rect(0, 0, self.tam, self.tam)
            r.center = (x, self.y_fios[alvos[0]])
            E.painel(tela, r, E.PAINEL_CLARO, borda, raio=10, largura_borda=2)
            grande = self.tam >= 60
            if partes(nome)[1]:                   # com ângulo: "Rx" e, embaixo, "π/2"; sem o título
                rotulo(tela, nome, r.center, int(self.tam * 0.36), borda)
                return
            E.texto(tela, simbolo(nome), (r.centerx, r.centery - (6 if grande else 0)), int(self.tam * 0.4), borda,
                    mono=True, negrito=True, ancora="center")
            if grande:
                E.texto(tela, p.titulo, (r.centerx, r.bottom - 14), 10, E.TEXTO_SUAVE, ancora="center")
            return
        ys = [self.y_fios[a] for a in alvos]
        desenhar_multi(tela, nome, x, ys, borda)

    def _desenhar_pulso(self, tela):
        """Pulso de energia andando pelos fios, sincronizado com a animação."""
        x = self.pulso_x[min(int(self.indice), len(self.pulso_x) - 1)]
        halo = pygame.Surface((48, 48), pygame.SRCALPHA)
        pygame.draw.circle(halo, (*E.OURO, 60), (24, 24), 22)
        pygame.draw.circle(halo, (*E.OURO_CLARO, 140), (24, 24), 10)
        for y in self.y_fios:
            pygame.draw.line(tela, E.OURO, (X_FIO_INICIO, y), (x, y), 3)
            tela.blit(halo, (x - 24, y - 24))
            pygame.draw.circle(tela, (255, 240, 200), (int(x), y), 5)

    def _desenhar_bandeja(self, tela):
        E.rotulo_secao(tela, "Portas", (CIRCUITO.x, BANDEJA_Y + 26))
        for k, (nome, r) in enumerate(self.cartoes.items()):
            sel = nome == self.selecionada
            rr = r.move(0, -6) if sel else r
            E.painel(tela, rr, E.PAINEL_CLARO, E.GELO if sel else E.COBRE, raio=10, largura_borda=2 if sel else 1)
            grande = rr.height >= 60
            cor = E.GELO if sel else E.OURO
            if partes(nome)[1]:                   # com ângulo: duas linhas, sem o título embaixo
                base = partes(nome)[0]
                tam = 20 if len(base) <= 2 else 16
                if rr.height < 60:
                    tam -= 3
                rotulo(tela, nome, (rr.centerx, rr.centery + 2), tam, cor)
                E.texto(tela, str(k + 1), (rr.x + 6, rr.y + 4), 10, E.TEXTO_APAGADO, mono=True)
                continue
            rot = simbolo(nome)
            tam_nome = (22 if len(rot) <= 2 else 13) if grande else (20 if len(rot) <= 2 else 11)
            E.texto(tela, rot, (rr.centerx, rr.centery - (6 if grande else 0)), tam_nome,
                    cor, mono=True, negrito=True, ancora="center")
            if grande:
                titulo, tam_t = buscar_porta(nome).titulo, 9
                while E.fonte(tam_t).size(titulo)[0] > rr.width - 6 and tam_t > 7:
                    tam_t -= 1                    # "X multicontrolada" encolhe para caber na carta
                if E.fonte(tam_t).size(titulo)[0] > rr.width - 6:
                    titulo = ""                   # ainda não cabe: a carta fica só com o símbolo
                E.texto(tela, titulo, (rr.centerx, rr.bottom - 12), tam_t, E.TEXTO_SUAVE,
                        ancora="center")
            E.texto(tela, str(k + 1), (rr.x + 6, rr.y + 4), 10, E.TEXTO_APAGADO, mono=True)
        self.b_ativar.ativo = self.modo != "animando"
        self.b_ativar.desenhar(tela)

    def _desenhar_detector(self, tela):
        r = PAINEL_DIR
        E.painel(tela, r)
        E.rotulo_secao(tela, "Detector", (r.x + 18, r.y + 18))
        c = (r.centerx, r.y + 130)
        aceso = self.modo == "resultado" and self.venceu
        mostrar = self.modo in ("animando", "resultado") and not self.escondido
        chance = self.fase.objetivo.chance(self.estado_atual) if mostrar else 0.0
        if aceso:
            pulso = 0.5 + 0.5 * math.sin(self.app.t * 3)
            halo = pygame.Surface((200, 200), pygame.SRCALPHA)
            pygame.draw.circle(halo, (*E.OURO, int(40 + 30 * pulso)), (100, 100), 90)
            pygame.draw.circle(halo, (*E.OURO, 90), (100, 100), 60)
            tela.blit(halo, (c[0] - 100, c[1] - 100))
        pygame.draw.circle(tela, E.COBRE, c, 68, 1)
        pygame.draw.circle(tela, E.FUNDO_FUNDO if not aceso else E.OURO, c, 44)
        pygame.draw.circle(tela, E.BORDA_CLARA if not aceso else E.OURO_CLARO, c, 44, 2)
        if mostrar and not aceso:
            # o "brilho" interno acompanha a chance durante a animação
            pygame.draw.circle(tela, E.misturar(E.FUNDO_FUNDO, E.AMBAR, chance * 0.7), c, 30)
        alvo = self.fase.objetivo.ket_detector
        E.texto(tela, alvo, c, 18, E.ESCURO if aceso else E.AMBAR, mono=True, negrito=aceso, ancora="center")

        vazio = "?" if self.colapso else "—"
        E.texto(tela, f"{chance:.0%}" if mostrar else vazio, (c[0], r.y + 230), 30, E.TEXTO, mono=True,
                negrito=True, ancora="center")
        E.texto(tela, "chance de acender" if self.fase.objetivo.tipo in ("probabilidade", "qubit")
                else "parecido com o alvo",
                (c[0], r.y + 262), 12, E.TEXTO_MEDIO, ancora="center")

        pygame.draw.line(tela, E.BORDA, (r.x + 16, r.y + 296), (r.right - 16, r.y + 296))
        usadas = len(self.fase.escolhas)
        limite = self.fase.max_portas if self.fase.max_portas is not None else len(self.fase.slots)
        for k, (rot, val) in enumerate([("Orçamento" if self.fase.max_portas is not None else "Portas usadas",
                                         f"{usadas} / {limite}"),
                                        ("Mínimo", str(self.solucao.minimo_portas))]):
            y = r.y + 314 + k * 26
            E.texto(tela, rot, (r.x + 18, y), 13, E.TEXTO_MEDIO)
            E.texto(tela, val, (r.right - 18, y), 13, E.TEXTO, mono=True, ancora="topright")

        # botões secundários, no pé do painel (desenhados depois do painel, por cima dele)
        self.b_reiniciar.ativo = self.modo != "animando"
        self.b_reiniciar.desenhar(tela)
        if self.colapso:
            self.b_espiar.ativo = not self.espiou and self.modo != "animando"
            self.b_espiar.rotulo = "Espiar (E)" if not self.espiou else "Já espiou"
            self.b_espiar.desenhar(tela)

    def _desenhar_rodape(self, tela):
        teclas_w = E.fonte(12, True).size("1–9 portas · Enter ativa · R reinicia · I explicação · G glossário")[0]
        if self.fase.dica and not self.colapso:          # no Modo Colapso não há dicas
            dica = "Dica: " + self.fase.dica
            largura = E.LARGURA - 64 - teclas_w - 32
            uma_linha = E.fonte(13).size(dica)[0] <= largura
            area = pygame.Rect(32, 668 if uma_linha else 656, largura, 56)
            E.texto_quebrado(tela, dica, area, 13, E.TEXTO_MEDIO, entrelinha=1.4)
        teclas = "1–9 portas · Enter ativa · E espia · R reinicia" if self.colapso else \
            "1–9 portas · Enter ativa · R reinicia · I explicação · G glossário"
        E.texto(tela, teclas, (E.LARGURA - 32, 676), 12, E.TEXTO_APAGADO, mono=True, ancora="midright")

    def _desenhar_vitoria(self, tela):
        veu = pygame.Surface((E.LARGURA, E.ALTURA), pygame.SRCALPHA)
        veu.fill((4, 8, 15, 150))
        tela.blit(veu, (0, 0))
        caixa = pygame.Rect(0, 0, 540, 250)
        caixa.center = (E.LARGURA // 2, E.ALTURA // 2)
        E.painel(tela, caixa, E.PAINEL, E.OURO, raio=16, largura_borda=2)
        ultima = self.fase.id >= self.app.total_fases
        fim_do_jogo = ultima and not self.colapso
        E.texto(tela, "Laboratório completo!" if fim_do_jogo else "Detector aceso!",
                (caixa.centerx, caixa.y + 34), 30, E.OURO, negrito=True, ancora="midtop")
        usadas, minimo = len(self.fase.escolhas), self.solucao.minimo_portas
        linha = (f"Solução perfeita: {usadas} porta{'s' if usadas != 1 else ''}, o mínimo possível."
                 if usadas == minimo else f"Você usou {usadas} portas. Dá para fazer com {minimo}.")
        E.texto(tela, linha, (caixa.centerx, caixa.y + 90), 15, E.TEXTO, ancora="midtop")
        final = f"Estado final: {formatar(self.quadros[-1].vetor)}"
        tam = 14
        while E.fonte(tam, True).size(final)[0] > caixa.width - 40 and tam > 11:
            tam -= 1                              # estados de 3 e 4 qubits podem ser longos
        if E.fonte(tam, True).size(final)[0] > caixa.width - 40:
            final = "Estado final: veja as probabilidades no painel à esquerda"
        E.texto(tela, final, (caixa.centerx, caixa.y + 118), tam, E.TEXTO_SUAVE, mono=True, ancora="midtop")
        if fim_do_jogo:
            E.texto(tela, f"Você completou as {self.app.total_fases} fases do Qubit Lab.",
                    (caixa.centerx, caixa.y + 146), 15, E.GELO, negrito=True, ancora="midtop")
        if self.colapso and ultima:
            E.texto(tela, "Você venceu o Modo Colapso inteiro!", (caixa.centerx, caixa.y + 146), 15,
                    E.GELO, negrito=True, ancora="midtop")
        self.b_proxima.rotulo = "Voltar ao menu" if ultima else "Próxima fase"
        self.b_proxima.rect.topleft = (caixa.centerx - 230, caixa.bottom - 76)
        self.b_menu_fim.rect.topleft = (caixa.centerx + 90, caixa.bottom - 76)
        self.b_proxima.desenhar(tela)
        if not ultima:
            self.b_menu_fim.desenhar(tela)

    def _desenhar_fim_de_jogo(self, tela):
        veu = pygame.Surface((E.LARGURA, E.ALTURA), pygame.SRCALPHA)
        veu.fill((4, 8, 15, 170))
        tela.blit(veu, (0, 0))
        caixa = pygame.Rect(0, 0, 560, 250)
        caixa.center = (E.LARGURA // 2, E.ALTURA // 2)
        E.painel(tela, caixa, E.PAINEL, E.ALERTA, raio=16, largura_borda=2)
        E.texto(tela, "O gelo venceu", (caixa.centerx, caixa.y + 34), 30, E.ALERTA, negrito=True, ancora="midtop")
        volta = inicio_do_capitulo(self.fase.id)
        E.texto(tela, "As três vidas queimaram.", (caixa.centerx, caixa.y + 88), 15, E.TEXTO, ancora="midtop")
        E.texto(tela, f"Recomece do início do capítulo: fase {volta}.", (caixa.centerx, caixa.y + 114), 15,
                E.TEXTO_SUAVE, ancora="midtop")
        self.b_proxima.rotulo = f"Recomeçar (fase {volta})"
        self.b_proxima.rect.topleft = (caixa.centerx - 240, caixa.bottom - 76)
        self.b_menu_fim.rect.topleft = (caixa.centerx + 100, caixa.bottom - 76)
        self.b_proxima.desenhar(tela)
        self.b_menu_fim.desenhar(tela)
