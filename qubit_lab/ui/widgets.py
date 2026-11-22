"""Botões e outros elementos clicáveis."""

from __future__ import annotations

import pygame

from . import estilo as E


class Botao:
    """Um botão retangular. `estilo`: "primario" (ouro), "normal" ou "fantasma"."""

    def __init__(self, rect, rotulo: str, estilo: str = "normal", ativo: bool = True,
                 detalhe: str = "", tamanho: int = 16):
        self.rect = pygame.Rect(rect)
        self.rotulo = rotulo
        self.estilo = estilo
        self.ativo = ativo
        self.detalhe = detalhe          # texto menor à direita (ex.: "fase 4")
        self.tamanho = tamanho

    def clicou(self, evento) -> bool:
        return (self.ativo and evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1
                and self.rect.collidepoint(evento.pos))

    def desenhar(self, tela):
        sobre = self.ativo and self.rect.collidepoint(pygame.mouse.get_pos())
        if not self.ativo:
            fundo, borda, cor = E.FUNDO_FUNDO, E.BORDA, E.TEXTO_APAGADO
        elif self.estilo == "primario":
            fundo, borda, cor = (E.OURO_CLARO if sobre else E.OURO), None, E.ESCURO
        else:
            fundo = E.PAINEL_CLARO if sobre else E.PAINEL
            borda, cor = (E.OURO if sobre else E.BORDA_CLARA), E.TEXTO
        E.painel(tela, self.rect, fundo, borda, raio=10)
        negrito = self.estilo == "primario"
        if self.detalhe:
            E.texto(tela, self.rotulo, (self.rect.x + 20, self.rect.centery), self.tamanho, cor,
                    negrito=negrito, ancora="midleft")
            cor_det = E.ESCURO if self.estilo == "primario" and self.ativo else E.TEXTO_MEDIO
            E.texto(tela, self.detalhe, (self.rect.right - 20, self.rect.centery), 13, cor_det,
                    mono=True, ancora="midright")
        else:
            E.texto(tela, self.rotulo, self.rect.center, self.tamanho, cor, negrito=negrito,
                    ancora="center")


def cadeado(tela, centro, cor=E.TEXTO_APAGADO):
    """Ícone de cadeado fechado."""
    x, y = centro
    pygame.draw.rect(tela, cor, (x - 7, y - 1, 14, 11), 2, border_radius=2)
    pygame.draw.arc(tela, cor, (x - 5, y - 10, 10, 12), 0, 3.1416, 2)
    pygame.draw.line(tela, cor, (x - 5, y - 4), (x - 5, y - 1), 2)
    pygame.draw.line(tela, cor, (x + 4, y - 4), (x + 4, y - 1), 2)
