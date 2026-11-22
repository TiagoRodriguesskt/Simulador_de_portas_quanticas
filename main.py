"""Ponto de entrada do Qubit Lab.

    python main.py             abre o jogo
    python main.py --liberar   abre com todas as fases liberadas (para testar; o progresso não muda)
    python main.py --teste     abre, desenha 30 quadros e fecha (checagem rápida)
"""

import os
import sys

if "--liberar" in sys.argv:
    os.environ["QUBIT_LAB_LIBERAR"] = "1"

from qubit_lab.app import executar  # noqa: E402

if __name__ == "__main__":
    executar(quadros_teste=30 if "--teste" in sys.argv else None)
