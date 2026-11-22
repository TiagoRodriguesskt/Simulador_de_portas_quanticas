"""Áudio do Qubit Lab: sons prontos (assets/sons) e síntese do estado em tempo real."""

from __future__ import annotations

import pygame

from ..caminhos import recurso
from .sintese import para_int16, sintetizar

SONS = {
    "detector": "08_detector_acende.wav",
    "colapso": "06_colapso.wav",
    "ambiente": "09_ambiente_criostato.wav",
}


class Audio:
    """Toca os sons do jogo. Se o computador não tiver som, tudo vira silêncio."""

    def __init__(self, ligado: bool = True):
        self.ligado = ligado
        self.sons = {}
        self.sr = 44100
        self.disponivel = pygame.mixer.get_init() is not None
        if not self.disponivel:
            return
        self.sr, _, canais = pygame.mixer.get_init()
        self.estereo = canais == 2
        for chave, arquivo in SONS.items():
            try:
                self.sons[chave] = pygame.mixer.Sound(str(recurso("sons", arquivo)))
            except (pygame.error, FileNotFoundError):
                pass
        if "ambiente" in self.sons:
            self.sons["ambiente"].set_volume(0.3)
            self.sons["ambiente"].play(loops=-1)
        self._canal_estado = None
        self.aplicar_ligado()

    def aplicar_ligado(self):
        if not self.disponivel:
            return
        if self.ligado:
            pygame.mixer.unpause()
        else:
            pygame.mixer.pause()

    def alternar(self) -> bool:
        self.ligado = not self.ligado
        self.aplicar_ligado()
        return self.ligado

    def tocar(self, chave: str):
        if self.ligado and chave in self.sons:
            self.sons[chave].play()

    def parar_efeitos(self):
        """Para o som do circuito e os efeitos (detector, colapso); o ambiente continua.

        Chamado em toda troca de tela: o que tocava numa tela não segue tocando na outra.
        """
        if not self.disponivel:
            return
        if self._canal_estado:
            self._canal_estado.stop()
            self._canal_estado = None
        for chave, som in self.sons.items():
            if chave != "ambiente":
                som.stop()

    def tocar_estado(self, quadros, fps: float):
        """Sintetiza e toca o som da animação de um circuito."""
        if not (self.ligado and self.disponivel):
            return
        x = sintetizar(quadros, fps, self.sr)
        if not self.estereo:
            x = x.mean(axis=1)
        som = pygame.sndarray.make_sound(para_int16(x))
        if self._canal_estado:
            self._canal_estado.stop()
        self._canal_estado = som.play()
