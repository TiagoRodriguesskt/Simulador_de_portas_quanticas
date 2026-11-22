"""Classe base das telas e o cabeçalho comum."""

from __future__ import annotations

import pygame

from ..ui import estilo as E
from ..ui.widgets import Botao


class Tela:
    def __init__(self, app):
        self.app = app

    def evento(self, e):
        pass

    def atualizar(self, dt: float):
        pass

    def desenhar(self, tela):
        pass


class Cabecalho:
    """Logo à esquerda, título no centro, botões de som e menu à direita."""

    def __init__(self, app, sobretitulo: str, titulo: str, ajuda=None, glossario=None):
        """ajuda / glossario: funções chamadas pelos botões "?" e do livro (só aparecem se passadas)."""
        self.app = app
        self.sobretitulo = sobretitulo
        self.titulo = titulo
        self.ajuda = ajuda
        self.glossario = glossario
        self.b_ajuda = Botao((E.LARGURA - 188, 12, 44, 44), "?")
        self.b_glossario = Botao((E.LARGURA - 244, 12, 44, 44), "")
        self.b_som = Botao((E.LARGURA - 132, 12, 44, 44), "♪")
        self.b_menu = Botao((E.LARGURA - 76, 12, 44, 44), "⌂")

    def evento(self, e) -> bool:
        """Trata cliques nos botões; devolve True se usou o evento."""
        if self.glossario and self.b_glossario.clicou(e):
            self.glossario()
            return True
        if self.ajuda and self.b_ajuda.clicou(e):
            self.ajuda()
            return True
        if self.b_som.clicou(e):
            self.app.alternar_som()
            return True
        if self.b_menu.clicou(e):
            from .menu import Menu
            self.app.ir(Menu(self.app))
            return True
        return False

    def desenhar(self, tela):
        E.texto(tela, "|q⟩", (32, 34), 18, E.OURO, mono=True, negrito=True, ancora="midleft")
        pygame.draw.rect(tela, E.COBRE, (26, 20, 50, 28), 1, border_radius=6)
        E.texto(tela, "QUBIT LAB", (90, 34), 19, E.OURO, negrito=True, ancora="midleft")
        E.texto(tela, self.sobretitulo.upper(), (E.LARGURA // 2, 22), 12, E.TEXTO_MEDIO,
                negrito=True, ancora="midtop")
        E.texto(tela, self.titulo, (E.LARGURA // 2, 40), 18, E.TEXTO, ancora="midtop")
        if self.ajuda:
            self.b_ajuda.desenhar(tela)
        if self.glossario:
            self.b_glossario.desenhar(tela)
            icone_livro(tela, self.b_glossario.rect.center)
        self.b_som.desenhar(tela)
        self.b_menu.desenhar(tela)
        if not self.app.audio.ligado:
            pygame.draw.line(tela, E.ALERTA, (self.b_som.rect.x + 12, self.b_som.rect.y + 12),
                             (self.b_som.rect.right - 12, self.b_som.rect.bottom - 12), 2)
        pygame.draw.line(tela, E.BORDA, (0, 68), (E.LARGURA, 68), 1)


def icone_livro(tela, centro, cor=E.TEXTO):
    """Livro aberto (botão do glossário)."""
    x, y = centro
    pygame.draw.lines(tela, cor, False, [(x, y - 6), (x - 4, y - 8), (x - 11, y - 8), (x - 11, y + 7),
                                         (x - 4, y + 7), (x, y + 9)], 2)
    pygame.draw.lines(tela, cor, False, [(x, y - 6), (x + 4, y - 8), (x + 11, y - 8), (x + 11, y + 7),
                                         (x + 4, y + 7), (x, y + 9)], 2)
    pygame.draw.line(tela, cor, (x, y - 6), (x, y + 9), 2)
