"""Tela de explicação: aparece antes de toda fase que não apresenta uma porta nova.

(As fases com porta nova mostram a carta da porta, em carta.py.)
Também pode ser aberta no meio da fase, pelo botão "?" da bancada.
"""

from __future__ import annotations

import numpy as np
import pygame

from ..core.portas import porta as buscar_porta
from ..core.portas import partes
from ..core.solver import resolver
from ..ui import estilo as E
from ..ui.bloch import desenhar_esfera
from ..ui.simbolos import largura_rotulo, rotulo
from ..ui.widgets import Botao
from .base import Cabecalho, Tela


def vetor_alvo(objetivo, n_qubits):
    """Vetor de Bloch do alvo, quando dá para mostrar numa esfera só (senão, None)."""
    if objetivo.tipo == "probabilidade" and n_qubits == 1:
        return np.array([0, 0, 1.0 if objetivo.ket == "0" else -1.0])
    if objetivo.tipo == "estado" and n_qubits == 1:
        return objetivo.alvo.bloch(0)
    if objetivo.tipo == "bloch":
        return objetivo.alvo.bloch(0)
    return None


class Explicacao(Tela):
    def __init__(self, app, id_fase: int, voltar=None):
        super().__init__(app)
        self.fase = app.nova_fase(id_fase)
        self.voltar = voltar                       # bancada aberta, quando vem do botão "?"
        self.minimo = resolver(self.fase).minimo_portas
        self.cab = Cabecalho(app, f"fase {id_fase} de {app.total_fases}", "Explicação")
        rotulo = "Voltar para a bancada" if voltar else "Começar a fase"
        self.b_continuar = Botao((958, 640, 250, 52), rotulo, "primario")

    def _continuar(self):
        if self.voltar is not None:
            self.app.ir(self.voltar)
        else:
            from .bancada import Bancada
            self.app.ir(Bancada(self.app, self.fase.id))

    def evento(self, e):
        if self.cab.evento(e):
            return
        if e.type == pygame.KEYDOWN:
            if e.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
                self._continuar()
            elif e.key == pygame.K_ESCAPE:
                if self.voltar is not None:
                    self.app.ir(self.voltar)
                else:
                    from .menu import Menu
                    self.app.ir(Menu(self.app))
        elif self.b_continuar.clicou(e):
            self._continuar()

    def desenhar(self, tela):
        self.cab.desenhar(tela)
        f = self.fase

        # --- painel principal ---------------------------------------------
        r = pygame.Rect(72, 92, 720, 530)
        E.painel(tela, r, E.PAINEL, E.BORDA_CLARA, raio=16)
        E.texto(tela, f"FASE {f.id:02d}", (r.x + 32, r.y + 28), 14, E.OURO, mono=True, negrito=True)
        E.texto(tela, f.titulo, (r.x + 32, r.y + 52), 32, E.TEXTO, negrito=True)

        y = r.y + 116
        E.rotulo_secao(tela, "Objetivo", (r.x + 32, y), E.OURO)
        E.texto_quebrado(tela, f.objetivo.descrever(), pygame.Rect(r.x + 32, y + 24, r.width - 64, 50), 17)

        y += 92
        E.rotulo_secao(tela, "A ideia", (r.x + 32, y), E.OURO)
        texto = f.explicacao or f.dica
        altura = E.texto_quebrado(tela, texto, pygame.Rect(r.x + 32, y + 24, r.width - 64, 220), 16,
                                  entrelinha=1.55)

        y = max(y + 24 + altura + 28, r.bottom - 104)
        E.rotulo_secao(tela, "Portas na bandeja", (r.x + 32, y), E.OURO)
        x = r.x + 32
        for nome in f.disponiveis:
            base, angulo = partes(nome)
            tam = 18 if len(base) <= 2 and not angulo else 14 if angulo else 13
            larg = max(52, largura_rotulo(nome, tam) + 22)
            chip = pygame.Rect(x, y + 26, larg, 44)
            E.painel(tela, chip, E.PAINEL_CLARO, E.COBRE, raio=8)
            rotulo(tela, nome, chip.center, tam, E.OURO)
            x += larg + 8
        E.texto(tela, f"{f.n_qubits} qubit{'s' if f.n_qubits > 1 else ''}", (r.right - 32, y), 13,
                E.TEXTO_MEDIO, mono=True, ancora="topright")

        # --- aonde chegar ---------------------------------------------------
        a = pygame.Rect(816, 92, 392, 530)
        E.painel(tela, a, E.FUNDO_FUNDO, E.BORDA, raio=16)
        E.rotulo_secao(tela, "Aonde chegar", (a.x + 24, a.y + 24), E.OURO)
        alvo = vetor_alvo(f.objetivo, f.n_qubits)
        if alvo is not None:
            desenhar_esfera(tela, (a.centerx, a.y + 210), 110, alvo)
            legenda = (f"qubit {f.objetivo.qubit}" if f.objetivo.tipo == "bloch" else "o vetor tem que chegar aqui")
            E.texto(tela, legenda, (a.centerx, a.y + 356), 13, E.TEXTO_MEDIO, ancora="center")
        else:
            from ..core import formatar
            o = f.objetivo
            if o.tipo == "estado":
                grande, frase = o.formula_do_alvo(), "Os qubits terminam juntos neste estado."
            elif o.tipo == "qubit":
                grande, frase = (f"qubit {o.qubit} → {o.valor}",
                                 f"Só o qubit {o.qubit} importa: ao ser medido, ele tem que dar {o.valor} sempre.")
            else:
                grande, frase = (f"|{o.ket}⟩",
                                 f"Ao medir os {f.n_qubits} qubits, o resultado tem que ser |{o.ket}⟩ sempre.")
            # o estado-alvo, o maior possível; estados longos encolhem e, se preciso, quebram em duas linhas
            linhas, tam = [grande], 34
            cabe = lambda: all(E.fonte(tam, True, True).size(x)[0] <= a.width - 48 for x in linhas)
            while not cabe() and tam > 14:
                tam -= 2
            if not cabe() and " + " in grande:
                partes_txt = grande.split(" + ")
                meio = len(partes_txt) // 2
                linhas = [" + ".join(partes_txt[:meio]) + " +", " + ".join(partes_txt[meio:])]
                tam = 20
                while not cabe() and tam > 11:
                    tam -= 1
            for k, linha in enumerate(linhas):
                y_linha = a.y + 170 + (k - (len(linhas) - 1) / 2) * (tam + 10)
                E.texto(tela, linha, (a.centerx, y_linha), tam, E.AMBAR, mono=True, negrito=True, ancora="center")
            E.texto_quebrado(tela, frase, pygame.Rect(a.x + 32, a.y + 230, a.width - 64, 120), 15, E.TEXTO_SUAVE)
        pygame.draw.line(tela, E.BORDA, (a.x + 24, a.y + 396), (a.right - 24, a.y + 396))
        linhas = [("Mínimo de portas", str(self.minimo)),
                  ("Slots (todos obrigatórios)" if f.completo else "Slots para preencher", str(len(f.slots)))]
        if f.max_portas is not None:              # fase com orçamento: o limite aparece em destaque
            linhas[1] = ("Orçamento de portas", f"no máximo {f.max_portas}")
        for k, (rot, val) in enumerate(linhas):
            yy = a.y + 418 + k * 30
            E.texto(tela, rot, (a.x + 24, yy), 14, E.TEXTO_MEDIO)
            E.texto(tela, val, (a.right - 24, yy), 14, E.TEXTO, mono=True, ancora="topright")
        if f.dica and f.explicacao:
            E.texto(tela, "A dica aparece no rodapé da bancada.", (a.x + 24, a.bottom - 40), 12,
                    E.TEXTO_APAGADO)

        self.b_continuar.desenhar(tela)
        E.texto(tela, "Enter para continuar", (self.b_continuar.rect.x - 20, self.b_continuar.rect.centery), 13,
                E.TEXTO_APAGADO, ancora="midright")
