<div align="center">

# ⚛️ Qubit Lab

**Um jogo de quebra-cabeça sobre portas lógicas quânticas, feito em Python.**

Monte circuitos, gire qubits na esfera de Bloch, crie emaranhamento e ouça o estado quântico mudar.
Por trás de cada fase existe a matemática real: vetores de estado, matrizes unitárias e medição.

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![pygame-ce](https://img.shields.io/badge/pygame--ce-jogo-2ea44f)
![NumPy](https://img.shields.io/badge/NumPy-simulador-013243?logo=numpy&logoColor=white)
![Plataformas](https://img.shields.io/badge/execut%C3%A1vel-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)
![Fases](https://img.shields.io/badge/fases-100-blueviolet)
![Portas](https://img.shields.io/badge/portas-34-orange)

![Tela inicial do Qubit Lab](docs/screenshots/tela-inicial.png)

</div>

---

## Sumário

- [Sobre o projeto](#sobre-o-projeto)
- [Como se joga](#como-se-joga)
- [Recursos](#recursos)
- [As portas quânticas](#as-portas-quânticas)
- [A matemática por trás do jogo](#a-matemática-por-trás-do-jogo)
- [Executável para download](#executável-para-download)
- [Rodar pelo código-fonte](#rodar-pelo-código-fonte)
- [Estrutura do projeto](#estrutura-do-projeto)
- [Testes](#testes)
- [Roteiro](#roteiro)
- [Inspiração e créditos](#inspiração-e-créditos)
- [Autor](#autor)

---

## Sobre o projeto

O **Qubit Lab** é um laboratório criogênico em forma de jogo. Cada fase é uma bancada com fios de qubits, espaços para portas e um detector. O objetivo é colocar as portas certas para levar os qubits até o estado pedido, e o detector só acende quando o estado está correto.

Criei o projeto para estudar **computação quântica e física computacional** na prática. Todo o jogo roda em cima de um **simulador quântico escrito do zero com NumPy**: nada de caixa-preta, cada porta é uma matriz e cada jogada é uma multiplicação de matriz por vetor.

> Acredito que se aprende por repetição. Por isso o jogo tem **100 fases**, que começam com uma única porta X e terminam em algoritmos quânticos completos.

---

## Como se joga

1. **Escolha uma fase** no mapa do laboratório.
2. **Arraste as portas** da bandeja para os slots nos fios dos qubits.
3. **Rode o circuito** e veja a esfera de Bloch de cada qubit girar em tempo real, junto com o som.
4. **Acenda o detector**: se o estado final bater com o alvo, a fase está concluída.

Algumas fases trazem portas "distratoras" na bandeja, e as fases finais têm **orçamento de portas**: não basta chegar ao estado certo, é preciso chegar pelo caminho mais curto.

---

## Recursos

| | |
| --- | --- |
| 🔵 **Esfera de Bloch animada** | O estado de cada qubit é mostrado como um vetor na esfera, girando enquanto as portas atuam. |
| 🔊 **Som que é física** | O áudio é sintetizado a partir do próprio estado quântico com NumPy: superposição, fase e colapso têm som próprio. |
| 🃏 **Cartas de porta** | Cada porta nova vem numa carta colecionável com símbolo, matriz, analogia e a rotação na esfera. |
| 📖 **Glossário / Álbum** | Todas as cartas conquistadas ficam guardadas para rever quando quiser. |
| ❄️ **Modo Colapso** | Modo difícil liberado após a fase 10: as esferas ficam cobertas de gelo, você tem 3 vidas e só pode espiar (medir) uma vez, e medir colapsa o estado. |
| 💡 **Explicação de cada fase** | Depois de vencer, uma tela explica o que aconteceu com o estado, com a notação de Dirac. |
| 💻 **Executável multiplataforma** | Baixe e jogue no Windows, Linux ou macOS, sem instalar nada. |
| 🔄 **Sempre em evolução** | O jogo recebe atualizações com o tempo: novas fases, portas e melhorias. |

---

## As portas quânticas

O jogo tem **34 portas**, apresentadas aos poucos, capítulo por capítulo.

| Tipo | Portas |
| --- | --- |
| **1 qubit** | I, X, Y, Z, H, S, S†, T, T†, √X, Rx, Ry, Rz, P, U |
| **2 qubits** | CNOT, CY, CZ, CH, SWAP, iSWAP, √SWAP, CRx, CRy, CRz, CP, CU, Rxx, Ryy, Rzz |
| **3 ou mais qubits** | Toffoli, Fredkin, CCZ, MCX |

Entre os desafios estão o **estado de Bell**, o **estado GHZ**, o **algoritmo de Deutsch**, a **busca de Grover**, o **teleporte quântico** e uma introdução à **correção de erros**.

---

## A matemática por trás do jogo

Além do jogo, o repositório tem um **guia de estudo** que resolve cada porta na matemática e na física:

- **Fundamentos:** qubit, vetor de estado, notação de Dirac, unitariedade, esfera de Bloch, produto tensorial e evolução temporal $U = e^{-iHt}$.
- **Cada porta:** a matriz, a conta feita passo a passo, o que acontece na esfera de Bloch e como a porta é feita em laboratório.
- **Exercícios** com respostas.
- **Script de conferência** (`docs/estudo_portas/portas_conferir.py`) que verifica todas as contas do guia com NumPy.

Um exemplo do que o guia mostra, a porta Hadamard criando superposição:

$$
H|0\rangle = \frac{1}{\sqrt{2}}\begin{pmatrix} 1 & 1 \\ 1 & -1 \end{pmatrix}\begin{pmatrix} 1 \\ 0 \end{pmatrix} = \frac{|0\rangle + |1\rangle}{\sqrt{2}} = |+\rangle
$$

E o mesmo cálculo em Python:

```python
import numpy as np

ket0 = np.array([1, 0], dtype=complex)
H = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)

print(H @ ket0)   # [0.707+0.j  0.707+0.j]  ->  |+>
```

---

## Executável para download

O Qubit Lab é distribuído como **jogo executável**: não precisa instalar Python nem nada. Basta baixar o arquivo do seu sistema e jogar.

1. Acesse a página de **[Releases](https://github.com/TiagoRodriguesskt/Simulador_de_portas_quanticas/releases)**.
2. Baixe a versão mais recente para o seu sistema: **Windows**, **Linux** ou **macOS**.
3. Abra o arquivo e jogue.

Os executáveis dos três sistemas são gerados automaticamente pelo GitHub Actions a cada nova versão. Como o jogo recebe **atualizações frequentes**, volte à página de Releases de vez em quando para baixar a versão mais nova.

---

## Rodar pelo código-fonte

Para jogar, o mais simples é baixar o [executável](#executável-para-download). Este caminho é para quem quer estudar ou modificar o código.

Requisitos: **Python 3.10 ou mais recente** e **Git**.

### Linux / macOS

```bash
git clone https://github.com/TiagoRodriguesskt/Simulador_de_portas_quanticas.git
cd Simulador_de_portas_quanticas
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

### Windows (PowerShell)

```powershell
git clone https://github.com/TiagoRodriguesskt/Simulador_de_portas_quanticas.git
cd Simulador_de_portas_quanticas
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
```

**Modo de teste:** para abrir todas as fases sem alterar o progresso salvo, rode `python main.py --liberar`.

**Gerar o executável** do seu sistema a partir do código:

```bash
pip install -r requirements-dev.txt
python ferramentas/gerar_executavel.py
```

---

## Estrutura do projeto

```
Qubit_Lab/
├── main.py                  # ponto de entrada do jogo
├── qubit_lab/
│   ├── core/                # simulador quântico: portas, estado, circuito,
│   │                        # medição, esfera de Bloch, solver e validador
│   ├── telas/               # menu, seleção de fases, bancada, álbum...
│   ├── ui/                  # esfera de Bloch, estilo, widgets
│   └── ...                  # sons, progresso, Modo Colapso
├── docs/
│   ├── DESIGN.md            # identidade visual, paleta e tabela de sons
│   ├── estudo_portas/       # guia de estudo + script de conferência
│   └── screenshots/
├── ferramentas/             # geração de executável e CI
├── tests/                   # testes com pytest
├── requirements.txt         # para jogar
└── requirements-dev.txt     # para desenvolver (pytest, pyinstaller)
```

---

## Testes

O simulador, as fases e o guia de estudo são testados com **pytest**. Há testes que jogam todas as fases pela bancada e um **solver** que confere se cada fase tem solução e não tem atalhos.

```bash
pip install -r requirements-dev.txt
pytest
```

---

## Roteiro

- [x] Simulador quântico com NumPy
- [x] Bancada jogável com esfera de Bloch e som
- [x] 100 fases e 34 portas
- [x] Modo Colapso e Álbum de portas
- [x] Guia de estudo da matemática e da física de cada porta
- [x] Executáveis para Linux, Windows e macOS

O Qubit Lab é um **jogo executável**: você baixa, abre e joga, no Windows, no Linux ou no Mac. O jogo continua em desenvolvimento e **vai receber atualizações com o tempo**, com novas fases, portas, explicações e melhorias. Cada nova versão sai na página de [Releases](https://github.com/TiagoRodriguesskt/Simulador_de_portas_quanticas/releases).

---

## Inspiração e créditos

A ideia do Qubit Lab surgiu do jogo **[Portas Lógicas](https://github.com/tclaro/logicGates)**, de **[tclaro](https://github.com/tclaro)**, um jogo de navegador sobre portas lógicas clássicas (AND, OR, NOT...). Ele me fez pensar: e se as portas fossem quânticas?

O Qubit Lab é um projeto próprio, escrito do zero em Python, com outra proposta: portas quânticas, esfera de Bloch, som gerado pelo estado quântico e um simulador feito com NumPy. Mesmo assim, a faísca veio de lá. Fica aqui o meu agradecimento e a recomendação: vale muito a pena conhecer o jogo original.

---

## Autor

**Tiago Rodrigues** · estudante de Física, Matemática, Computação Quântica e Física Computacional.

[![GitHub](https://img.shields.io/badge/GitHub-TiagoRodriguesskt-181717?logo=github)](https://github.com/TiagoRodriguesskt)
[![Portfólio](https://img.shields.io/badge/Portf%C3%B3lio-tiagorodriguesskt.github.io-0A66C2)](https://tiagorodriguesskt.github.io)

<div align="center">

*Feito com Python, NumPy e muita curiosidade sobre o mundo quântico.* ⚛️

</div>
