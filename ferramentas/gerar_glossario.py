"""Gera docs/GLOSSARIO.md a partir dos mesmos textos do glossário do jogo.

    python ferramentas/gerar_glossario.py

Assim o glossário do jogo e o do repositório nunca ficam diferentes: para mudar
um texto, edite qubit_lab/textos.py e rode este script de novo.
"""

import cmath
import re
import sys
from pathlib import Path

import numpy as np

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

from qubit_lab.core import Estado, formatar  # noqa: E402
from qubit_lab.core.capitulos import APRESENTACAO  # noqa: E402
from qubit_lab.core.portas import porta, simbolo  # noqa: E402
from qubit_lab.textos import CONCEITOS, GLOSSARIO, OUTRAS_PORTAS, carta, entrada_glossario  # noqa: E402


def _entrada(z) -> str:
    """Um número da matriz em LaTeX."""
    for valor, txt in [(0, "0"), (1, "1"), (-1, "-1"), (1j, "i"), (-1j, "-i")]:
        if abs(z - valor) < 1e-9:
            return txt
    if abs(abs(z.real) - 0.5) < 1e-9 and abs(abs(z.imag) - 0.5) < 1e-9:  # √SWAP: (1 ± i)/2 sem fator comum
        return ("-" if z.real < 0 else "") + r"\tfrac{1" + ("+" if z.imag > 0 else "-") + "i}{2}"
    if abs(abs(z.real) - 1) < 1e-9 and abs(abs(z.imag) - 1) < 1e-9:      # 1 ± i (√X, depois do fator 1/2)
        return f"{'-' if z.real < 0 else ''}1 {'+' if z.imag > 0 else '-'} i"
    if abs(abs(z) - 2 ** -0.5) < 1e-9 and min(abs(z.real), abs(z.imag)) < 1e-9:   # CH, CRx: ±1/√2, ±i/√2
        u = _entrada(z * 2 ** 0.5)
        sinal, num = ("-", u[1:]) if u.startswith("-") else ("", u)
        return sinal + r"\tfrac{" + num + r"}{\sqrt{2}}"
    k = round(cmath.phase(z) / (cmath.pi / 4))
    return {1: r"e^{i\pi/4}", -1: r"e^{-i\pi/4}", 3: r"e^{3i\pi/4}", -3: r"e^{-3i\pi/4}"}[k]


def matriz_latex(nome: str) -> str:
    """A matriz da porta em LaTeX (o GitHub desenha fórmulas entre $$)."""
    m = porta(nome).matriz
    if len(m) > 8:                       # 16 × 16 (MCX): grande demais para escrever
        n = porta(nome).n_qubits
        return (f"A matriz é {len(m)} × {len(m)}: a identidade, menos no canto de baixo, onde fica um X "
                f"(troca `|{'1' * (n - 1)}0⟩` e `|{'1' * n}⟩`).")
    fator = ""
    if all(abs(abs(z.real) - 0.5) < 1e-9 and abs(abs(z.imag) - 0.5) < 1e-9 for z in m.ravel()):
        fator, m = r"\frac{1}{2}", m * 2
    elif abs(abs(m[0, 0]) - 2 ** -0.5) < 1e-9:
        fator, m = r"\frac{1}{\sqrt{2}}", m * 2 ** 0.5
    linhas = r" \\ ".join(" & ".join(_entrada(z) for z in linha) for linha in m)
    rotulo = simbolo(nome).replace("†", r"^\dagger").replace("√X", r"\sqrt{X}").replace("√SWAP", r"\sqrt{\mathrm{SWAP}}").replace("π", r"\pi")
    rotulo = re.sub(r"R([xyz]+)", r"R_{\1}", rotulo)                   # Rxx(π/2) → R_{xx}(\pi/2)
    return f"$$\n{rotulo} = {fator}\\begin{{pmatrix}} {linhas} \\end{{pmatrix}}\n$$"


def ancora(texto: str) -> str:
    return texto.lower().replace(" ", "-")


def secao_porta(nome: str) -> list[str]:
    """O texto de uma porta: resumo, matriz, tabela de entradas, relações e Qiskit."""
    p, g = porta(nome), entrada_glossario(nome)
    subtitulo = g.get("subtitulo") or carta(nome)["subtitulo"]
    md = [f"### {p.titulo}", "", f"**{subtitulo}.** {g['resumo']}", "",
          g["faz"], "", f"**Na esfera de Bloch:** {g['esfera']}", "", matriz_latex(nome), "",
          "| Entrada | Saída |", "|---|---|"]
    kets = [format(i, f"0{p.n_qubits}b") for i in range(2 ** p.n_qubits)]
    if p.n_qubits >= 4:                  # só as entradas que mudam
        kets = [k for k in kets if not np.allclose(Estado.da_base(k).aplicar(p, range(p.n_qubits)).vetor,
                                                   Estado.da_base(k).vetor)]
    for k in kets:
        saida = formatar(Estado.da_base(k).aplicar(p, range(p.n_qubits)).vetor, manter_fase=True)
        md.append(f"| `\\|{k}⟩` | `{saida.replace('|', chr(92) + '|')}` |")
    if p.n_qubits >= 4:
        md.append(f"| as outras {2 ** p.n_qubits - len(kets)} | não mudam |")
    md += ["", "**Relações úteis:**", ""] + [f"- {r}" for r in g["relacoes"]]
    md += ["", f"**No Qiskit:** `{g['qiskit']}`", ""]
    return md


def main():
    portas = sorted(GLOSSARIO, key=APRESENTACAO.get)
    resumo = lambda nome: entrada_glossario(nome)["resumo"].replace("|", chr(92) + "|")
    md = [
        "# Glossário do Qubit Lab",
        "",
        "As portas quânticas do jogo, na ordem em que aparecem nas fases, e os conceitos principais.",
        "No jogo, o glossário abre pelo menu ou pelo botão do livro na bancada (tecla `G`).",
        "",
        "> Gerado por `ferramentas/gerar_glossario.py` a partir de `qubit_lab/textos.py`.",
        "",
        "## Portas",
        "",
        "| Porta | Nome | Qubits | Resumo | Fase |",
        "|:---:|---|:---:|---|:---:|",
    ]
    for nome in portas:
        p = porta(nome)
        md.append(f"| [**{simbolo(nome)}**](#{ancora(p.titulo)}) | {p.titulo} | {p.n_qubits} | "
                  f"{resumo(nome)} | {APRESENTACAO[nome]} |")
    md.append("")
    for nome in portas:
        md += secao_porta(nome)

    if OUTRAS_PORTAS:                    # some quando todas as portas já estão nas fases
        md += ["## Outras portas", "",
               "Portas que não aparecem nas fases, mas são comuns em artigos e no Qiskit. Algumas têm ângulos;",
               "aqui elas aparecem com um exemplo de ângulo fixo.", "",
               "| Porta | Nome | Qubits | Resumo |", "|:---:|---|:---:|---|"]
        for nome in OUTRAS_PORTAS:
            p = porta(nome)
            md.append(f"| [**{simbolo(nome)}**](#{ancora(p.titulo)}) | {p.titulo} | {p.n_qubits} | {resumo(nome)} |")
        md.append("")
        for nome in OUTRAS_PORTAS:
            md += secao_porta(nome)

    md += ["## Conceitos", ""]
    for nome, texto in CONCEITOS.items():
        md += [f"### {nome}", "", texto, ""]

    destino = RAIZ / "docs" / "GLOSSARIO.md"
    destino.write_text("\n".join(md), encoding="utf-8")
    print(f"Gerado: {destino}")


if __name__ == "__main__":
    main()
