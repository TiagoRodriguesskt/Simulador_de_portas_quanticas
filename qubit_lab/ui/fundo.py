"""Elementos de ambiente: cristais de gelo flutuando e o lustre do criostato."""

from __future__ import annotations

import math
import random

import pygame

from . import estilo as E


class Particulas:
    def __init__(self, quantidade=40, semente=11):
        rng = random.Random(semente)
        self.p = [[rng.uniform(0, E.LARGURA), rng.uniform(0, E.ALTURA), rng.uniform(4, 14),
                   rng.choice([1, 1, 2]), rng.uniform(0, math.tau)] for _ in range(quantidade)]
        self.rng = rng

    def atualizar(self, dt):
        for p in self.p:
            p[1] -= p[2] * dt
            if p[1] < -4:
                p[0], p[1] = self.rng.uniform(0, E.LARGURA), E.ALTURA + 4

    def desenhar(self, tela, t):
        for x, y, _, r, fase in self.p:
            cor = E.misturar(E.FUNDO, E.GELO, 0.3 + 0.25 * math.sin(t * 1.5 + fase))
            pygame.draw.circle(tela, cor, (int(x), int(y)), r)


def lustre(tela, t, cx=940):
    """O 'lustre' dourado do refrigerador de diluição, com o chip do qubit."""
    placas = [(80, 190, "50 K"), (190, 155, "4 K"), (300, 120, "800 mK"),
              (410, 88, "100 mK"), (510, 60, "10 mK")]
    pygame.draw.line(tela, E.COBRE, (cx, 0), (cx, 70), 6)
    for (y1, r1, _), (y2, r2, _) in zip(placas, placas[1:]):
        for lado in (-1, 1):
            pygame.draw.line(tela, E.COBRE, (cx + lado * (r1 - 80), y1), (cx + lado * (r2 - 45), y2), 3)
        pontos = [(cx + (12 if i % 2 else -12) * (r2 / 120), y1 + 6 + i * (y2 - y1 - 12) / 7)
                  for i in range(8)]
        pygame.draw.lines(tela, E.OURO, False, pontos, 2)
    for y, r, rotulo in placas:
        pygame.draw.ellipse(tela, E.COBRE, (cx - r, y - 10, 2 * r, 26))
        pygame.draw.ellipse(tela, E.OURO, (cx - r, y - 14, 2 * r, 26))
        E.texto(tela, rotulo, (cx + r + 20, y - 8), 14, E.GELO if rotulo == "10 mK" else E.TEXTO_SUAVE,
                mono=True)

    pulso = 0.5 + 0.5 * math.sin(t * 2.2)
    halo = pygame.Surface((160, 160), pygame.SRCALPHA)
    pygame.draw.circle(halo, (*E.GELO, int(18 + 22 * pulso)), (80, 80), 70)
    pygame.draw.circle(halo, (*E.GELO, int(30 + 30 * pulso)), (80, 80), 42)
    tela.blit(halo, (cx - 80, 505))
    pygame.draw.line(tela, E.COBRE, (cx, 515), (cx, 565), 4)
    pygame.draw.rect(tela, E.PAINEL, (cx - 20, 565, 40, 40), border_radius=4)
    pygame.draw.rect(tela, E.GELO, (cx - 20, 565, 40, 40), 2, border_radius=4)
    pygame.draw.rect(tela, E.GELO, (cx - 8, 577, 16, 16), border_radius=2)
    E.texto(tela, "chip do qubit", (cx, 660), 14, E.GELO, mono=True, ancora="center")
