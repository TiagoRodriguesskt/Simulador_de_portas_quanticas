"""Gera o executável do Qubit Lab para o sistema em que está rodando.

    pip install -r requirements-dev.txt
    python ferramentas/gerar_executavel.py

Resultado em dist/:
    Linux    dist/QubitLab            (arquivo único)
    Windows  dist/QubitLab.exe        (arquivo único)
    macOS    dist/QubitLab.app        (aplicativo)

Importante: o PyInstaller NÃO faz "compilação cruzada". Para ter o .exe do
Windows, rode este script num Windows; para o Mac, num Mac. O workflow em
ferramentas/ci/build-executaveis.yml faz os três de uma vez no GitHub.
"""

import os
import platform
import sys
from pathlib import Path

import PyInstaller.__main__

RAIZ = Path(__file__).resolve().parent.parent


def main():
    sistema = platform.system()          # "Linux", "Windows" ou "Darwin" (macOS)
    # --add-data usa ";" no Windows e ":" nos outros: os.pathsep resolve isso
    assets = f"{RAIZ / 'assets'}{os.pathsep}assets"

    argumentos = [
        str(RAIZ / "main.py"),
        "--name", "QubitLab",
        "--add-data", assets,
        "--windowed",                    # sem janela de terminal junto
        "--noconfirm",
        "--clean",
        "--distpath", str(RAIZ / "dist"),
        "--workpath", str(RAIZ / "build"),
        "--specpath", str(RAIZ / "build"),
    ]
    if sistema == "Darwin":
        argumentos.append("--onedir")    # no Mac o padrão é um QubitLab.app
    else:
        argumentos.append("--onefile")   # Linux e Windows: um arquivo só

    print(f"Gerando o executável para {sistema} ({platform.machine()})...")
    PyInstaller.__main__.run(argumentos)
    print("\nPronto! Veja a pasta dist/")


if __name__ == "__main__":
    sys.exit(main())
