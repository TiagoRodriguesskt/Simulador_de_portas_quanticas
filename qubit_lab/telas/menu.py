"""Menu principal."""

from __future__ import annotations

import pygame

from .. import __version__
from ..ui import estilo as E
from ..ui.fundo import lustre
from ..ui.widgets import Botao
from .base import Tela


class Menu(Tela):
    def __init__(self, app):
        super().__init__(app)
        x, y, w, h, gap = 88, 336, 340, 48, 10
        prox = app.progresso.proxima(app.total_fases)
        feitas = len(app.progresso.concluidas)
        self.b_jogar = Botao((x, y, w, h), "Jogar", "primario", detalhe=f"fase {prox}", tamanho=18)
        self.b_fases = Botao((x, y + (h + gap), w, h), "Fases", detalhe=f"{feitas} / {app.total_fases}")
        prog = app.progresso
        detalhe = (f"recorde: fase {prog.recorde_colapso}" if prog.recorde_colapso
                   else "novo!") if prog.colapso_liberado() else "conclua a fase 10"
        self.b_colapso = Botao((x, y + 2 * (h + gap), w, h), "Modo Colapso",
                               ativo=prog.colapso_liberado(), detalhe=detalhe)
        from ..core.capitulos import APRESENTACAO
        vistas = len(set(APRESENTACAO) & prog.portas_vistas)
        meia = (w - gap) // 2
        self.b_album = Botao((x, y + 3 * (h + gap), meia, h), "Álbum", detalhe=f"{vistas}/{len(APRESENTACAO)}")
        self.b_glossario = Botao((x + meia + gap, y + 3 * (h + gap), w - meia - gap, h), "Glossário")
        self.b_som = Botao((x, y + 4 * (h + gap), w, h), "Som")
        self.b_sair = Botao((x, y + 5 * (h + gap), w, h), "Sair")
        self.botoes = [self.b_jogar, self.b_fases, self.b_colapso, self.b_album, self.b_glossario, self.b_som,
                       self.b_sair]
        self.prox = prox

    def evento(self, e):
        if e.type == pygame.KEYDOWN and e.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
            self.app.jogar(self.prox)
        elif e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            self.app.sair()
        elif self.b_jogar.clicou(e):
            self.app.jogar(self.prox)
        elif self.b_colapso.clicou(e):
            self.app.jogar_colapso(1)
        elif self.b_fases.clicou(e):
            from .selecao import Selecao
            self.app.ir(Selecao(self.app))
        elif self.b_glossario.clicou(e):
            from .glossario import Glossario
            self.app.ir(Glossario(self.app))
        elif self.b_album.clicou(e):
            from .album import Album
            self.app.ir(Album(self.app))
        elif self.b_som.clicou(e):
            self.app.alternar_som()
        elif self.b_sair.clicou(e):
            self.app.sair()

    def desenhar(self, tela):
        self.app.particulas.desenhar(tela, self.app.t)
        lustre(tela, self.app.t)
        E.texto(tela, "|ψ⟩ = α|0⟩ + β|1⟩", (88, 128), 16, E.GELO, mono=True)
        E.texto(tela, "QUBIT LAB", (82, 154), 72, E.OURO, negrito=True)
        E.texto(tela, "Aprenda computação quântica girando,", (88, 248), 19, E.TEXTO_SUAVE)
        E.texto(tela, "somando e medindo qubits.", (88, 276), 19, E.TEXTO_SUAVE)
        self.b_som.detalhe = "ligado" if self.app.audio.ligado else "desligado"
        for b in self.botoes:
            b.desenhar(tela)
        E.texto(tela, f"v{__version__} · inspirado em Portas Lógicas clássicas · feito por Tiago Rodrigues",
                (88, 702), 12, E.TEXTO_APAGADO, ancora="midleft")
