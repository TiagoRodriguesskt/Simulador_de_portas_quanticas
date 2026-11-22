"""Desenho da esfera de Bloch em perspectiva (projeção ortográfica)."""

from __future__ import annotations

import math

import numpy as np
import pygame

from . import estilo as E

# Câmera: olhando um pouco de cima (20°) e de lado (30°), de modo que
# o eixo x aponta para o jogador (embaixo, à esquerda), y para a direita e z para cima.
_AZ, _EL = math.radians(30), math.radians(20)
_D = np.array([math.cos(_EL) * math.cos(_AZ), math.cos(_EL) * math.sin(_AZ), math.sin(_EL)])
_DIREITA = np.cross([0, 0, 1], _D)
_DIREITA /= np.linalg.norm(_DIREITA)
_CIMA = np.cross(_D, _DIREITA)


def projetar(v, centro, raio):
    """Ponto 3D (na esfera unitária) → (x, y) na tela, e a profundidade (>0 = frente)."""
    v = np.asarray(v, dtype=float)
    return (centro[0] + raio * float(v @ _DIREITA), centro[1] - raio * float(v @ _CIMA)), float(v @ _D)


def _circulo_maximo(tela, centro, raio, eixo_a, eixo_b, cor_frente, cor_tras, largura=1):
    """Desenha um círculo da esfera: a metade de trás mais apagada e tracejada."""
    pontos = []
    for i in range(73):
        t = 2 * math.pi * i / 72
        pontos.append(projetar(np.cos(t) * eixo_a + np.sin(t) * eixo_b, centro, raio))
    for i in range(72):
        (p1, z1), (p2, _) = pontos[i], pontos[i + 1]
        if z1 >= 0:
            pygame.draw.line(tela, cor_frente, p1, p2, largura)
        elif i % 2 == 0:
            pygame.draw.line(tela, cor_tras, p1, p2, largura)


def desenhar_esfera(tela, centro, raio, vetor, rastro=(), rotulos=True, apagada=False):
    """Esfera de Bloch com o vetor de estado.

    vetor:  (x, y, z) do qubit; comprimento < 1 indica emaranhamento.
    rastro: pontos anteriores do vetor, para mostrar o caminho percorrido.
    """
    cx, cy = centro
    pygame.draw.circle(tela, E.FUNDO_FUNDO, centro, raio)
    pygame.draw.circle(tela, E.BORDA_CLARA, centro, raio, 2)

    ex, ey, ez = np.eye(3)
    _circulo_maximo(tela, centro, raio, ex, ey, E.BORDA_CLARA, E.BORDA)      # equador
    _circulo_maximo(tela, centro, raio, ex, ez, E.BORDA, E.FUNDO_FUNDO)      # meridiano x-z

    for eixo in (ex, ey, ez):
        (a, _), (b, _) = projetar(-eixo, centro, raio), projetar(eixo, centro, raio)
        pygame.draw.line(tela, E.BORDA_CLARA, a, b, 1)

    (topo, _), (base, _) = projetar(ez, centro, raio), projetar(-ez, centro, raio)
    pygame.draw.circle(tela, E.GELO, topo, max(3, raio // 28))
    pygame.draw.circle(tela, E.AMBAR, base, max(3, raio // 28))
    if rotulos:
        t = max(11, raio // 7)
        E.texto(tela, "|0⟩", (topo[0], topo[1] - 6), t, E.GELO, mono=True, ancora="midbottom")
        E.texto(tela, "|1⟩", (base[0], base[1] + 6), t, E.AMBAR, mono=True, ancora="midtop")
        (px, _), (py, _) = projetar(ex * 1.18, centro, raio), projetar(ey * 1.16, centro, raio)
        E.texto(tela, "x", px, t - 1, E.TEXTO_MEDIO, mono=True, ancora="center")
        E.texto(tela, "y", py, t - 1, E.TEXTO_MEDIO, mono=True, ancora="center")

    if apagada:            # Modo Colapso: o estado fica escondido sob o gelo
        gelo = pygame.Surface((2 * raio + 4, 2 * raio + 4), pygame.SRCALPHA)
        c = (raio + 2, raio + 2)
        pygame.draw.circle(gelo, (*E.GELO, 70), c, raio)
        pygame.draw.circle(gelo, (230, 248, 255, 140), c, raio, 3)
        # rachaduras e reflexos do gelo
        for a1, a2, f1, f2 in [(0.3, 1.1, 0.15, 0.85), (2.2, 2.9, 0.2, 0.7), (4.0, 4.6, 0.1, 0.9),
                               (5.2, 5.9, 0.3, 0.6)]:
            p1 = (c[0] + math.cos(a1) * raio * f1, c[1] + math.sin(a1) * raio * f1)
            p2 = (c[0] + math.cos(a2) * raio * f2, c[1] + math.sin(a2) * raio * f2)
            pygame.draw.line(gelo, (240, 252, 255, 120), p1, p2, 1)
        pygame.draw.arc(gelo, (255, 255, 255, 110), (c[0] - raio * 0.7, c[1] - raio * 0.8, raio * 0.9, raio * 0.9),
                        1.8, 2.8, 3)
        tela.blit(gelo, (cx - raio - 2, cy - raio - 2))
        E.texto(tela, "?", centro, max(16, raio // 2), (240, 252, 255), negrito=True, ancora="center")
        return

    # rastro do caminho, mais forte perto do presente
    n = len(rastro)
    for i, p in enumerate(rastro):
        (q, _) = projetar(p, centro, raio)
        cor = E.misturar(E.FUNDO_FUNDO, E.OURO, 0.15 + 0.55 * (i + 1) / max(n, 1))
        pygame.draw.circle(tela, cor, q, 2)

    v = np.asarray(vetor, dtype=float)
    comprimento = float(np.linalg.norm(v))
    (ponta, prof) = projetar(v, centro, raio)
    if comprimento < 0.03:
        # emaranhamento máximo: o vetor some no centro
        pygame.draw.circle(tela, E.OURO, centro, 4, 1)
        return
    cor = E.OURO if prof >= -0.05 else E.misturar(E.OURO, E.FUNDO_FUNDO, 0.35)
    pygame.draw.line(tela, cor, centro, ponta, 3)
    halo = pygame.Surface((40, 40), pygame.SRCALPHA)
    pygame.draw.circle(halo, (*E.OURO, 50), (20, 20), 14)
    tela.blit(halo, (ponta[0] - 20, ponta[1] - 20))
    pygame.draw.circle(tela, cor, ponta, 6)
