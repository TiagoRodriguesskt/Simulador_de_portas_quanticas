"""Testes básicos: os arquivos existem e o jogo abre sem erro (sem precisar de tela)."""

import os

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")   # roda sem monitor
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")   # roda sem placa de som

from qubit_lab.audio import SONS
from qubit_lab.caminhos import recurso
from qubit_lab.ui.estilo import _ARQUIVOS # type: ignore


def test_sons_existem():
    for arquivo in SONS.values():
        assert recurso("sons", arquivo).is_file(), f"faltando: {arquivo}"


def test_fontes_existem():
    for arquivo in _ARQUIVOS.values():
        assert recurso("fontes", arquivo).is_file(), f"faltando: {arquivo}"


def test_jogo_abre_e_fecha(tmp_path, monkeypatch): # type: ignore
    monkeypatch.setenv("QUBIT_LAB_DADOS", str(tmp_path)) # type: ignore
    from qubit_lab.app import executar # type: ignore
    executar(quadros_teste=10)
