# Glossário do Qubit Lab

As portas quânticas do jogo, na ordem em que aparecem nas fases, e os conceitos principais.
No jogo, o glossário abre pelo menu ou pelo botão do livro na bancada (tecla `G`).

> Gerado por `ferramentas/gerar_glossario.py` a partir de `qubit_lab/textos.py`.

## Portas

| Porta | Nome | Qubits | Resumo | Fase |
|:---:|---|:---:|---|:---:|
| [**X**](#pauli-x) | Pauli-X | 1 | Inverte o qubit: \|0⟩ vira \|1⟩ e \|1⟩ vira \|0⟩. | 1 |
| [**H**](#hadamard) | Hadamard | 1 | Leva \|0⟩ a (\|0⟩ + \|1⟩)/√2 e \|1⟩ a (\|0⟩ − \|1⟩)/√2. | 2 |
| [**Z**](#pauli-z) | Pauli-Z | 1 | Troca o sinal da amplitude de \|1⟩: α\|0⟩ + β\|1⟩ vira α\|0⟩ − β\|1⟩. | 4 |
| [**CNOT**](#cnot) | CNOT | 2 | Se o controle for 1, inverte o alvo. | 6 |
| [**S**](#fase-s) | Fase S | 1 | Multiplica a amplitude de \|1⟩ por i. | 8 |
| [**T**](#fase-t) | Fase T | 1 | Multiplica a amplitude de \|1⟩ por e^(iπ/4). | 11 |
| [**CCX**](#toffoli) | Toffoli | 3 | Se os dois controles forem 1, inverte o alvo. | 15 |
| [**CZ**](#cz) | CZ | 2 | Inverte a fase só de \|11⟩. | 19 |
| [**Y**](#pauli-y) | Pauli-Y | 1 | Troca \|0⟩ e \|1⟩ e ainda ajusta a fase: \|0⟩ vira i\|1⟩ e \|1⟩ vira −i\|0⟩. | 21 |
| [**S†**](#fase-s†) | Fase S† | 1 | Multiplica a amplitude de \|1⟩ por −i: a S ao contrário. | 22 |
| [**T†**](#fase-t†) | Fase T† | 1 | Multiplica a amplitude de \|1⟩ por e^(−iπ/4): a T ao contrário. | 23 |
| [**√X**](#raiz-de-x) | Raiz de X | 1 | Um quarto de volta em torno do eixo x: duas √X formam um X. | 26 |
| [**SWAP**](#swap) | SWAP | 2 | Troca o estado de dois qubits. | 31 |
| [**iSWAP**](#iswap) | iSWAP | 2 | Troca dois qubits e dá um i de fase quando eles são diferentes. | 33 |
| [**CSWAP**](#fredkin) | Fredkin | 3 | Se o controle for 1, troca os outros dois qubits. | 35 |
| [**CY**](#cy) | CY | 2 | Se o controle for 1, aplica Y no alvo. | 36 |
| [**CH**](#ch) | CH | 2 | Se o controle for 1, aplica H no alvo. | 37 |
| [**CCZ**](#ccz) | CCZ | 3 | Inverte a fase só de \|111⟩. | 39 |
| [**Rx(π/2)**](#rotação-x) | Rotação X | 1 | Um quarto de volta em torno do eixo x. | 41 |
| [**Ry(π/2)**](#rotação-y) | Rotação Y | 1 | Um quarto de volta em torno do eixo y. | 42 |
| [**Rz(π/2)**](#rotação-z) | Rotação Z | 1 | Um quarto de volta em torno do eixo z. | 43 |
| [**P(π/2)**](#fase-p) | Fase P | 1 | Multiplica a amplitude de \|1⟩ por e^(iθ); no jogo, θ = π/2. | 44 |
| [**CP(π/2)**](#fase-controlada) | Fase controlada | 2 | Se os dois qubits forem 1, multiplica a amplitude por i. | 46 |
| [**CRz(π/2)**](#rz-controlada) | Rz controlada | 2 | Se o controle for 1, aplica Rz(π/2) no alvo. | 47 |
| [**CRx(π/2)**](#rx-controlada) | Rx controlada | 2 | Se o controle for 1, aplica Rx(π/2) no alvo. | 49 |
| [**CRy(π/2)**](#ry-controlada) | Ry controlada | 2 | Se o controle for 1, aplica Ry(π/2) no alvo. | 50 |
| [**Rxx(π/2)**](#ising-xx) | Ising XX | 2 | Gira os dois qubits ao mesmo tempo em torno de X⊗X. | 51 |
| [**Ryy(π/2)**](#ising-yy) | Ising YY | 2 | Gira os dois qubits ao mesmo tempo em torno de Y⊗Y. | 52 |
| [**Rzz(π/2)**](#ising-zz) | Ising ZZ | 2 | Dá fases opostas a qubits iguais e diferentes. | 53 |
| [**√SWAP**](#raiz-de-swap) | Raiz de SWAP | 2 | Metade de uma SWAP: duas formam uma troca completa. | 58 |
| [**U(π/2,0,π)**](#porta-u) | Porta U | 1 | A porta geral de um qubit, aqui com os ângulos (π/2, 0, π). | 63 |
| [**U(π,0,π)**](#porta-u) | Porta U | 1 | A porta geral de um qubit, aqui com os ângulos (π, 0, π). | 64 |
| [**U(0,0,π/2)**](#porta-u) | Porta U | 1 | A porta geral de um qubit, aqui com os ângulos (0, 0, π/2). | 65 |
| [**CU(π,0,π)**](#u-controlada) | U controlada | 2 | Se o controle for 1, aplica U(π, 0, π) no alvo. | 66 |
| [**CU(π/2,0,π)**](#u-controlada) | U controlada | 2 | Se o controle for 1, aplica U(π/2, 0, π) no alvo. | 67 |
| [**I**](#identidade) | Identidade | 1 | Deixa o qubit exatamente como está. | 68 |
| [**MCX**](#x-multicontrolada) | X multicontrolada | 4 | Se todos os controles forem 1, inverte o alvo. | 69 |

### Pauli-X

**O NOT quântico.** Inverte o qubit: |0⟩ vira |1⟩ e |1⟩ vira |0⟩.

É o equivalente quântico da porta NOT da lógica clássica. Numa superposição, troca as amplitudes de |0⟩ e |1⟩ entre si: α|0⟩ + β|1⟩ vira β|0⟩ + α|1⟩.

**Na esfera de Bloch:** Meia volta (180°) em torno do eixo x. Os polos trocam de lugar.

$$
X = \begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix}
$$

| Entrada | Saída |
|---|---|
| `\|0⟩` | `\|1⟩` |
| `\|1⟩` | `\|0⟩` |

**Relações úteis:**

- X·X = I: aplicar duas vezes desfaz
- H·X·H = Z
- Também chamada de Pauli-X ou NOT

**No Qiskit:** `qc.x(0)`

### Hadamard

**Cria a superposição.** Leva |0⟩ a (|0⟩ + |1⟩)/√2 e |1⟩ a (|0⟩ − |1⟩)/√2.

Transforma cada estado da base numa mistura igual dos dois, com 50% de chance cada. H|0⟩ e H|1⟩ diferem só no sinal (a fase); por isso, aplicar a H de novo faz as amplitudes interferirem e o qubit volta ao estado inicial.

**Na esfera de Bloch:** Meia volta em torno do eixo diagonal entre x e z. O polo norte vai para o eixo x.

$$
H = \frac{1}{\sqrt{2}}\begin{pmatrix} 1 & 1 \\ 1 & -1 \end{pmatrix}
$$

| Entrada | Saída |
|---|---|
| `\|0⟩` | `(\|0⟩ + \|1⟩)/√2` |
| `\|1⟩` | `(\|0⟩ − \|1⟩)/√2` |

**Relações úteis:**

- H·H = I
- H·Z·H = X e H·X·H = Z: a H troca os eixos x e z
- Abre quase todo algoritmo quântico

**No Qiskit:** `qc.h(0)`

### Pauli-Z

**Inverte a fase.** Troca o sinal da amplitude de |1⟩: α|0⟩ + β|1⟩ vira α|0⟩ − β|1⟩.

Não muda as probabilidades: medir antes ou depois do Z dá as mesmas chances. Muda o sinal da amplitude de |1⟩, e esse sinal decide o resultado quando há interferência, por exemplo entre duas H.

**Na esfera de Bloch:** Meia volta em torno do eixo z. Os polos ficam parados; o equador gira 180°.

$$
Z = \begin{pmatrix} 1 & 0 \\ 0 & -1 \end{pmatrix}
$$

| Entrada | Saída |
|---|---|
| `\|0⟩` | `\|0⟩` |
| `\|1⟩` | `−\|1⟩` |

**Relações úteis:**

- Z·Z = I
- S·S = Z
- H·Z·H = X

**No Qiskit:** `qc.z(0)`

### CNOT

**O X condicional.** Se o controle for 1, inverte o alvo.

Age em dois qubits: o controle (bolinha) e o alvo (⊕). Com entradas clássicas, o alvo vira controle XOR alvo e o controle não muda. Com o controle em superposição, a CNOT emaranha os qubits: H seguida de CNOT gera o estado de Bell (|00⟩ + |11⟩)/√2.

**Na esfera de Bloch:** Ao emaranhar os qubits, o vetor de cada esfera encolhe até o centro.

$$
CNOT = \begin{pmatrix} 1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 0 & 1 \\ 0 & 0 & 1 & 0 \end{pmatrix}
$$

| Entrada | Saída |
|---|---|
| `\|00⟩` | `\|00⟩` |
| `\|01⟩` | `\|01⟩` |
| `\|10⟩` | `\|11⟩` |
| `\|11⟩` | `\|10⟩` |

**Relações úteis:**

- CNOT·CNOT = I
- Com H no alvo antes e depois, vira uma CZ
- Também chamada de CX

**No Qiskit:** `qc.cx(0, 1)`

### Fase S

**Um quarto de volta.** Multiplica a amplitude de |1⟩ por i.

Como o Z, não muda as probabilidades, só a fase de |1⟩, mas gira metade do que o Z gira: α|0⟩ + β|1⟩ vira α|0⟩ + iβ|1⟩.

**Na esfera de Bloch:** 90° em torno do eixo z: do eixo x, o qubit vai para o eixo y.

$$
S = \begin{pmatrix} 1 & 0 \\ 0 & i \end{pmatrix}
$$

| Entrada | Saída |
|---|---|
| `\|0⟩` | `\|0⟩` |
| `\|1⟩` | `i\|1⟩` |

**Relações úteis:**

- S·S = Z
- T·T = S
- Quatro S dão uma volta inteira: S·S·S·S = I

**No Qiskit:** `qc.s(0)`

### Fase T

**Um oitavo de volta.** Multiplica a amplitude de |1⟩ por e^(iπ/4).

O ajuste mais fino de fase do jogo. Junto com a H, forma um conjunto universal: combinando H e T, dá para chegar tão perto quanto se queira de qualquer porta de um qubit.

**Na esfera de Bloch:** 45° em torno do eixo z. Os polos não se mexem.

$$
T = \begin{pmatrix} 1 & 0 \\ 0 & e^{i\pi/4} \end{pmatrix}
$$

| Entrada | Saída |
|---|---|
| `\|0⟩` | `\|0⟩` |
| `\|1⟩` | `e^(iπ/4)\|1⟩` |

**Relações úteis:**

- T·T = S
- T·T·T·T = Z
- Quatro T são um Z; oito T, uma volta inteira

**No Qiskit:** `qc.t(0)`

### Toffoli

**O AND reversível.** Se os dois controles forem 1, inverte o alvo.

Uma CNOT com dois controles. Com o alvo em 0, ele vira o AND dos dois controles, e as entradas continuam lá. Por isso a Toffoli é o AND reversível: com ela dá para fazer qualquer conta clássica num computador quântico.

**Na esfera de Bloch:** Com um controle em superposição, o alvo se emaranha e o vetor dele encolhe.

$$
CCX = \begin{pmatrix} 1 & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 1 & 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 1 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 1 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 & 1 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 & 0 & 0 & 1 \\ 0 & 0 & 0 & 0 & 0 & 0 & 1 & 0 \end{pmatrix}
$$

| Entrada | Saída |
|---|---|
| `\|000⟩` | `\|000⟩` |
| `\|001⟩` | `\|001⟩` |
| `\|010⟩` | `\|010⟩` |
| `\|011⟩` | `\|011⟩` |
| `\|100⟩` | `\|100⟩` |
| `\|101⟩` | `\|101⟩` |
| `\|110⟩` | `\|111⟩` |
| `\|111⟩` | `\|110⟩` |

**Relações úteis:**

- Toffoli·Toffoli = I
- Universal para a computação clássica reversível
- Também chamada de CCX ou CCNOT

**No Qiskit:** `qc.ccx(0, 1, 2)`

### CZ

**A fase condicional.** Inverte a fase só de |11⟩.

Se os dois qubits forem 1, a amplitude ganha um sinal de menos; nos outros casos, nada muda. É simétrica: não importa qual qubit é o controle. Não muda probabilidades, mas a marca aparece na interferência. É o oráculo da busca de Grover (fase 19).

**Na esfera de Bloch:** Com os dois qubits em |+⟩, a CZ os emaranha e os dois vetores somem no centro.

$$
CZ = \begin{pmatrix} 1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & -1 \end{pmatrix}
$$

| Entrada | Saída |
|---|---|
| `\|00⟩` | `\|00⟩` |
| `\|01⟩` | `\|01⟩` |
| `\|10⟩` | `\|10⟩` |
| `\|11⟩` | `−\|11⟩` |

**Relações úteis:**

- CZ·CZ = I
- É um Z controlado
- Com H no alvo antes e depois, vira uma CNOT

**No Qiskit:** `qc.cz(0, 1)`

### Pauli-Y

**O giro que faltava.** Troca |0⟩ e |1⟩ e ainda ajusta a fase: |0⟩ vira i|1⟩ e |1⟩ vira −i|0⟩.

É a terceira porta de Pauli, junto com X e Z. Como o X, inverte as probabilidades de 0 e 1; como o Z, troca |+⟩ e |−⟩. Na prática, o Y faz o trabalho dos dois de uma vez: Y = i·X·Z.

**Na esfera de Bloch:** Meia volta em torno do eixo y. Polos trocam de lugar e o eixo x se inverte.

$$
Y = \begin{pmatrix} 0 & -i \\ i & 0 \end{pmatrix}
$$

| Entrada | Saída |
|---|---|
| `\|0⟩` | `i\|1⟩` |
| `\|1⟩` | `−i\|0⟩` |

**Relações úteis:**

- Y·Y = I
- Y = i·X·Z
- H·Y·H = −Y: entre duas H, o Y continua um Y

**No Qiskit:** `qc.y(0)`

### Fase S†

**A S ao contrário.** Multiplica a amplitude de |1⟩ por −i: a S ao contrário.

A S† (S conjugada, ou S-adaga) é a inversa da S: gira a fase um quarto de volta no sentido negativo. α|0⟩ + β|1⟩ vira α|0⟩ − iβ|1⟩. Toda porta quântica tem uma inversa, e o † é o símbolo dela.

**Na esfera de Bloch:** 90° em torno do eixo z, no sentido contrário ao da S: do eixo x para o −y.

$$
S^\dagger = \begin{pmatrix} 1 & 0 \\ 0 & -i \end{pmatrix}
$$

| Entrada | Saída |
|---|---|
| `\|0⟩` | `\|0⟩` |
| `\|1⟩` | `−i\|1⟩` |

**Relações úteis:**

- S·S† = I: uma desfaz a outra
- S† = S·S·S
- T†·T† = S†

**No Qiskit:** `qc.sdg(0)`

### Fase T†

**A T ao contrário.** Multiplica a amplitude de |1⟩ por e^(−iπ/4): a T ao contrário.

A T† é a inversa da T: um oitavo de volta de fase no sentido negativo. Junto com H, T e CNOT, ela aparece em quase toda receita de circuito em computadores quânticos reais.

**Na esfera de Bloch:** 45° em torno do eixo z, no sentido contrário ao da T.

$$
T^\dagger = \begin{pmatrix} 1 & 0 \\ 0 & e^{-i\pi/4} \end{pmatrix}
$$

| Entrada | Saída |
|---|---|
| `\|0⟩` | `\|0⟩` |
| `\|1⟩` | `e^(−iπ/4)\|1⟩` |

**Relações úteis:**

- T·T† = I
- T†·T† = S†
- Oito T† dão uma volta inteira

**No Qiskit:** `qc.tdg(0)`

### Raiz de X

**Meio NOT.** Um quarto de volta em torno do eixo x: duas √X formam um X.

Leva |0⟩ a (|0⟩ − i|1⟩)/√2, a menos de uma fase global: 50% de chance para cada resultado, como a H, mas num ponto diferente do equador. É uma das portas nativas de computadores quânticos reais, como os da IBM.

**Na esfera de Bloch:** 90° em torno do eixo x. Do polo norte, o qubit vai para o lado negativo do eixo y.

$$
\sqrt{X} = \frac{1}{2}\begin{pmatrix} 1 + i & 1 - i \\ 1 - i & 1 + i \end{pmatrix}
$$

| Entrada | Saída |
|---|---|
| `\|0⟩` | `e^(iπ/4)(\|0⟩ − i\|1⟩)/√2` |
| `\|1⟩` | `e^(−iπ/4)(\|0⟩ + i\|1⟩)/√2` |

**Relações úteis:**

- √X·√X = X
- H·S·H = √X (a menos de uma fase global)
- Quatro √X dão uma volta inteira

**No Qiskit:** `qc.sx(0)`

### SWAP

**A troca de lugar.** Troca o estado de dois qubits.

|01⟩ vira |10⟩ e |10⟩ vira |01⟩; |00⟩ e |11⟩ ficam como estão. Como é uma porta quântica, troca o estado inteiro, com superposição e fase. Em chips reais, só qubits vizinhos conversam, e a SWAP é usada para levar um qubit até o outro.

**Na esfera de Bloch:** Os dois vetores trocam de esfera. No meio do caminho, eles encolhem.

$$
SWAP = \begin{pmatrix} 1 & 0 & 0 & 0 \\ 0 & 0 & 1 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 0 & 1 \end{pmatrix}
$$

| Entrada | Saída |
|---|---|
| `\|00⟩` | `\|00⟩` |
| `\|01⟩` | `\|10⟩` |
| `\|10⟩` | `\|01⟩` |
| `\|11⟩` | `\|11⟩` |

**Relações úteis:**

- SWAP·SWAP = I
- Três CNOTs alternando o controle formam uma SWAP
- É simétrica: tanto faz qual qubit vem primeiro

**No Qiskit:** `qc.swap(0, 1)`

### iSWAP

**A troca com fase.** Troca dois qubits e dá um i de fase quando eles são diferentes.

|01⟩ vira i|10⟩ e |10⟩ vira i|01⟩; |00⟩ e |11⟩ não mudam. Com entradas da base, o i é só uma fase global e o resultado parece uma SWAP. Com superposição, a fase aparece: |+⟩|0⟩ vira |0⟩|+i⟩.

**Na esfera de Bloch:** Os vetores trocam de esfera e o que chega gira um quarto de volta em z.

$$
iSWAP = \begin{pmatrix} 1 & 0 & 0 & 0 \\ 0 & 0 & i & 0 \\ 0 & i & 0 & 0 \\ 0 & 0 & 0 & 1 \end{pmatrix}
$$

| Entrada | Saída |
|---|---|
| `\|00⟩` | `\|00⟩` |
| `\|01⟩` | `i\|10⟩` |
| `\|10⟩` | `i\|01⟩` |
| `\|11⟩` | `\|11⟩` |

**Relações úteis:**

- iSWAP = SWAP + CZ + S nos dois qubits
- iSWAP·iSWAP = Z⊗Z, não a identidade
- Quatro iSWAP dão a identidade

**No Qiskit:** `qc.iswap(0, 1)`

### Fredkin

**A troca com chave.** Se o controle for 1, troca os outros dois qubits.

Também chamada de porta de Fredkin. O primeiro qubit é o controle; os outros dois só trocam de lugar se ele for 1. Assim como a Toffoli, é universal para a computação clássica reversível, e a quantidade de 1s nunca muda.

**Na esfera de Bloch:** Com o controle em superposição, os três qubits se emaranham.

$$
CSWAP = \begin{pmatrix} 1 & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 1 & 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 1 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 1 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & 0 & 0 & 1 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 & 0 & 0 & 1 \end{pmatrix}
$$

| Entrada | Saída |
|---|---|
| `\|000⟩` | `\|000⟩` |
| `\|001⟩` | `\|001⟩` |
| `\|010⟩` | `\|010⟩` |
| `\|011⟩` | `\|011⟩` |
| `\|100⟩` | `\|100⟩` |
| `\|101⟩` | `\|110⟩` |
| `\|110⟩` | `\|101⟩` |
| `\|111⟩` | `\|111⟩` |

**Relações úteis:**

- CSWAP·CSWAP = I
- É uma SWAP controlada
- Mantém o número de 1s: |101⟩ vira |110⟩

**No Qiskit:** `qc.cswap(0, 1, 2)`

### CY

**O Y com interruptor.** Se o controle for 1, aplica Y no alvo.

Uma porta controlada genérica: bolinha no controle, caixa com a letra no alvo. Com o controle em 0, nada muda; em 1, o alvo recebe um Y: |10⟩ vira i|11⟩ e |11⟩ vira −i|10⟩. Com o controle em |+⟩, gera o Bell com fase (|00⟩ + i|11⟩)/√2.

**Na esfera de Bloch:** Com o controle em |+⟩, os dois qubits se emaranham e os vetores encolhem.

$$
CY = \begin{pmatrix} 1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 0 & -i \\ 0 & 0 & i & 0 \end{pmatrix}
$$

| Entrada | Saída |
|---|---|
| `\|00⟩` | `\|00⟩` |
| `\|01⟩` | `\|01⟩` |
| `\|10⟩` | `i\|11⟩` |
| `\|11⟩` | `−i\|10⟩` |

**Relações úteis:**

- CY·CY = I
- S† no alvo, CNOT, S no alvo = CY
- É um Y controlado

**No Qiskit:** `qc.cy(0, 1)`

### CH

**Superposição sob condição.** Se o controle for 1, aplica H no alvo.

Com o controle em 1, o alvo entra em superposição; com 0, nada acontece. Com o controle em |+⟩ e o alvo em |0⟩, o resultado é |00⟩/√2 + |10⟩/2 + |11⟩/2: probabilidades de 50%, 25% e 25%. É um jeito de criar superposições desiguais.

**Na esfera de Bloch:** Com o controle em |+⟩, o alvo vai só até o meio do caminho: emaranhamento parcial.

$$
CH = \begin{pmatrix} 1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & \tfrac{1}{\sqrt{2}} & \tfrac{1}{\sqrt{2}} \\ 0 & 0 & \tfrac{1}{\sqrt{2}} & -\tfrac{1}{\sqrt{2}} \end{pmatrix}
$$

| Entrada | Saída |
|---|---|
| `\|00⟩` | `\|00⟩` |
| `\|01⟩` | `\|01⟩` |
| `\|10⟩` | `(\|10⟩ + \|11⟩)/√2` |
| `\|11⟩` | `(\|10⟩ − \|11⟩)/√2` |

**Relações úteis:**

- CH·CH = I
- É um H controlado
- Probabilidades desiguais: 50%, 25%, 25%

**No Qiskit:** `qc.ch(0, 1)`

### CCZ

**A marca para três.** Inverte a fase só de |111⟩.

A CZ com dois controles. Só o |111⟩ ganha um sinal de menos, e por isso ela é simétrica: os três fios ganham uma bolinha, sem caixa. Não muda probabilidades sozinha, mas é o oráculo da busca de Grover com 3 qubits.

**Na esfera de Bloch:** Com os três qubits em |+⟩, eles se emaranham e os vetores encolhem.

$$
CCZ = \begin{pmatrix} 1 & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 1 & 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 1 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 1 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 & 1 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & 0 & 0 & 0 & 0 & -1 \end{pmatrix}
$$

| Entrada | Saída |
|---|---|
| `\|000⟩` | `\|000⟩` |
| `\|001⟩` | `\|001⟩` |
| `\|010⟩` | `\|010⟩` |
| `\|011⟩` | `\|011⟩` |
| `\|100⟩` | `\|100⟩` |
| `\|101⟩` | `\|101⟩` |
| `\|110⟩` | `\|110⟩` |
| `\|111⟩` | `−\|111⟩` |

**Relações úteis:**

- CCZ·CCZ = I
- H no alvo, CCZ, H no alvo = Toffoli
- Simétrica: tanto faz qual qubit é o alvo

**No Qiskit:** `qc.ccz(0, 1, 2)`

### Rotação X

**O giro com ângulo.** Um quarto de volta em torno do eixo x.

Rx(θ) gira o vetor θ radianos em torno do eixo x; no jogo, θ = π/2. Leva |0⟩ a (|0⟩ − i|1⟩)/√2, como a √X. As rotações são o jeito mais comum de descrever portas em computadores reais: o ângulo é ajustado por um pulso de micro-ondas.

**Na esfera de Bloch:** 90° em torno do eixo x: do polo norte para o lado negativo do eixo y.

$$
R_{x}(\pi/2) = \frac{1}{\sqrt{2}}\begin{pmatrix} 1 & -i \\ -i & 1 \end{pmatrix}
$$

| Entrada | Saída |
|---|---|
| `\|0⟩` | `(\|0⟩ − i\|1⟩)/√2` |
| `\|1⟩` | `−i(\|0⟩ + i\|1⟩)/√2` |

**Relações úteis:**

- Rx(π/2) = √X, a menos de uma fase global
- Duas Rx(π/2) = X, a menos de fase
- Quatro Rx(π/2) = −I: uma volta inteira troca o sinal

**No Qiskit:** `qc.rx(pi / 2, 0)`

### Rotação Y

**O giro sem números complexos.** Um quarto de volta em torno do eixo y.

Ry(θ) gira o vetor θ radianos em torno do eixo y; no jogo, θ = π/2. A matriz só tem números reais. Leva |0⟩ a |+⟩ e |+⟩ a |1⟩: é o giro mais simples para criar superposições sem fase complexa.

**Na esfera de Bloch:** 90° em torno do eixo y: do polo norte para o eixo x.

$$
R_{y}(\pi/2) = \frac{1}{\sqrt{2}}\begin{pmatrix} 1 & -1 \\ 1 & 1 \end{pmatrix}
$$

| Entrada | Saída |
|---|---|
| `\|0⟩` | `(\|0⟩ + \|1⟩)/√2` |
| `\|1⟩` | `−(\|0⟩ − \|1⟩)/√2` |

**Relações úteis:**

- Z, depois Ry(π/2) = H
- Duas Ry(π/2) = Y, a menos de uma fase global
- Quatro Ry(π/2) = −I

**No Qiskit:** `qc.ry(pi / 2, 0)`

### Rotação Z

**A S com fase global.** Um quarto de volta em torno do eixo z.

Rz(θ) gira θ radianos em torno do eixo z; no jogo, θ = π/2. Multiplica |0⟩ por e^(−iπ/4) e |1⟩ por e^(iπ/4). Como a fase relativa é i, faz o mesmo que a S, a menos de uma fase global.

**Na esfera de Bloch:** 90° em torno do eixo z: |+⟩ vai para |+i⟩. Os polos não se mexem.

$$
R_{z}(\pi/2) = \begin{pmatrix} e^{-i\pi/4} & 0 \\ 0 & e^{i\pi/4} \end{pmatrix}
$$

| Entrada | Saída |
|---|---|
| `\|0⟩` | `e^(−iπ/4)\|0⟩` |
| `\|1⟩` | `e^(iπ/4)\|1⟩` |

**Relações úteis:**

- Rz(π/2) = S, a menos de uma fase global
- H, Rz(π/2), H = Rx(π/2)
- Quatro Rz(π/2) = −I

**No Qiskit:** `qc.rz(pi / 2, 0)`

### Fase P

**A família da fase.** Multiplica a amplitude de |1⟩ por e^(iθ); no jogo, θ = π/2.

A porta de fase. Não toca no |0⟩ e gira a fase de |1⟩ pelo ângulo θ. Com θ = π/2 é exatamente a S. Ela reúne numa família só várias portas do jogo: Z, S e T são P(π), P(π/2) e P(π/4).

**Na esfera de Bloch:** 90° em torno do eixo z, igual à S.

$$
P(\pi/2) = \begin{pmatrix} 1 & 0 \\ 0 & i \end{pmatrix}
$$

| Entrada | Saída |
|---|---|
| `\|0⟩` | `\|0⟩` |
| `\|1⟩` | `i\|1⟩` |

**Relações úteis:**

- P(π/2) = S, P(π/4) = T, P(π) = Z
- Duas P(π/2) = Z
- Rz(θ) = P(θ) vezes a fase global e^(−iθ/2)

**No Qiskit:** `qc.p(pi / 2, 0)`

### Fase controlada

**A S controlada.** Se os dois qubits forem 1, multiplica a amplitude por i.

A P(π/2) controlada, ou seja, a S controlada. Só o |11⟩ muda: ganha um i. Como a CZ, é simétrica. Fases controladas como essa são a peça principal da transformada de Fourier quântica, usada no algoritmo de Shor.

**Na esfera de Bloch:** Com os dois qubits em |+⟩, eles se emaranham e os vetores encolhem.

$$
CP(\pi/2) = \begin{pmatrix} 1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & i \end{pmatrix}
$$

| Entrada | Saída |
|---|---|
| `\|00⟩` | `\|00⟩` |
| `\|01⟩` | `\|01⟩` |
| `\|10⟩` | `\|10⟩` |
| `\|11⟩` | `i\|11⟩` |

**Relações úteis:**

- Duas CP(π/2) = CZ
- CP(π/2) = CRz(π/2) seguida de T no controle
- Simétrica: tanto faz qual qubit é o controle

**No Qiskit:** `qc.cp(pi / 2, 0, 1)`

### Rz controlada

**Quando a fase global aparece.** Se o controle for 1, aplica Rz(π/2) no alvo.

Parece a CP, mas não é. Com o controle em 1, |10⟩ ganha e^(−iπ/4) e |11⟩ ganha e^(iπ/4). A fase global da Rz virou uma fase do controle: a diferença entre CRz e CP é uma T no qubit de controle.

**Na esfera de Bloch:** Com os dois qubits em |+⟩, eles se emaranham.

$$
CR_{z}(\pi/2) = \begin{pmatrix} 1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & e^{-i\pi/4} & 0 \\ 0 & 0 & 0 & e^{i\pi/4} \end{pmatrix}
$$

| Entrada | Saída |
|---|---|
| `\|00⟩` | `\|00⟩` |
| `\|01⟩` | `\|01⟩` |
| `\|10⟩` | `e^(−iπ/4)\|10⟩` |
| `\|11⟩` | `e^(iπ/4)\|11⟩` |

**Relações úteis:**

- CRz(π/2) seguida de T no controle = CP(π/2)
- Sozinhas, Rz e P são iguais; controladas, não
- Quatro CRz(π/2) = Z no controle

**No Qiskit:** `qc.crz(pi / 2, 0, 1)`

### Rx controlada

**Meio NOT condicional.** Se o controle for 1, aplica Rx(π/2) no alvo.

Com o controle em 1, o alvo gira um quarto de volta em torno do eixo x. Com o controle em |+⟩ e o alvo em |0⟩, as probabilidades ficam em 50%, 25% e 25%, com uma fase −i no |11⟩.

**Na esfera de Bloch:** Com o controle em |+⟩, o alvo vai até o meio do caminho.

$$
CR_{x}(\pi/2) = \begin{pmatrix} 1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & \tfrac{1}{\sqrt{2}} & -\tfrac{i}{\sqrt{2}} \\ 0 & 0 & -\tfrac{i}{\sqrt{2}} & \tfrac{1}{\sqrt{2}} \end{pmatrix}
$$

| Entrada | Saída |
|---|---|
| `\|00⟩` | `\|00⟩` |
| `\|01⟩` | `\|01⟩` |
| `\|10⟩` | `(\|10⟩ − i\|11⟩)/√2` |
| `\|11⟩` | `−i(\|10⟩ + i\|11⟩)/√2` |

**Relações úteis:**

- Duas CRx(π/2) = CNOT com S† no controle
- Quatro CRx(π/2) = Z no controle
- Controlada, a fase global vira local

**No Qiskit:** `qc.crx(pi / 2, 0, 1)`

### Ry controlada

**A Ry com interruptor.** Se o controle for 1, aplica Ry(π/2) no alvo.

Com o controle em 1, o alvo gira um quarto de volta em torno do eixo y. Com o alvo em |0⟩, o resultado é o mesmo da CH. Com o alvo em |1⟩, não: a H é um espelho e a Ry é um giro, e a diferença aparece no sinal.

**Na esfera de Bloch:** Com o controle em |+⟩, o alvo vai até o meio do caminho.

$$
CR_{y}(\pi/2) = \begin{pmatrix} 1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & \tfrac{1}{\sqrt{2}} & -\tfrac{1}{\sqrt{2}} \\ 0 & 0 & \tfrac{1}{\sqrt{2}} & \tfrac{1}{\sqrt{2}} \end{pmatrix}
$$

| Entrada | Saída |
|---|---|
| `\|00⟩` | `\|00⟩` |
| `\|01⟩` | `\|01⟩` |
| `\|10⟩` | `(\|10⟩ + \|11⟩)/√2` |
| `\|11⟩` | `−(\|10⟩ − \|11⟩)/√2` |

**Relações úteis:**

- Com o alvo em |0⟩, igual à CH
- Matriz só com números reais
- Quatro CRy(π/2) = Z no controle

**No Qiskit:** `qc.cry(pi / 2, 0, 1)`

### Ising XX

**Giro de dois qubits juntos.** Gira os dois qubits ao mesmo tempo em torno de X⊗X.

Rxx(θ) = e^(−iθ·X⊗X/2). Com θ = π/2, leva |00⟩ direto a um estado de Bell, numa porta só. É a porta nativa dos computadores de íons presos (Mølmer–Sørensen) e aparece em simulações do modelo de Ising.

**Na esfera de Bloch:** Partindo de |00⟩, os dois vetores encolhem juntos até o centro: emaranhamento.

$$
R_{xx}(\pi/2) = \frac{1}{\sqrt{2}}\begin{pmatrix} 1 & 0 & 0 & -i \\ 0 & 1 & -i & 0 \\ 0 & -i & 1 & 0 \\ -i & 0 & 0 & 1 \end{pmatrix}
$$

| Entrada | Saída |
|---|---|
| `\|00⟩` | `(\|00⟩ − i\|11⟩)/√2` |
| `\|01⟩` | `(\|01⟩ − i\|10⟩)/√2` |
| `\|10⟩` | `−i(\|01⟩ + i\|10⟩)/√2` |
| `\|11⟩` | `−i(\|00⟩ + i\|11⟩)/√2` |

**Relações úteis:**

- Rxx(π/2)|00⟩ = (|00⟩ − i|11⟩)/√2
- Rxx(π) = −i·X⊗X
- H nos dois qubits antes e depois: Rzz vira Rxx

**No Qiskit:** `qc.rxx(pi / 2, 0, 1)`

### Ising YY

**O giro YY.** Gira os dois qubits ao mesmo tempo em torno de Y⊗Y.

Ryy(θ) = e^(−iθ·Y⊗Y/2). Como a Rxx, cria um estado de Bell a partir de |00⟩, mas com o sinal da fase trocado. Junto com Rxx e Rzz, forma o trio de interações entre spins.

**Na esfera de Bloch:** Partindo de |00⟩, os dois vetores encolhem juntos até o centro.

$$
R_{yy}(\pi/2) = \frac{1}{\sqrt{2}}\begin{pmatrix} 1 & 0 & 0 & i \\ 0 & 1 & -i & 0 \\ 0 & -i & 1 & 0 \\ i & 0 & 0 & 1 \end{pmatrix}
$$

| Entrada | Saída |
|---|---|
| `\|00⟩` | `(\|00⟩ + i\|11⟩)/√2` |
| `\|01⟩` | `(\|01⟩ − i\|10⟩)/√2` |
| `\|10⟩` | `−i(\|01⟩ + i\|10⟩)/√2` |
| `\|11⟩` | `i(\|00⟩ − i\|11⟩)/√2` |

**Relações úteis:**

- Ryy(π/2)|00⟩ = (|00⟩ + i|11⟩)/√2
- Ryy(π) = −i·Y⊗Y
- Rxx(π/2) e Ryy(π/2) juntas = iSWAP†, a troca com −i

**No Qiskit:** `qc.ryy(pi / 2, 0, 1)`

### Ising ZZ

**A interação de Ising.** Dá fases opostas a qubits iguais e diferentes.

Rzz(θ) é diagonal: multiplica |00⟩ e |11⟩ por e^(−iθ/2), e |01⟩ e |10⟩ por e^(iθ/2). Não muda probabilidades, só fases. É a interação ZZ do modelo de Ising e a peça central do algoritmo de otimização QAOA.

**Na esfera de Bloch:** Com os dois qubits em |+⟩, eles se emaranham e os vetores encolhem.

$$
R_{zz}(\pi/2) = \begin{pmatrix} e^{-i\pi/4} & 0 & 0 & 0 \\ 0 & e^{i\pi/4} & 0 & 0 \\ 0 & 0 & e^{i\pi/4} & 0 \\ 0 & 0 & 0 & e^{-i\pi/4} \end{pmatrix}
$$

| Entrada | Saída |
|---|---|
| `\|00⟩` | `e^(−iπ/4)\|00⟩` |
| `\|01⟩` | `e^(iπ/4)\|01⟩` |
| `\|10⟩` | `e^(iπ/4)\|10⟩` |
| `\|11⟩` | `e^(−iπ/4)\|11⟩` |

**Relações úteis:**

- CNOT, Rz(θ) no alvo, CNOT = Rzz(θ)
- Rzz(π) = −i·Z⊗Z
- Diagonal: não muda probabilidades

**No Qiskit:** `qc.rzz(pi / 2, 0, 1)`

### Raiz de SWAP

**Meia troca.** Metade de uma SWAP: duas formam uma troca completa.

Assim como a √X é meio X, a √SWAP é meia troca. No meio do caminho, os qubits ficam emaranhados: |10⟩ vira uma superposição de |10⟩ e |01⟩. Com √SWAP e portas de um qubit dá para montar qualquer circuito. É natural em qubits de spin.

**Na esfera de Bloch:** Partindo de |10⟩, os dois vetores encolhem até o centro: os qubits se emaranham.

$$
\sqrt{\mathrm{SWAP}} = \begin{pmatrix} 1 & 0 & 0 & 0 \\ 0 & \tfrac{1+i}{2} & \tfrac{1-i}{2} & 0 \\ 0 & \tfrac{1-i}{2} & \tfrac{1+i}{2} & 0 \\ 0 & 0 & 0 & 1 \end{pmatrix}
$$

| Entrada | Saída |
|---|---|
| `\|00⟩` | `\|00⟩` |
| `\|01⟩` | `e^(iπ/4)(\|01⟩ − i\|10⟩)/√2` |
| `\|10⟩` | `e^(−iπ/4)(\|01⟩ + i\|10⟩)/√2` |
| `\|11⟩` | `\|11⟩` |

**Relações úteis:**

- √SWAP·√SWAP = SWAP
- √SWAP, Z no 1º qubit, √SWAP, S e S† = CZ
- Em |01⟩ e |10⟩, igual à Rxx(π/2); em |00⟩, não

**No Qiskit:** `qc.append(SwapGate().power(1 / 2), [0, 1])`

### Porta U

**A porta de três ângulos.** A porta geral de um qubit, aqui com os ângulos (π/2, 0, π).

U(θ, φ, λ) descreve qualquer porta de um qubit com três ângulos: θ diz o quanto o vetor se afasta do polo, e φ e λ ajustam as fases. Toda porta de um qubit do jogo é uma U com os ângulos certos. Com (π/2, 0, π), ela trabalha igual à H.

**Na esfera de Bloch:** Com U(π/2, 0, π), o polo norte vai para |+⟩, como na H.

$$
U(\pi/2,0,\pi) = \frac{1}{\sqrt{2}}\begin{pmatrix} 1 & 1 \\ 1 & -1 \end{pmatrix}
$$

| Entrada | Saída |
|---|---|
| `\|0⟩` | `(\|0⟩ + \|1⟩)/√2` |
| `\|1⟩` | `(\|0⟩ − \|1⟩)/√2` |

**Relações úteis:**

- U(π/2, 0, π) = H
- U(π, 0, π) = X e U(0, 0, π/2) = S
- U(θ, −π/2, π/2) = Rx(θ) e U(0, 0, λ) = P(λ)

**No Qiskit:** `qc.u(pi / 2, 0, pi, 0)`

### Porta U

**A mesma U, outros ângulos.** A porta geral de um qubit, aqui com os ângulos (π, 0, π).

A mesma porta U, com outros ângulos. Com θ = π, o vetor vai de um polo ao outro: é o X. A letra é a mesma da U(π/2, 0, π), mas os ângulos mudam tudo.

**Na esfera de Bloch:** Meia volta: do polo norte ao polo sul, como no X.

$$
U(\pi,0,\pi) = \begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix}
$$

| Entrada | Saída |
|---|---|
| `\|0⟩` | `\|1⟩` |
| `\|1⟩` | `\|0⟩` |

**Relações úteis:**

- U(π, 0, π) = X
- U(π, π/2, π/2) = Y
- U(π/2, 0, π) = H

**No Qiskit:** `qc.u(pi, 0, pi, 0)`

### Porta U

**A U que só gira a fase.** A porta geral de um qubit, aqui com os ângulos (0, 0, π/2).

Com θ = 0, a U não afasta o vetor do polo: só gira a fase de |1⟩ pelo ângulo λ. É a porta P(λ). Com λ = π/2, trabalha igual à S; com λ = π/4, à T; com λ = π, ao Z.

**Na esfera de Bloch:** Um quarto de volta em torno do eixo z, como na S.

$$
U(0,0,\pi/2) = \begin{pmatrix} 1 & 0 \\ 0 & i \end{pmatrix}
$$

| Entrada | Saída |
|---|---|
| `\|0⟩` | `\|0⟩` |
| `\|1⟩` | `i\|1⟩` |

**Relações úteis:**

- U(0, 0, π/2) = S
- U(0, 0, π/4) = T e U(0, 0, π) = Z
- U(0, 0, λ) = P(λ)

**No Qiskit:** `qc.u(0, 0, pi / 2, 0)`

### U controlada

**A controlada de três ângulos.** Se o controle for 1, aplica U(π, 0, π) no alvo.

Qualquer porta controlada de um alvo é uma CU com os ângulos certos. Com (π, 0, π), a U é um X, e a CU trabalha igual à CNOT. No Qiskit, a CU tem um quarto ângulo, γ, para a fase que o controle ganha.

**Na esfera de Bloch:** Com o controle em |+⟩, a CU(π, 0, π) emaranha os qubits, como a CNOT.

$$
CU(\pi,0,\pi) = \begin{pmatrix} 1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 0 & 1 \\ 0 & 0 & 1 & 0 \end{pmatrix}
$$

| Entrada | Saída |
|---|---|
| `\|00⟩` | `\|00⟩` |
| `\|01⟩` | `\|01⟩` |
| `\|10⟩` | `\|11⟩` |
| `\|11⟩` | `\|10⟩` |

**Relações úteis:**

- CU(π, 0, π) = CNOT
- CU(π/2, 0, π) = CH
- CU(π, π/2, π/2) = CY

**No Qiskit:** `qc.cu(pi, 0, pi, 0, 0, 1)`

### U controlada

**A mesma CU, outros ângulos.** Se o controle for 1, aplica U(π/2, 0, π) no alvo.

A mesma CU, com os ângulos (π/2, 0, π). A U dentro dela é uma H, então a CU trabalha igual à CH: com o controle em |+⟩ e o alvo em |0⟩, as probabilidades ficam em 50%, 25% e 25%.

**Na esfera de Bloch:** Com o controle em |+⟩, o alvo vai só até o meio do caminho: emaranhamento parcial.

$$
CU(\pi/2,0,\pi) = \begin{pmatrix} 1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & \tfrac{1}{\sqrt{2}} & \tfrac{1}{\sqrt{2}} \\ 0 & 0 & \tfrac{1}{\sqrt{2}} & -\tfrac{1}{\sqrt{2}} \end{pmatrix}
$$

| Entrada | Saída |
|---|---|
| `\|00⟩` | `\|00⟩` |
| `\|01⟩` | `\|01⟩` |
| `\|10⟩` | `(\|10⟩ + \|11⟩)/√2` |
| `\|11⟩` | `(\|10⟩ − \|11⟩)/√2` |

**Relações úteis:**

- CU(π/2, 0, π) = CH
- CU(π, 0, π) = CNOT
- Duas CU(π/2, 0, π) = I

**No Qiskit:** `qc.cu(pi / 2, 0, pi, 0, 0, 1)`

### Identidade

**A porta que não faz nada.** Deixa o qubit exatamente como está.

A identidade é a matriz que não muda nenhum estado. Parece inútil, mas aparece o tempo todo: é o que sobra quando uma porta encontra a sua inversa (X·X, H·H, S·S†), e nos computadores reais marca um intervalo em que o qubit só espera.

**Na esfera de Bloch:** Nada se mexe: o vetor fica onde estava.

$$
I = \begin{pmatrix} 1 & 0 \\ 0 & 1 \end{pmatrix}
$$

| Entrada | Saída |
|---|---|
| `\|0⟩` | `\|0⟩` |
| `\|1⟩` | `\|1⟩` |

**Relações úteis:**

- X·X = H·H = S·S† = I
- U(0, 0, 0) = I
- Rx(2π) = −I: igual à I a menos de fase global

**No Qiskit:** `qc.id(0)`

### X multicontrolada

**Muitos controles.** Se todos os controles forem 1, inverte o alvo.

A X multicontrolada generaliza a CNOT (1 controle) e a Toffoli (2 controles) para quantos controles se queira; o exemplo aqui tem 3. É o AND de muitas entradas, e aparece nos oráculos da busca de Grover com muitos qubits.

**Na esfera de Bloch:** Com um controle em |+⟩ e os outros em 1, o alvo se emaranha com ele.

A matriz é 16 × 16: a identidade, menos no canto de baixo, onde fica um X (troca `|1110⟩` e `|1111⟩`).

| Entrada | Saída |
|---|---|
| `\|1110⟩` | `\|1111⟩` |
| `\|1111⟩` | `\|1110⟩` |
| as outras 14 | não mudam |

**Relações úteis:**

- Com 1 controle é a CNOT; com 2, a Toffoli
- MCX·MCX = I
- Com H no alvo antes e depois, vira uma Z multicontrolada

**No Qiskit:** `qc.mcx([0, 1, 2], 3)`

## Conceitos

### Qubit

A unidade de informação quântica. Um bit clássico é 0 ou 1; um qubit pode estar em α|0⟩ + β|1⟩, onde α e β são números complexos chamados amplitudes, com |α|² + |β|² = 1. Ao medir, sai 0 com chance |α|² e 1 com chance |β|².

### Superposição

Quando α e β são os dois diferentes de zero, o qubit está em superposição: não é 0 nem 1 até ser medido. O exemplo mais comum é (|0⟩ + |1⟩)/√2, criado pela porta H, com 50% de chance para cada resultado.

### Fase

O sinal (ou, em geral, o ângulo complexo) de uma amplitude. (|0⟩ + |1⟩)/√2 e (|0⟩ − |1⟩)/√2 têm as mesmas probabilidades e diferem só na fase. Medir não revela a fase; a interferência revela. As portas Z, S e T mexem só na fase.

### Interferência

Amplitudes se somam como ondas: com o mesmo sinal se reforçam, com sinais opostos se cancelam. É o motor dos algoritmos quânticos: o circuito é montado para que as respostas erradas se cancelem e a certa se reforce. Exemplo: H seguida de H devolve |0⟩, porque as duas contribuições para |1⟩ se cancelam.

### Emaranhamento

Quando o estado de dois ou mais qubits não pode ser descrito qubit por qubit. No estado de Bell (|00⟩ + |11⟩)/√2, cada qubit sozinho é 50/50, mas os dois sempre dão o mesmo resultado. Na esfera de Bloch, o vetor de um qubit emaranhado encolhe.

### Medição

Ler o qubit. O resultado é sorteado com as probabilidades |α|² e |β|², e depois o estado colapsa para o resultado obtido: a superposição se perde. Por isso o Modo Colapso só deixa espiar uma vez.

### Esfera de Bloch

Um jeito de desenhar o estado de um qubit como um ponto numa esfera: |0⟩ no polo norte, |1⟩ no polo sul e as superposições iguais no equador. A altura dá as probabilidades, e o ângulo em volta do eixo z dá a fase. Toda porta de um qubit é uma rotação dessa esfera.

### Oráculo

Uma caixa-preta que calcula uma função f e escreve o resultado num qubit extra. Nos algoritmos, o oráculo é consultado com as entradas em superposição, todas de uma vez. Com o qubit extra em |−⟩, a resposta vira uma fase. Fases 18, 83, 84, 85 e 86.

### Retorno de fase

Quando o alvo de uma porta controlada está num estado que a porta não muda (só ganha um sinal ou uma fase), essa fase vai para o controle. É o truque por trás de Deutsch, Grover e da estimativa de fase. Fases 74, 89 e 90.

### Codificação superdensa

Com um par de Bell dividido, Alice manda dois bits clássicos enviando um qubit só: nada, X, Z ou X e Z viram 00, 01, 10 ou 11. Bob desfaz o par com CNOT e H e lê os dois bits. Fases 87 e 91.

### Transformada de Fourier quântica

A QFT leva cada número x a um estado em que as fases giram no ritmo de x. Com dois qubits: H, uma fase controlada de π/2, H e uma SWAP. É o coração do algoritmo de Shor. Fase 88.

### Estimativa de fase

Descobre quanto uma porta gira a fase de um autoestado dela: o controle em |+⟩, a porta controlada, e uma H (ou uma QFT inversa, com mais bits) para transformar a fase em bits medidos. Fases 89 e 90.

### Troca de emaranhamento

Dois pares de Bell, uma medição de Bell nos qubits do meio e correções: os qubits das pontas ficam emaranhados sem nunca terem interagido. É a base das redes quânticas de longa distância. Fase 92.
