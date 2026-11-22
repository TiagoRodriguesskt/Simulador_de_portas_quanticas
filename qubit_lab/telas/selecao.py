"""Tela de seleção de fases, em páginas de 20 (5 colunas × 4 linhas)."""

from __future__ import annotations

import pygame

from ..core.capitulos import porta_nova
from ..core.portas import simbolo
from ..ui import estilo as E
from ..ui.widgets import Botao, cadeado
from .base import Cabecalho, Tela

COLUNAS, CARTAO_W, CARTAO_H, GAP = 5, 214, 112, 16
POR_PAGINA = 20


class Selecao(Tela):
    def __init__(self, app):
        super().__init__(app)
        self.cab = Cabecalho(app, "escolha uma fase", "Fases")
        self.titulos = {f.id: f.titulo for f in app.fases}
        self.ids = [f.id for f in app.fases]
        self.paginas = max(1, (len(self.ids) + POR_PAGINA - 1) // POR_PAGINA)
        # abre na página da próxima fase a jogar
        proxima = app.progresso.proxima(app.total_fases)
        self.pagina = min(self.paginas - 1, self.ids.index(proxima) // POR_PAGINA if proxima in self.ids else 0)
        largura = COLUNAS * CARTAO_W + (COLUNAS - 1) * GAP
        self.x0 = x0 = (E.LARGURA - largura) // 2
        self.b_voltar = Botao((x0, E.ALTURA - 84, 160, 48), "Voltar")
        self.b_anterior = Botao((E.LARGURA // 2 - 130, E.ALTURA - 84, 48, 48), "◀")
        self.b_proxima = Botao((E.LARGURA // 2 + 82, E.ALTURA - 84, 48, 48), "▶")
        self._montar()

    def _montar(self):
        """Posiciona os cartões da página atual."""
        self.cartoes = {}
        inicio = self.pagina * POR_PAGINA
        for i, id_fase in enumerate(self.ids[inicio:inicio + POR_PAGINA]):
            linha, col = divmod(i, COLUNAS)
            self.cartoes[id_fase] = pygame.Rect(self.x0 + col * (CARTAO_W + GAP), 92 + linha * (CARTAO_H + GAP),
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
        if e.type == pygame.MOUSEWHEEL:
            self.mudar_pagina(-e.y)
            return
        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            for id_fase, r in self.cartoes.items():
                if r.collidepoint(e.pos) and self.app.progresso.liberada(id_fase):
                    self.app.jogar(id_fase)
                    return

    def desenhar(self, tela):
        self.cab.desenhar(tela)
        mouse = pygame.mouse.get_pos()
        prog = self.app.progresso
        for id_fase, r in self.cartoes.items():
            liberada = prog.liberada(id_fase)
            feita = id_fase in prog.concluidas
            sobre = liberada and r.collidepoint(mouse)
            borda = E.OURO if sobre else (E.COBRE if feita else E.BORDA)
            E.painel(tela, r, E.PAINEL if liberada else E.FUNDO_FUNDO, borda)
            cor_num = E.OURO if liberada else E.TEXTO_APAGADO
            E.texto(tela, f"{id_fase:02d}", (r.x + 16, r.y + 12), 24, cor_num, mono=True, negrito=True)
            E.texto_quebrado(tela, self.titulos[id_fase], pygame.Rect(r.x + 16, r.y + 46, r.width - 32, 40), 14,
                             E.TEXTO if liberada else E.TEXTO_APAGADO, entrelinha=1.3)
            nova = porta_nova(id_fase)
            if nova:
                E.texto(tela, f"nova porta: {simbolo(nova)}", (r.x + 16, r.bottom - 22), 12, E.GELO, mono=True)
            if feita:
                E.texto(tela, "✓", (r.right - 16, r.y + 12), 20, E.OURO, ancora="topright")
            elif not liberada:
                cadeado(tela, (r.right - 26, r.y + 26))
        self.b_voltar.desenhar(tela)
        if self.paginas > 1:
            self.b_anterior.desenhar(tela)
            self.b_proxima.desenhar(tela)
            E.texto(tela, f"página {self.pagina + 1} de {self.paginas}", (E.LARGURA // 2, E.ALTURA - 60), 14,
                    E.TEXTO_MEDIO, mono=True, ancora="center")
        feitas = len(prog.concluidas)
        if prog.tudo_liberado:
            E.texto(tela, "modo de teste: todas as fases liberadas", (E.LARGURA // 2, E.ALTURA - 22), 12,
                    E.GELO, mono=True, ancora="center")
        E.texto(tela, f"{feitas} de {self.app.total_fases} fases concluídas", (E.LARGURA - 120, E.ALTURA - 60),
                14, E.TEXTO_MEDIO, mono=True, ancora="midright")
