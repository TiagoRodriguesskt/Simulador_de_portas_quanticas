"""Glossário: referência de todas as portas do jogo e dos conceitos principais.

Diferente do Álbum (que guarda as cartas conquistadas), o Glossário mostra tudo
desde o início, para consultar a qualquer momento: pelo menu ou pela bancada.
"""

from __future__ import annotations

import numpy as np
import pygame

from ..core import Circuito, Estado, formatar
from ..core.capitulos import APRESENTACAO
from ..core.portas import porta as buscar_porta
from ..core.portas import partes
from ..textos import CONCEITOS, GLOSSARIO, OUTRAS_PORTAS, carta, entrada_glossario
from ..ui import estilo as E
from ..ui.bloch import desenhar_esfera
from ..ui.widgets import Botao
from .base import Cabecalho, Tela
from .carta import (demo_da_porta, desenhar_simbolo, fios_simbolo, formatar_matriz, kets_que_mudam,
                    quadro_em_loop, tamanho_matriz, x_colunas)

LISTA = pygame.Rect(32, 88, 264, 560)
AREA_ITENS = pygame.Rect(LISTA.x, LISTA.y + 8, LISTA.width, LISTA.height - 16)   # parte que rola
DETALHE = pygame.Rect(316, 88, 932, 560)
ALTURA_ITEM = 32


def _exemplos_conceitos():
    """Ilustração de cada conceito: uma animação (lista de estados) ou None."""
    r = 1 / np.sqrt(2)
    parado = lambda vetor: [Estado(vetor)]
    return {
        "Qubit": parado([np.cos(0.6), np.sin(0.6) * np.exp(0.9j)]),
        "Superposição": Circuito(1).adicionar("H", [0]).animar(60),
        "Fase": Circuito(1).adicionar("Z", [0]).animar(60, inicial=Estado([r, r])),
        "Interferência": Circuito(1).adicionar("H", [0]).adicionar("H", [0]).animar(45),
        "Emaranhamento": Circuito(2).adicionar("CNOT", [0, 1]).animar(60, inicial=Estado([1, 0, 1, 0])),
        "Medição": None,
        "Esfera de Bloch": Circuito(1).adicionar("H", [0]).adicionar("S", [0]).animar(45),
    }


