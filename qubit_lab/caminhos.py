"""Caminhos de arquivos que funcionam em Linux, Windows e macOS.

Dois cuidados para o jogo rodar em qualquer sistema:
1. Nunca escrever caminhos com "/" ou "\\" na mão: usamos pathlib.Path.
2. Quando o jogo vira executável (PyInstaller), os arquivos ficam numa pasta
   temporária indicada por sys._MEIPASS, e não ao lado do código.
"""

import os
import sys
from pathlib import Path


def pasta_base() -> Path:
    """Raiz do projeto, tanto rodando com Python quanto como executável."""
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS)
    return Path(__file__).resolve().parent.parent


def recurso(*partes: str) -> Path:
    """Caminho de um arquivo em assets/, ex.: recurso("sons", "01_estado_0.wav")."""
    return pasta_base() / "assets" / Path(*partes)


def pasta_progresso() -> Path:
    """Onde o progresso do jogador é salvo (na pasta do usuário, em qualquer sistema).

    Linux/macOS: ~/.qubit_lab    Windows: C:\\Users\\<nome>\\.qubit_lab
    A variável de ambiente QUBIT_LAB_DADOS troca essa pasta (usada nos testes).
    """
    pasta = Path(os.environ.get("QUBIT_LAB_DADOS", Path.home() / ".qubit_lab"))
    pasta.mkdir(parents=True, exist_ok=True)
    return pasta
