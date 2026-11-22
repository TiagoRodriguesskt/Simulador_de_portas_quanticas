"""O aplicativo: janela, laço principal e navegação entre telas."""

from __future__ import annotations

import copy

import pygame

from .audio import Audio
from .core import carregar_fases
from .core.capitulos import porta_nova
from .progresso import Progresso
from .ui import estilo as E
from .ui.fundo import Particulas

FPS = 60


class App:
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 2, 512)
        pygame.init()
        try:
            pygame.mixer.init()
        except pygame.error:
            pass                                  # computador sem som: o jogo segue mudo
        E.fonte.cache_clear()                     # fontes de uma sessão anterior do pygame não valem mais
        pygame.display.set_caption("Qubit Lab")
        self.janela = pygame.display.set_mode((E.LARGURA, E.ALTURA))
        self.relogio = pygame.time.Clock()
        self.t = 0.0
        self.progresso = Progresso()
        self.audio = Audio(self.progresso.som)
        self.fases = carregar_fases()
        self.total_fases = len(self.fases)
        self.particulas = Particulas()
        self.rodando = True
        from .telas.menu import Menu
        self.atual = Menu(self)

    # ----------------------------------------------------------- navegação ---
    def ir(self, tela):
        if tela is not self.atual:
            self.audio.parar_efeitos()     # sair de uma tela interrompe o som que ela tocava
        self.atual = tela

    def nova_fase(self, id_fase: int):
        """Uma cópia "limpa" da fase (sem as escolhas de uma partida anterior)."""
        return copy.deepcopy(next(f for f in self.fases if f.id == id_fase))

    def jogar(self, id_fase: int):
        """Abre a fase sempre pela explicação: a carta da porta nova, ou a tela de explicação."""
        self.ir(self.explicacao(id_fase))

    def explicacao(self, id_fase: int, voltar=None):
        """A tela que explica a fase. Com `voltar`, ela retorna para essa tela (a bancada aberta)."""
        from .telas.carta import Carta
        from .telas.explicacao import Explicacao
        nova = porta_nova(id_fase)
        if nova:
            return Carta(self, nova, id_fase, voltar=voltar)
        return Explicacao(self, id_fase, voltar=voltar)

    def jogar_colapso(self, id_fase: int, sessao=None):
        """Abre uma fase no Modo Colapso (sessao=None começa uma partida nova)."""
        from .colapso import SessaoColapso
        from .telas.bancada import Bancada
        from .telas.carta import Carta
        sessao = sessao or SessaoColapso()
        nova = porta_nova(id_fase)
        if nova and nova not in self.progresso.portas_vistas:
            self.ir(Carta(self, nova, id_fase, colapso=sessao))
        else:
            self.ir(Bancada(self, id_fase, colapso=sessao))

    def alternar_som(self):
        self.progresso.som = self.audio.alternar()
        self.progresso.salvar()

    def sair(self):
        self.rodando = False

    # --------------------------------------------------------------- laço ---
    def passo(self, dt: float, eventos=None):
        """Um quadro do jogo: eventos → atualização → desenho."""
        for e in pygame.event.get() if eventos is None else eventos:
            if e.type == pygame.QUIT:
                self.sair()
            elif e.type == pygame.KEYDOWN and e.key == pygame.K_m:
                self.alternar_som()
            else:
                self.atual.evento(e)
        self.t += dt
        self.particulas.atualizar(dt)
        self.atual.atualizar(dt)
        self.janela.fill(E.FUNDO)
        if self.atual.__class__.__name__ != "Menu":
            self.particulas.desenhar(self.janela, self.t)
        self.atual.desenhar(self.janela)
        pygame.display.flip()

    def rodar(self, quadros_teste=None):
        quadro = 0
        while self.rodando:
            dt = self.relogio.tick(FPS) / 1000
            self.passo(dt)
            quadro += 1
            if quadros_teste is not None and quadro >= quadros_teste:
                break
        pygame.quit()


def executar(quadros_teste=None):
    """Abre o jogo. Com `quadros_teste`, roda só essa quantidade de quadros e fecha."""
    App().rodar(quadros_teste)
