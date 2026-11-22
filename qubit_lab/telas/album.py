"""Álbum de portas: as cartas já conquistadas, para rever quando quiser."""

from __future__ import annotations

import pygame

from ..core.capitulos import APRESENTACAO
from ..core.portas import porta as buscar_porta
from ..textos import carta
from ..ui import estilo as E
from ..ui.widgets import Botao, cadeado
from .base import Cabecalho, Tela
from .carta import Carta, desenhar_simbolo, fios_simbolo

COLUNAS, CARTAO_W, CARTAO_H, GAP = 6, 186, 236, 14
POR_PAGINA = 12


class Album(Tela):
    def __init__(self, app):
        super().__init__(app)
        self.ordem = sorted(APRESENTACAO, key=APRESENTACAO.get)
        vistas = len([p for p in self.ordem if p in app.progresso.portas_vistas])
        self.cab = Cabecalho(app, f"{vistas} de {len(self.ordem)} cartas", "Álbum de portas")
        largura = COLUNAS * CARTAO_W + (COLUNAS - 1) * GAP
        self.x0 = x0 = (E.LARGURA - largura) // 2
        self.pagina = 0
        self.paginas = max(1, (len(self.ordem) + POR_PAGINA - 1) // POR_PAGINA)
        self.b_voltar = Botao((x0, E.ALTURA - 72, 160, 48), "Voltar")
        self.b_anterior = Botao((E.LARGURA // 2 - 130, E.ALTURA - 72, 48, 48), "◀")
        self.b_proxima = Botao((E.LARGURA // 2 + 82, E.ALTURA - 72, 48, 48), "▶")
        self._montar()

    def _montar(self):
        self.cartoes = {}
        inicio = self.pagina * POR_PAGINA
        for i, nome in enumerate(self.ordem[inicio:inicio + POR_PAGINA]):
            linha, col = divmod(i, COLUNAS)
            self.cartoes[nome] = pygame.Rect(self.x0 + col * (CARTAO_W + GAP), 92 + linha * (CARTAO_H + GAP),
                                             CARTAO_W, CARTAO_H)
        self.b_anterior.ativo = self.pagina > 0
        self.b_proxima.ativo = self.pagina < self.paginas - 1

    def mudar_pagina(self, passo: int):
        nova = max(0, min(self.paginas - 1, self.pagina + passo))
        if nova != self.pagina:
            self.pagina = nova
            self._montar()

    def evento(self, e):
        if self.cab.evento(e):
            return
        if self.b_voltar.clicou(e) or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
            from .menu import Menu
            self.app.ir(Menu(self.app))
            return
        if self.b_anterior.clicou(e) or (e.type == pygame.KEYDOWN and e.key == pygame.K_LEFT):
            self.mudar_pagina(-1)
            return
        if self.b_proxima.clicou(e) or (e.type == pygame.KEYDOWN and e.key == pygame.K_RIGHT):
            self.mudar_pagina(1)
            return
        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            for nome, r in self.cartoes.items():
                if r.collidepoint(e.pos) and nome in self.app.progresso.portas_vistas:
                    self.app.ir(Carta(self.app, nome, None, voltar=self))
                    return

    def desenhar(self, tela):
        self.cab.desenhar(tela)
        mouse = pygame.mouse.get_pos()
        for nome, r in self.cartoes.items():
            k = self.ordem.index(nome)
            vista = nome in self.app.progresso.portas_vistas
            sobre = vista and r.collidepoint(mouse)
            E.painel(tela, r, E.PAINEL if vista else E.FUNDO_FUNDO,
                     E.OURO_CLARO if sobre else (E.OURO if vista else E.BORDA), raio=14,
                     largura_borda=2 if vista else 1)
            E.texto(tela, f"nº {k + 1:02d}", (r.right - 16, r.y + 14), 11, E.TEXTO_MEDIO, mono=True,
                    ancora="topright")
            area = pygame.Rect(r.x + 16, r.y + 34, r.width - 32, 110)
            E.painel(tela, area, E.FUNDO_FUNDO, E.BORDA, raio=10)
            if not vista:
                cadeado(tela, area.center)
                E.texto(tela, "???", (r.x + 16, r.y + 160), 22, E.TEXTO_APAGADO, negrito=True)
                E.texto(tela, f"aparece na fase {APRESENTACAO[nome]}", (r.x + 16, r.y + 196), 13,
                        E.TEXTO_APAGADO)
                continue
            n = buscar_porta(nome).n_qubits
            for y in fios_simbolo(n, area.centery, 70):
                pygame.draw.line(tela, E.COBRE, (area.x, y), (area.right, y), 2)
            desenhar_simbolo(tela, nome, area.center, 70)
            titulo, tam = buscar_porta(nome).titulo, 22
            while E.fonte(tam, False, True).size(titulo)[0] > r.width - 32 and tam > 13:
                tam -= 1                          # títulos longos encolhem para caber na carta
            E.texto(tela, titulo, (r.x + 16, r.y + 156 + (22 - tam) // 2), tam, E.TEXTO, negrito=True)
            E.texto(tela, carta(nome)["subtitulo"], (r.x + 16, r.y + 192), 14, E.GELO)
        self.b_voltar.desenhar(tela)
        if self.paginas > 1:
            self.b_anterior.desenhar(tela)
            self.b_proxima.desenhar(tela)
            E.texto(tela, f"página {self.pagina + 1} de {self.paginas}", (E.LARGURA // 2, E.ALTURA - 48), 14,
                    E.TEXTO_MEDIO, mono=True, ancora="center")
        E.texto(tela, "Clique numa carta para rever a porta", (E.LARGURA - 120, E.ALTURA - 48), 13,
                E.TEXTO_MEDIO, ancora="midright")