class Glossario(Tela):
    def __init__(self, app, voltar=None, selecionado: str | None = None):
        super().__init__(app)
        self.voltar = voltar
        self.cab = Cabecalho(app, "consulta", "Glossário")
        self.portas = sorted(GLOSSARIO, key=lambda nome: APRESENTACAO.get(nome, 99))
        self.outras = list(OUTRAS_PORTAS)                 # só no glossário: não aparecem nas fases
        self.conceitos = list(CONCEITOS)
        self.itens = ([("porta", p) for p in self.portas] + [("porta", p) for p in self.outras]
                      + [("conceito", c) for c in self.conceitos])
        # (índice do primeiro item, título) de cada seção da lista
        self.secoes = [(0, "Portas"), (len(self.portas), "Outras portas"),
                       (len(self.portas) + len(self.outras), "Conceitos")]
        if not self.outras:                       # todas as portas já estão nas fases: sem seção vazia
            self.secoes.pop(1)
        self.indice = 0
        if selecionado:
            for i, (_, nome) in enumerate(self.itens):
                if nome == selecionado:
                    self.indice = i
        self.t = 0.0
        self.demos = {p: demo_da_porta(p) for p in self.portas + self.outras}
        self.exemplos = _exemplos_conceitos()
        self.rolagem = 0                                  # pixels rolados na lista
        self.rects = self._montar_lista()
        self._mostrar_selecionado()
        rotulo = "Voltar para a bancada" if voltar is not None else "Voltar"
        self.b_voltar = Botao((LISTA.x, E.ALTURA - 62, LISTA.width, 44), rotulo)

    def _montar_lista(self):
        """Posição de cada item SEM rolagem; na tela, ele aparece `self.rolagem` pixels acima."""
        rects, y = [], LISTA.y + 44
        for k, (tipo, _) in enumerate(self.itens):
            if k > 0 and k in dict(self.secoes):
                y += 40                                   # espaço para o título da seção
            rects.append(pygame.Rect(LISTA.x + 12, y, LISTA.width - 24, ALTURA_ITEM - 4))
            y += ALTURA_ITEM
        self.altura_conteudo = y + 12 - AREA_ITENS.y
        return rects

    @property
    def rolagem_maxima(self) -> int:
        return max(0, self.altura_conteudo - AREA_ITENS.height)

    def rolar(self, pixels: int):
        self.rolagem = max(0, min(self.rolagem_maxima, self.rolagem + pixels))

    def _na_tela(self, r: pygame.Rect) -> pygame.Rect:
        return r.move(0, -self.rolagem)

    def _mostrar_selecionado(self):
        """Rola a lista o necessário para o item selecionado ficar visível."""
        r = self._na_tela(self.rects[self.indice])
        topo, base = AREA_ITENS.y + 8, AREA_ITENS.bottom - 8
        if self.indice == 0:
            self.rolagem = 0
        elif self.indice in dict(self.secoes):           # primeiro item da seção: mostra o título também
            self.rolar(r.top - 40 - topo if r.top - 40 < topo else 0)
        elif r.top < topo:
            self.rolar(r.top - topo)
        if r.bottom > base:
            self.rolar(r.bottom - base)

    # --------------------------------------------------------------- eventos ---
    def _sair(self):
        if self.voltar is not None:
            self.app.ir(self.voltar)
        else:
            from .menu import Menu
            self.app.ir(Menu(self.app))

    def selecionar(self, indice: int):
        self.indice = indice % len(self.itens)
        self.t = 0.0                                      # a animação recomeça
        self._mostrar_selecionado()

    def evento(self, e):
        if self.cab.evento(e):
            return
        if e.type == pygame.KEYDOWN:
            if e.key in (pygame.K_ESCAPE, pygame.K_BACKSPACE):
                self._sair()
            elif e.key in (pygame.K_DOWN, pygame.K_s):
                self.selecionar(self.indice + 1)
            elif e.key in (pygame.K_UP, pygame.K_w):
                self.selecionar(self.indice - 1)
        elif self.b_voltar.clicou(e):
            self._sair()
        elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            for k, r in enumerate(self.rects):
                if AREA_ITENS.collidepoint(e.pos) and self._na_tela(r).collidepoint(e.pos):
                    self.selecionar(k)
                    return
        elif e.type == pygame.MOUSEWHEEL:
            if LISTA.collidepoint(pygame.mouse.get_pos()):
                self.rolar(-e.y * ALTURA_ITEM)            # roda do mouse sobre a lista: rola
            else:
                self.selecionar(self.indice - e.y)        # no resto da tela: troca de item

    def atualizar(self, dt):
        self.t += dt

    # --------------------------------------------------------------- desenho ---
    def desenhar(self, tela):
        self.cab.desenhar(tela)
        self._desenhar_lista(tela)
        tipo, nome = self.itens[self.indice]
        E.painel(tela, DETALHE, E.PAINEL, E.BORDA_CLARA, raio=16)
        if tipo == "porta":
            self._desenhar_porta(tela, nome)
        else:
            self._desenhar_conceito(tela, nome)
        self.b_voltar.desenhar(tela)
        E.texto(tela, "↑ ↓ navegam · roda do mouse rola a lista · Esc volta", (DETALHE.right, E.ALTURA - 40), 12, E.TEXTO_APAGADO,
                mono=True, ancora="midright")

    def _desenhar_lista(self, tela):
        E.painel(tela, LISTA, E.FUNDO_FUNDO, E.BORDA, raio=14)
        recorte_antigo = tela.get_clip()
        tela.set_clip(AREA_ITENS)                         # nada é desenhado fora do painel
        for inicio, titulo in self.secoes:
            y = LISTA.y + 18 if inicio == 0 else self.rects[inicio].y - 26
            E.rotulo_secao(tela, titulo, (LISTA.x + 18, y - self.rolagem), E.OURO)
        mouse = pygame.mouse.get_pos()
        for k, ((tipo, nome), r0) in enumerate(zip(self.itens, self.rects)):
            r = self._na_tela(r0)
            if r.bottom < AREA_ITENS.top or r.top > AREA_ITENS.bottom:
                continue
            ativo = k == self.indice
            if ativo:
                E.painel(tela, r, E.PAINEL_CLARO, E.GELO, raio=8)
            elif r.collidepoint(mouse) and AREA_ITENS.collidepoint(mouse):
                E.painel(tela, r, E.PAINEL, None, raio=8)
            if tipo == "porta":
                E.texto(tela, partes(nome)[0], (r.x + 12, r.centery), 13,
                        E.GELO if ativo else E.OURO, mono=True, negrito=True, ancora="midleft")
                E.texto(tela, buscar_porta(nome).titulo, (r.x + 64, r.centery), 14,
                        E.TEXTO if ativo else E.TEXTO_SUAVE, ancora="midleft")
            else:
                tam = 14
                while E.fonte(tam).size(nome)[0] > r.width - 20 and tam > 10:
                    tam -= 1                      # "Transformada de Fourier quântica" encolhe para caber
                E.texto(tela, nome, (r.x + 12, r.centery), tam, E.TEXTO if ativo else E.TEXTO_SUAVE,
                        ancora="midleft")
        tela.set_clip(recorte_antigo)

        # barra de rolagem, quando a lista não cabe inteira
        if self.rolagem_maxima > 0:
            trilho = pygame.Rect(LISTA.right - 8, AREA_ITENS.y + 6, 3, AREA_ITENS.height - 12)
            pygame.draw.rect(tela, E.BORDA, trilho, border_radius=2)
            prop = AREA_ITENS.height / self.altura_conteudo
            alt = max(30, int(trilho.height * prop))
            y = trilho.y + int((trilho.height - alt) * self.rolagem / self.rolagem_maxima)
            pygame.draw.rect(tela, E.TEXTO_MEDIO, (trilho.x, y, 3, alt), border_radius=2)

    def _desenhar_porta(self, tela, nome):
        p = buscar_porta(nome)
        g = entrada_glossario(nome)
        d = DETALHE

        # --- cabeçalho: símbolo, nome e resumo ---------------------------------
        area = pygame.Rect(d.x + 24, d.y + 22, 132, 104)
        E.painel(tela, area, E.FUNDO_FUNDO, E.BORDA, raio=10)
        for y in fios_simbolo(p.n_qubits, area.centery, 64):
            pygame.draw.line(tela, E.COBRE, (area.x, y), (area.right, y), 2)
        desenhar_simbolo(tela, nome, area.center, 64)
        x0 = area.right + 24
        E.texto(tela, p.titulo, (x0, d.y + 24), 30, E.TEXTO, negrito=True)
        E.texto(tela, g.get("subtitulo") or carta(nome)["subtitulo"], (x0, d.y + 66), 15, E.GELO)
        E.texto_quebrado(tela, g["resumo"], pygame.Rect(x0, d.y + 94, 520, 40), 15, E.TEXTO_SUAVE)
        onde = f"apresentada na fase {APRESENTACAO[nome]}" if nome in APRESENTACAO else "só no glossário"
        info = f"{p.n_qubits} qubit{'s' if p.n_qubits > 1 else ''} · {onde}"
        E.texto(tela, info, (d.right - 24, d.y + 30), 12, E.TEXTO_MEDIO, mono=True, ancora="topright")
        pygame.draw.line(tela, E.BORDA, (d.x + 24, d.y + 144), (d.right - 24, d.y + 144))

        # --- coluna esquerda: o que faz, esfera, relações --------------------------
        col = pygame.Rect(d.x + 24, d.y + 162, 470, 380)
        E.rotulo_secao(tela, "O que faz", (col.x, col.y), E.OURO)
        h = E.texto_quebrado(tela, g["faz"], pygame.Rect(col.x, col.y + 24, col.width, 140), 14, entrelinha=1.5)

        y = col.y + 24 + h + 18
        E.rotulo_secao(tela, "Na esfera de Bloch", (col.x, y), E.OURO)
        q = quadro_em_loop(self.demos[nome], self.t)
        if p.n_qubits == 1:
            desenhar_esfera(tela, (col.x + 50, y + 74), 46, q.bloch(0), rotulos=False)
            x_txt = col.x + 116
        else:
            passo, raio = (72, 30) if p.n_qubits <= 3 else (58, 25)     # 4 qubits: esferas menores
            for i in range(p.n_qubits):
                desenhar_esfera(tela, (col.x + 34 + i * passo, y + 74), raio, q.bloch(i), rotulos=False)
            x_txt = col.x + 34 + p.n_qubits * passo
        E.texto_quebrado(tela, g["esfera"], pygame.Rect(x_txt, y + 40, col.right - x_txt, 80), 14,
                         E.TEXTO_SUAVE)

        y += 140
        E.rotulo_secao(tela, "Relações úteis", (col.x, y), E.OURO)
        for k, rel in enumerate(g["relacoes"]):
            yy = y + 26 + k * 24
            pygame.draw.circle(tela, E.COBRE, (col.x + 5, yy + 8), 3)
            E.texto(tela, rel, (col.x + 18, yy), 14, E.TEXTO)

        # --- coluna direita: matriz, ação na base, Qiskit ------------------------
        cd = pygame.Rect(d.x + 522, d.y + 162, d.right - 24 - (d.x + 522), 380)
        E.rotulo_secao(tela, "Matriz", (cd.x, cd.y), E.OURO)
        self._desenhar_matriz(tela, nome, (cd.x, cd.y + 30))

        y = cd.y + {1: 100, 2: 150, 3: 186}.get(p.n_qubits, 120)
        E.rotulo_secao(tela, "O que faz com cada entrada", (cd.x, y), E.OURO)
        y += 26
        kets = [format(i, f"0{p.n_qubits}b") for i in range(2 ** p.n_qubits)]
        if p.n_qubits >= 3:
            kets = kets_que_mudam(p)
        for k in kets:
            saida = Estado.da_base(k).aplicar(p, range(p.n_qubits))
            mudou = not np.allclose(saida.vetor, Estado.da_base(k).vetor)
            E.texto(tela, f"|{k}⟩  →  {formatar(saida.vetor, manter_fase=True)}", (cd.x, y), 14,
                    E.TEXTO if mudou else E.TEXTO_MEDIO, mono=True)
            y += 22
        if p.n_qubits >= 3:
            E.texto(tela, f"as outras {2 ** p.n_qubits - len(kets)} entradas não mudam", (cd.x, y), 13, E.TEXTO_MEDIO)
            y += 22

        y = cd.bottom - 66
        E.rotulo_secao(tela, "Em Python, no Qiskit", (cd.x, y), E.OURO)
        caixa = pygame.Rect(cd.x, y + 22, cd.width, 38)
        E.painel(tela, caixa, E.FUNDO_FUNDO, E.BORDA, raio=8)
        tam = 15
        while E.fonte(tam, True).size(g["qiskit"])[0] > caixa.width - 28 and tam > 10:
            tam -= 1                                      # linhas longas encolhem para caber na caixa
        E.texto(tela, g["qiskit"], (caixa.x + 14, caixa.centery), tam, E.GELO, mono=True, ancora="midleft")

    def _desenhar_matriz(self, tela, nome, pos):
        p = buscar_porta(nome)
        if p.n_qubits >= 4:                               # 16 × 16 não cabe: descreve em palavras
            n = 2 ** p.n_qubits
            E.texto_quebrado(tela, f"{n} × {n}: a identidade, menos no canto de baixo, onde fica um X "
                             f"(troca |{'1' * (p.n_qubits - 1)}0⟩ e |{'1' * p.n_qubits}⟩).",
                             pygame.Rect(pos[0], pos[1], DETALHE.right - 24 - pos[0], 60), 14, E.TEXTO_SUAVE)
            return
        fator, linhas = formatar_matriz(p.matriz)
        rotulo = f"{partes(nome)[0]} ="
        livre = DETALHE.right - 24 - pos[0] - E.fonte(15, True).size(rotulo)[0] - 12 - 10
        if fator:
            livre -= E.fonte(15, True).size(fator)[0] + 10
        tam, cols = tamanho_matriz(linhas, {1: 17, 2: 13, 3: 10}[p.n_qubits],
                                       {1: 46, 2: 34, 3: 24}[p.n_qubits], livre)
        passo = tam + 7
        x, y = pos
        altura = len(linhas) * passo
        meio = y + altura // 2 - 2
        E.texto(tela, rotulo, (x, meio), 15, E.TEXTO, mono=True, ancora="midleft")
        x += E.fonte(15, True).size(rotulo)[0] + 12
        if fator:
            E.texto(tela, fator, (x, meio), 15, E.TEXTO, mono=True, ancora="midleft")
            x += E.fonte(15, True).size(fator)[0] + 10
        direita = x + sum(cols) + 10
        centros = x_colunas(x, cols)
        pygame.draw.line(tela, E.TEXTO_MEDIO, (x, y - 4), (x, y + altura), 2)
        pygame.draw.line(tela, E.TEXTO_MEDIO, (direita, y - 4), (direita, y + altura), 2)
        for i, linha in enumerate(linhas):
            for j, entrada in enumerate(linha):
                cor = E.AMBAR if entrada.startswith("−") else (E.TEXTO if entrada != "0" else E.TEXTO_APAGADO)
                E.texto(tela, entrada, (centros[j], y + i * passo), tam, cor,
                        mono=True, ancora="midtop")

    def _desenhar_conceito(self, tela, nome):
        d = DETALHE
        E.texto(tela, "CONCEITO", (d.x + 32, d.y + 28), 12, E.OURO, negrito=True)
        E.texto(tela, nome, (d.x + 32, d.y + 50), 32, E.TEXTO, negrito=True)
        exemplo = self.exemplos.get(nome)
        largura_texto = 520 if exemplo else d.width - 64
        E.texto_quebrado(tela, CONCEITOS[nome], pygame.Rect(d.x + 32, d.y + 116, largura_texto, 380), 16,
                         entrelinha=1.6)
        if not exemplo:
            return
        q = quadro_em_loop(exemplo, self.t) if len(exemplo) > 1 else exemplo[0]
        cx, cy = d.x + 760, d.y + 250
        if q.n_qubits == 1:
            desenhar_esfera(tela, (cx, cy), 110, q.bloch(0))
        else:
            for i in range(q.n_qubits):
                desenhar_esfera(tela, (cx - 80 + i * 160, cy), 64, q.bloch(i), rotulos=False)
                E.texto(tela, f"qubit {i}", (cx - 80 + i * 160, cy + 82), 12, E.TEXTO_MEDIO, mono=True,
                        ancora="center")
        # a fórmula aparece só nos estados "redondos": antes e depois da animação
        linhas = ([("", exemplo[0])] if len(exemplo) == 1
                  else [("antes:  ", exemplo[0]), ("depois: ", exemplo[-1])])
        for k, (rotulo, est) in enumerate(linhas):
            txt = f"{rotulo}|ψ⟩ = {formatar(est.vetor)}"
            tam = 15
            while E.fonte(tam, True).size(txt)[0] > 380 and tam > 10:
                tam -= 1
            E.texto(tela, txt, (cx, cy + 150 + k * 26), tam, E.TEXTO if k == len(linhas) - 1 else E.TEXTO_SUAVE,
                    mono=True, ancora="center")
