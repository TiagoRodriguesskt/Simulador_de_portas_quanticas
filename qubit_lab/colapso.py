"""Modo Colapso: o estado fica escondido sob o gelo e cada erro queima uma vida.

Regras:
- Liberado depois de concluir a fase 10 no modo normal.
- A partida começa na fase 1 e segue em ordem.
- As esferas ficam cobertas de gelo: é preciso prever o resultado de cabeça.
- Uma vez por fase, dá para ESPIAR: o circuito roda e o qubit é medido UMA vez.
  Você vê um resultado sorteado, como num experimento real, e o estado colapsa.
- Ativar sem acender o detector queima uma das 3 vidas (e o gelo quebra,
  para você entender o que aconteceu).
- As vidas se renovam a cada fase vencida.
- Sem vidas, a partida recomeça do início do capítulo: a fase em que a
  última porta nova foi apresentada.
"""

from __future__ import annotations

from .core.capitulos import APRESENTACAO

VIDAS = 3
FASE_LIBERA = 10


def inicio_do_capitulo(id_fase: int) -> int:
    """A fase em que a porta mais recente (até `id_fase`) foi apresentada."""
    return max(f for f in APRESENTACAO.values() if f <= id_fase)


class SessaoColapso:
    def __init__(self):
        self.vidas = VIDAS

    def perder_vida(self) -> bool:
        """Queima uma vida; devolve True se ainda restam vidas."""
        self.vidas = max(0, self.vidas - 1)
        return self.vidas > 0

    def renovar(self):
        self.vidas = VIDAS
