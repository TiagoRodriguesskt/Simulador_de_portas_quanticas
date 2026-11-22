"""Cores, fontes e funções de desenho de texto (docs/DESIGN.md)."""

from __future__ import annotations

from functools import lru_cache

import pygame

from ..caminhos import recurso

LARGURA, ALTURA = 1280, 720

FUNDO = (6, 11, 20)
FUNDO_FUNDO = (10, 18, 32)
PAINEL = (16, 28, 44)
PAINEL_CLARO = (26, 38, 56)
BORDA = (27, 42, 62)
BORDA_CLARA = (42, 61, 85)
COBRE = (194, 112, 61)
OURO = (232, 184, 92)
OURO_CLARO = (245, 208, 140)
GELO = (127, 227, 255)
AMBAR = (255, 154, 60)
TEXTO = (230, 241, 250)
TEXTO_SUAVE = (169, 187, 208)
TEXTO_MEDIO = (143, 166, 191)
TEXTO_APAGADO = (110, 130, 154)
ALERTA = (255, 77, 94)
ESCURO = (26, 18, 6)          # texto sobre o ouro

# As fontes vão junto com o jogo (assets/fontes), então o texto fica igual
# em Linux, Windows e macOS, inclusive símbolos como ⟩, ψ, √ e ⊕.
_ARQUIVOS = {
    (False, False): "DejaVuSans.ttf",
    (False, True): "DejaVuSans-Bold.ttf",
    (True, False): "DejaVuSansMono.ttf",
    (True, True): "DejaVuSansMono-Bold.ttf",
}


@lru_cache(maxsize=None)
def fonte(tamanho: int, mono: bool = False, negrito: bool = False) -> pygame.font.Font:
    caminho = recurso("fontes", _ARQUIVOS[(mono, negrito)])
    try:
        return pygame.font.Font(str(caminho), tamanho)
    except (FileNotFoundError, OSError):
        return pygame.font.SysFont(None, tamanho, bold=negrito)


def texto(tela, conteudo: str, pos, tamanho=16, cor=TEXTO, mono=False, negrito=False,
          ancora="topleft") -> pygame.Rect:
    """Desenha um texto e devolve o retângulo que ele ocupou."""
    img = fonte(tamanho, mono, negrito).render(conteudo, True, cor)
    r = img.get_rect(**{ancora: pos})
    tela.blit(img, r)
    return r


def texto_quebrado(tela, conteudo: str, rect: pygame.Rect, tamanho=16, cor=TEXTO,
                   mono=False, entrelinha=1.45) -> int:
    """Texto com quebra de linha automática dentro de `rect`. Devolve a altura usada."""
    f = fonte(tamanho, mono)
    palavras, linhas, atual = conteudo.split(), [], ""
    for p in palavras:
        teste = f"{atual} {p}".strip()
        if f.size(teste)[0] <= rect.width:
            atual = teste
        else:
            linhas.append(atual)
            atual = p
    if atual:
        linhas.append(atual)
    passo = int(tamanho * entrelinha)
    for i, linha in enumerate(linhas):
        tela.blit(f.render(linha, True, cor), (rect.x, rect.y + i * passo))
    return len(linhas) * passo


def rotulo_secao(tela, conteudo: str, pos, cor=TEXTO_MEDIO):
    """Os títulos pequenos em caixa alta, como "ESFERA DE BLOCH"."""
    return texto(tela, conteudo.upper(), pos, 12, cor, negrito=True)


def painel(tela, rect, cor=PAINEL, borda=BORDA, raio=12, largura_borda=1):
    pygame.draw.rect(tela, cor, rect, border_radius=raio)
    if borda:
        pygame.draw.rect(tela, borda, rect, largura_borda, border_radius=raio)


def tracejado(tela, cor, rect, traco=8, espaco=6, largura=2):
    """Retângulo com borda tracejada (os slots vazios)."""
    x0, y0, x1, y1 = rect.left, rect.top, rect.right - 1, rect.bottom - 1
    for (ax, ay), (bx, by) in [((x0, y0), (x1, y0)), ((x1, y0), (x1, y1)),
                               ((x1, y1), (x0, y1)), ((x0, y1), (x0, y0))]:
        comprimento = max(abs(bx - ax), abs(by - ay))
        d = 0
        while d < comprimento:
            f = min(d + traco, comprimento)
            p1 = (ax + (bx - ax) * d / comprimento, ay + (by - ay) * d / comprimento)
            p2 = (ax + (bx - ax) * f / comprimento, ay + (by - ay) * f / comprimento)
            pygame.draw.line(tela, cor, p1, p2, largura)
            d += traco + espaco


def misturar(c1, c2, t: float):
    """Cor entre c1 (t=0) e c2 (t=1)."""
    t = max(0.0, min(1.0, t))
    return tuple(int(a + (b - a) * t) for a, b in zip(c1, c2))
