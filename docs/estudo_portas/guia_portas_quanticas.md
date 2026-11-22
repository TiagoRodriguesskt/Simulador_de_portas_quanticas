# Qubit Lab — Guia de estudo: a matemática e a física de cada porta

Tiago Rodrigues · 21/11/2026

Toda porta quântica é uma matriz unitária que multiplica o vetor de estado, e, fisicamente, é uma evolução no tempo controlada do qubit. Este guia cobre as 34 portas do Qubit Lab. Para cada uma: a matriz, uma conta resolvida passo a passo, o que acontece na esfera de Bloch e como ela é feita num laboratório de verdade. Todas as contas foram conferidas com testes automáticos em NumPy (ver o fim do guia).

## Fundamentos: o que você precisa antes das portas

### 1. O qubit é um vetor

Um qubit é uma combinação de dois estados de base, |0⟩ e |1⟩. Os números α e β são as amplitudes, e podem ser complexos.

$$
|\psi\rangle = \alpha|0\rangle + \beta|1\rangle = \begin{pmatrix} \alpha \\ \beta \end{pmatrix}, \qquad |0\rangle = \begin{pmatrix} 1 \\ 0 \end{pmatrix}, \quad |1\rangle = \begin{pmatrix} 0 \\ 1 \end{pmatrix}
$$

Ao medir, a chance de dar 0 é |α|² e a de dar 1 é |β|² (regra de Born). Por isso sempre vale |α|² + |β|² = 1.

Seis estados aparecem o tempo todo no jogo:

| Estado | Vetor | Onde fica na esfera |
| --- | --- | --- |
| \|0⟩ | (1, 0) | polo norte (+z) |
| \|1⟩ | (0, 1) | polo sul (−z) |
| \|+⟩ | (1, 1)/√2 | equador, +x |
| \|−⟩ | (1, −1)/√2 | equador, −x |
| \|+i⟩ | (1, i)/√2 | equador, +y |
| \|−i⟩ | (1, −i)/√2 | equador, −y |

### 2. Aplicar uma porta é multiplicar matriz por vetor

A regra é sempre a mesma: linha da matriz vezes a coluna do vetor.

$$
\begin{pmatrix} a & b \\ c & d \end{pmatrix} \begin{pmatrix} \alpha \\ \beta \end{pmatrix} = \begin{pmatrix} a\alpha + b\beta \\ c\alpha + d\beta \end{pmatrix}
$$

Várias portas em sequência: a primeira aplicada fica mais à direita. Se o circuito é "primeiro A, depois B", a conta é B·A·|ψ⟩. Esse é o erro mais comum de iniciante.

### 3. Unitária: por que toda porta pode ser desfeita

Uma porta U é unitária quando U†U = I. U† é a transposta conjugada: troca linhas por colunas e troca i por −i. Duas consequências físicas:

- **A probabilidade total continua 1.** A porta gira o vetor, mas não muda o seu tamanho.
- **Toda porta é reversível.** U† desfaz U. Na física, isso vem de a evolução quântica não perder informação. A medição é a única coisa que não é reversível.

### 4. Fase global e fase relativa

Multiplicar o estado inteiro por e^{iγ} (fase global) não muda nada que se possa medir. Já a fase entre |0⟩ e |1⟩ (fase relativa) muda tudo: |+⟩ e |−⟩ só diferem nela e são estados opostos na esfera. Várias portas do guia são "iguais a menos de fase global", e isso deixa de ser verdade quando elas viram controladas (ver CP × CRz).

### 5. A esfera de Bloch

Ignorando a fase global, todo qubit pode ser escrito com dois ângulos:

$$
|\psi\rangle = \cos\frac{\theta}{2}|0\rangle + e^{i\varphi}\sin\frac{\theta}{2}|1\rangle \quad\Rightarrow\quad (x, y, z) = (\sin\theta\cos\varphi,\ \sin\theta\sin\varphi,\ \cos\theta)
$$

θ é a latitude (do norte ao sul) e φ é a longitude (a fase relativa). **Toda porta de 1 qubit é uma rotação dessa esfera**, em torno de algum eixo e por algum ângulo. É por isso que o jogo mostra o estado na esfera.

### 6. A física: de onde vem uma porta

Um sistema quântico evolui pela equação de Schrödinger. Se o Hamiltoniano H (a energia do sistema) fica ligado por um tempo t, o estado sofre a transformação U:

$$
i\hbar\frac{d}{dt}|\psi\rangle = H|\psi\rangle \quad\Rightarrow\quad U = e^{-iHt/\hbar}
$$

Fazer uma porta é escolher o H certo e ligá-lo pelo tempo certo. Para 1 qubit, H é uma combinação das matrizes de Pauli (X, Y, Z), e a evolução é uma rotação:

$$
R_{\hat n}(\theta) = e^{-i\frac{\theta}{2}(n_x X + n_y Y + n_z Z)} = \cos\frac{\theta}{2}\,I - i\sin\frac{\theta}{2}\,(n_x X + n_y Y + n_z Z)
$$

A imagem física clássica é um spin (um pequeno ímã) num campo magnético. O spin gira em torno do campo, o que se chama precessão de Larmor. O eixo do campo é o eixo de rotação, e a intensidade vezes o tempo dá o ângulo.

Como isso é feito em cada tecnologia:

- **Qubits supercondutores (IBM, Google).** Um pulso de micro-ondas na frequência do qubit gira o estado em torno de um eixo do equador. A fase do pulso escolhe o eixo (x ou y), e a duração escolhe o ângulo (oscilação de Rabi). Rotações em z são feitas "de graça", no software, mudando a referência de fase dos próximos pulsos ("Z virtual").
- **Íons presos (IonQ, Quantinuum).** Lasers fazem o mesmo papel das micro-ondas. As portas de 2 qubits usam a vibração coletiva dos íons.
- **Fótons.** O qubit pode ser a polarização da luz. Placas de onda e divisores de feixe são as portas.

### 7. Mais de um qubit: produto tensorial

Dois qubits vivem num vetor de 4 amplitudes, na ordem |00⟩, |01⟩, |10⟩, |11⟩. Neste guia o primeiro dígito é o primeiro qubit (controle) e o segundo é o alvo. Atenção: o Qiskit usa a ordem inversa (o qubit 0 é o dígito da direita).

$$
\begin{pmatrix} a \\ b \end{pmatrix} \otimes \begin{pmatrix} c \\ d \end{pmatrix} = \begin{pmatrix} ac \\ ad \\ bc \\ bd \end{pmatrix}
$$

Um estado que **não** pode ser escrito como um produto desses é **emaranhado**. A porta controlada mais geral tem uma fórmula só, que vale para CNOT, CY, CZ, CH e todas as outras:

$$
C(U) = |0\rangle\langle 0| \otimes I + |1\rangle\langle 1| \otimes U = \begin{pmatrix} I & 0 \\ 0 & U \end{pmatrix}
$$

Leitura: se o controle é 0, nada acontece no alvo; se é 1, aplica U. Num estado emaranhado, cada qubit sozinho não tem um ponto na superfície da esfera. O vetor de Bloch dele encolhe para dentro da esfera, e num estado de Bell vai até o centro.

## Portas de 1 qubit

Toda porta de 1 qubit é uma rotação da esfera de Bloch. Resumo antes dos detalhes:

| Porta | Eixo | Ângulo | O que faz com \|0⟩ ou \|+⟩ |
| --- | --- | --- | --- |
| I | — | 0 | nada |
| X | x | 180° | \|0⟩ → \|1⟩ |
| Y | y | 180° | \|0⟩ → i\|1⟩ |
| Z | z | 180° | \|+⟩ → \|−⟩ |
| H | (x+z)/√2 | 180° | \|0⟩ → \|+⟩ |
| S / S† | z | +90° / −90° | \|+⟩ → \|+i⟩ / \|−i⟩ |
| T / T† | z | +45° / −45° | \|+⟩ → fase 45° / −45° |
| √X | x | 90° | \|0⟩ → \|−i⟩ |
| Rx, Ry, Rz (θ) | x, y, z | θ | qualquer ângulo |
| P(λ) | z | λ | fase λ no \|1⟩ |
| U(θ, φ, λ) | qualquer | qualquer | qualquer porta de 1 qubit |

### I — Identidade

$$
I = \begin{pmatrix} 1 & 0 \\ 0 & 1 \end{pmatrix}, \qquad I(\alpha|0\rangle + \beta|1\rangle) = \alpha|0\rangle + \beta|1\rangle
$$

**Conta:** linha 1 · coluna = 1·α + 0·β = α; linha 2 · coluna = 0·α + 1·β = β. Nada muda.

**Na esfera:** rotação de 0°.

**Física:** "não fazer nada" num chip real não é grátis. O tempo passa e o qubit perde informação para o ambiente (decoerência, tempos T1 e T2). Por isso, no hardware, a I é uma espera, usada para medir quanto o qubit aguenta parado.

### X — Pauli-X (o NOT quântico)

$$
X = \begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix}, \qquad X\begin{pmatrix} \alpha \\ \beta \end{pmatrix} = \begin{pmatrix} 0\cdot\alpha + 1\cdot\beta \\ 1\cdot\alpha + 0\cdot\beta \end{pmatrix} = \begin{pmatrix} \beta \\ \alpha \end{pmatrix}
$$

**Conta:** a X troca as duas amplitudes. X|0⟩ = |1⟩ e X|1⟩ = |0⟩, igual ao NOT clássico. Em |+⟩, troca 1/√2 com 1/√2 e não muda nada: |+⟩ fica parado porque está no próprio eixo x.

**Na esfera:** 180° em torno do eixo x. O norte vai para o sul.

**Física:** é o "pulso π". Um pulso de micro-ondas ressonante faz o qubit oscilar entre 0 e 1 (oscilação de Rabi), com P(1) = sin²(Ωt/2), onde Ω é a frequência de Rabi (proporcional à força do pulso). Desligando o pulso em t = π/Ω, o qubit termina exatamente em 1. A X é a Rx(π) a menos da fase global i.

### Y — Pauli-Y

$$
Y = \begin{pmatrix} 0 & -i \\ i & 0 \end{pmatrix}, \qquad Y|0\rangle = \begin{pmatrix} 0 \\ i \end{pmatrix} = i|1\rangle, \qquad Y|1\rangle = \begin{pmatrix} -i \\ 0 \end{pmatrix} = -i|0\rangle
$$

**Conta:** como a X, troca as amplitudes, mas cada uma ganha um fator: Y(α, β) = (−iβ, iα). Em |0⟩ o resultado é i|1⟩. A medição dá 1 com 100%, porque o i é fase global (|i|² = 1).

**Na esfera:** 180° em torno do eixo y. Vale Y = iXZ: a Y é "uma X e uma Z juntas".

**Física:** o mesmo pulso π da X, mas com a fase da micro-onda deslocada de 90°. Esse deslocamento gira o eixo da rotação de x para y no equador.

### Z — Pauli-Z (inverte a fase)

$$
Z = \begin{pmatrix} 1 & 0 \\ 0 & -1 \end{pmatrix}, \qquad Z|+\rangle = \frac{1}{\sqrt 2}\begin{pmatrix} 1 \\ -1 \end{pmatrix} = |-\rangle
$$

**Conta:** a Z deixa o α e troca o sinal do β. Em |0⟩ e |1⟩ não muda nada que se meça (|1⟩ vira −|1⟩, fase global). Em |+⟩ muda tudo: vira |−⟩.

**Na esfera:** 180° em torno do eixo z. Os polos ficam parados e o equador dá meia volta.

**Física:** é a precessão livre. O Hamiltoniano de um qubit parado é H = −(ħω/2)Z, e o estado gira sozinho em torno de z. Por isso a Z não precisa de pulso: em chips supercondutores ela é "virtual", uma mudança na fase de referência dos pulsos seguintes, com duração zero e sem erro.

### H — Hadamard (cria superposição)

$$
H = \frac{1}{\sqrt 2}\begin{pmatrix} 1 & 1 \\ 1 & -1 \end{pmatrix}, \qquad H|0\rangle = \frac{1}{\sqrt 2}\begin{pmatrix} 1\cdot 1 + 1\cdot 0 \\ 1\cdot 1 - 1\cdot 0 \end{pmatrix} = |+\rangle, \qquad H|1\rangle = |-\rangle
$$

**Conta:** H|0⟩ = |+⟩ dá 50% / 50% na medição: (1/√2)² = 1/2. Aplicando duas vezes: H·H = I, então H|+⟩ = |0⟩. A H troca a "linguagem" z pela x: HZH = X e HXH = Z.

**Na esfera:** 180° em torno do eixo diagonal entre x e z. Isso leva o norte para +x e o +x para o norte.

**Física:** não existe pulso "H" nativo. O chip faz H = Ry(π/2)·Z: primeiro uma Z virtual, depois um pulso π/2 em torno de y. Na óptica, um divisor de feixe 50:50 faz o papel da H: o fóton passa a estar nos dois caminhos.

### S e S† — Fase de 90°

$$
S = \begin{pmatrix} 1 & 0 \\ 0 & i \end{pmatrix}, \quad S^\dagger = \begin{pmatrix} 1 & 0 \\ 0 & -i \end{pmatrix}, \qquad S|+\rangle = \frac{1}{\sqrt 2}\begin{pmatrix} 1 \\ i \end{pmatrix} = |{+i}\rangle, \quad S^\dagger|+\rangle = |{-i}\rangle
$$

**Conta:** a S multiplica só o β por i, que é e^{iπ/2}, ou seja, soma 90° à fase. Duas S dão i·i = −1, então S·S = Z. Por isso a S também se chama √Z. A S† faz o contrário (−90°), e S·S† = I.

**Na esfera:** 90° em torno de z (S) ou −90° (S†). O +x vai para +y ou para −y.

**Física:** Z virtual de 90°. S, H e CNOT formam as portas de Clifford, que um computador clássico consegue simular com eficiência (teorema de Gottesman–Knill). Para ter vantagem quântica, falta a T.

### T e T† — Fase de 45°

$$
T = \begin{pmatrix} 1 & 0 \\ 0 & e^{i\pi/4} \end{pmatrix}, \qquad T|+\rangle = \frac{1}{\sqrt 2}\left(|0\rangle + e^{i\pi/4}|1\rangle\right), \qquad e^{i\pi/4} = \frac{1+i}{\sqrt 2}
$$

**Conta:** a T soma 45° à fase do |1⟩. Duas T dão 90°: T·T = S. Quatro T dão Z. A T† usa e^{−iπ/4} e desfaz a T. As probabilidades não mudam (|e^{iπ/4}|² = 1); muda só a longitude φ.

**Na esfera:** 45° em torno de z. Partindo de |+⟩, o ponto para no meio do caminho entre +x e +y.

**Física:** a T é a porta que completa o conjunto universal {H, T, CNOT}: com elas dá para aproximar qualquer circuito. Em computadores com correção de erros, ela é a porta mais cara, porque não pode ser feita direto no código. É preciso "destilar" estados especiais (estados mágicos).

### √X — Raiz de X (SX)

$$
\sqrt X = \frac12\begin{pmatrix} 1+i & 1-i \\ 1-i & 1+i \end{pmatrix}, \qquad \sqrt X|0\rangle = \frac12\begin{pmatrix} 1+i \\ 1-i \end{pmatrix} = \frac{1+i}{2}\begin{pmatrix} 1 \\ -i \end{pmatrix} = e^{i\pi/4}\,|{-i}\rangle
$$

**Conta:** P(0) = |1+i|²/4 = 2/4 = 50%, e P(1) também. Para ver o estado, coloque (1+i)/2 em evidência: sobra (1, −i), porque (1−i)/(1+i) = −i. Aplicando duas vezes, √X·√X = X (confira multiplicando as matrizes).

**Na esfera:** 90° em torno de x. O norte vai para −y. É a metade do caminho da X.

**Física:** é o "pulso π/2", metade da duração do pulso da X. Nos computadores da IBM, a SX é uma das portas nativas: todo circuito é traduzido para SX, X, RZ e uma porta de 2 qubits.

### Rx(θ), Ry(θ), Rz(θ) — Rotações

$$
R_x(\theta) = \begin{pmatrix} \cos\frac\theta2 & -i\sin\frac\theta2 \\ -i\sin\frac\theta2 & \cos\frac\theta2 \end{pmatrix}, \quad R_y(\theta) = \begin{pmatrix} \cos\frac\theta2 & -\sin\frac\theta2 \\ \sin\frac\theta2 & \cos\frac\theta2 \end{pmatrix}, \quad R_z(\theta) = \begin{pmatrix} e^{-i\theta/2} & 0 \\ 0 & e^{i\theta/2} \end{pmatrix}
$$

**Conta (θ = π/2, como no jogo):** cos(π/4) = sin(π/4) = 1/√2.

- Rx(π/2)|0⟩ = (|0⟩ − i|1⟩)/√2 = |−i⟩. É a √X a menos de fase global.
- Ry(π/2)|0⟩ = (|0⟩ + |1⟩)/√2 = |+⟩. As amplitudes ficam reais, por isso a Ry é a rotação "sem números complexos".
- Rz(π/2)|+⟩ = (e^{−iπ/4}|0⟩ + e^{iπ/4}|1⟩)/√2 = e^{−iπ/4}|+i⟩.

Para qualquer θ, partindo de |0⟩ com Rx ou Ry: P(1) = sin²(θ/2). Essa é a curva da oscilação de Rabi.

**Por que θ/2?** Na esfera, girar 360° volta ao mesmo ponto, mas a matriz vira −I. O qubit é um spin 1/2 (um espinor) e só volta ao estado original, com fase e tudo, depois de 720°. Isso foi medido em experimentos com nêutrons nos anos 1970.

**Na esfera:** giro de θ em torno do eixo do nome. A fórmula geral é a da seção 6: R = cos(θ/2)I − i sin(θ/2)·(eixo).

**Física:** Rx e Ry são pulsos de micro-ondas de duração proporcional a θ (fase 0° para x, 90° para y). A Rz é Z virtual. Toda rotação é a solução da equação de Schrödinger para H = (ħΩ/2)·(eixo) ligado por um tempo t = θ/Ω.

### P(λ) — Fase geral (antigo U₁)

$$
P(\lambda) = \begin{pmatrix} 1 & 0 \\ 0 & e^{i\lambda} \end{pmatrix}, \qquad P(\pi) = Z, \quad P(\pi/2) = S, \quad P(\pi/4) = T, \qquad P(\lambda) = e^{i\lambda/2}R_z(\lambda)
$$

**Conta:** P(λ) soma λ à fase do |1⟩. Para ver que P e Rz são "a mesma" porta, tire e^{iλ/2} em evidência de P: sobra diag(e^{−iλ/2}, e^{iλ/2}), que é a Rz(λ). A diferença é só fase global.

**Na esfera:** giro de λ em torno de z. Igual à Rz(λ).

**Física:** também é Z virtual. A fase global não importa sozinha, mas importa quando a porta vira controlada: CP e CRz são portas diferentes (ver seção de 2 qubits).

### U(θ, φ, λ) — Unitária universal (antigo U₃)

$$
U(\theta,\varphi,\lambda) = \begin{pmatrix} \cos\frac\theta2 & -e^{i\lambda}\sin\frac\theta2 \\ e^{i\varphi}\sin\frac\theta2 & e^{i(\varphi+\lambda)}\cos\frac\theta2 \end{pmatrix} = e^{i(\varphi+\lambda)/2}\,R_z(\varphi)\,R_y(\theta)\,R_z(\lambda)
$$

**Conta:** com três ângulos, a U vira qualquer porta de 1 qubit. Exemplo: U(π, 0, π). Como cos(π/2) = 0 e sin(π/2) = 1, a matriz fica \[\[0, −e^{iπ}\], \[1, 0\]\] = \[\[0, 1\], \[1, 0\]\] = X.

| Ângulos (θ, φ, λ) | Porta |
| --- | --- |
| (0, 0, 0) | I |
| (π, 0, π) | X |
| (π, π/2, π/2) | Y |
| (π/2, 0, π) | H |
| (0, 0, λ) | P(λ) |
| (θ, −π/2, π/2) | Rx(θ) |
| (θ, 0, 0) | Ry(θ) |

**Na esfera:** gira λ em z, depois θ em y, depois φ em z. Isso são os ângulos de Euler: qualquer orientação de um corpo rígido sai de três giros assim.

**Física:** é o que o compilador faz com qualquer porta de 1 qubit. Na IBM, a U vira RZ · SX · RZ · SX · RZ: três Z virtuais e dois pulsos π/2.

## Portas de 2 qubits

Portas de 2 qubits são as únicas que criam emaranhamento, e, na física, exigem que os dois qubits interajam. Ordem da base em todas as matrizes: |00⟩, |01⟩, |10⟩, |11⟩, com o primeiro dígito = controle (ou qubit de cima).

**Teste rápido de emaranhamento.** Escreva o estado como a|00⟩ + b|01⟩ + c|10⟩ + d|11⟩. Ele é um produto de dois qubits separados **se e só se** a·d = b·c. Se a·d ≠ b·c, está emaranhado. Use isso para conferir os exemplos abaixo.

**Física comum a todas.** Um qubit sozinho não emaranha. É preciso um termo no Hamiltoniano que envolva os dois, um acoplamento. Cada tecnologia tem o seu acoplamento natural, e as outras portas são montadas a partir dele com portas de 1 qubit:

| Tecnologia | Acoplamento físico | Porta nativa |
| --- | --- | --- |
| Supercondutor (IBM) | cross-resonance: pulsar o controle na frequência do alvo | ECR / CNOT |
| Supercondutor (Google) | acopladores sintonizáveis, troca de energia entre qubits | CZ, √iSWAP |
| Íons presos | vibração coletiva dos íons (fonons) | Rxx (Mølmer–Sørensen) |
| Átomos neutros | bloqueio de Rydberg | CZ |
| Spins em pontos quânticos | interação de troca (Heisenberg) | √SWAP |

Portas de 2 qubits costumam errar bem mais que as de 1 qubit. Por isso os compiladores tentam usar o mínimo possível delas, a mesma ideia das fases de otimização do jogo.

### CNOT (CX) — NOT controlado

$$
\text{CNOT} = \begin{pmatrix} 1&0&0&0 \\ 0&1&0&0 \\ 0&0&0&1 \\ 0&0&1&0 \end{pmatrix}, \qquad \text{CNOT}|c,t\rangle = |c,\ t \oplus c\rangle
$$

**Conta (o estado de Bell, passo a passo):**

1. Comece em |00⟩ = (1, 0, 0, 0).
2. H no primeiro qubit: (|0⟩ + |1⟩)/√2 ⊗ |0⟩ = (|00⟩ + |10⟩)/√2 = (1, 0, 1, 0)/√2.
3. CNOT troca as duas últimas amplitudes: (1, 0, 0, 1)/√2 = (|00⟩ + |11⟩)/√2.
4. Teste: a·d = 1/2 e b·c = 0. Está emaranhado. Medindo, dá 00 ou 11, nunca 01 ou 10.

**Na esfera:** cada qubit do estado de Bell, olhado sozinho, tem vetor de Bloch de tamanho zero (centro da esfera). A informação não está em nenhum dos dois: está na correlação entre eles.

**Física:** na IBM, a CNOT é feita com a porta ECR (cross-resonance): o controle é pulsado na frequência do alvo, e o alvo gira para um lado ou para o outro dependendo do estado do controle. Um fenômeno importante é o **phase kickback**: com controle |+⟩ e alvo |−⟩, a CNOT muda o **controle** para |−⟩ e deixa o alvo como está. A ideia de "controle" e "alvo" depende da base em que você olha.

### CY — Y controlada

$$
\text{CY} = \begin{pmatrix} I & 0 \\ 0 & Y \end{pmatrix} = \begin{pmatrix} 1&0&0&0 \\ 0&1&0&0 \\ 0&0&0&-i \\ 0&0&i&0 \end{pmatrix}, \qquad \text{CY}|10\rangle = |1\rangle \otimes Y|0\rangle = i|11\rangle
$$

**Conta:** se o controle é 0, nada. Se é 1, o alvo recebe a Y: |10⟩ vira i|11⟩ e |11⟩ vira −i|10⟩.

**Na esfera:** quando o controle é 1, o alvo dá 180° em torno de y.

**Física:** não é nativa. O compilador faz CY = (I⊗S)·CNOT·(I⊗S†): gira o eixo y até o x, aplica a CNOT, e gira de volta.

### CZ — Z controlada

$$
\text{CZ} = \begin{pmatrix} 1&0&0&0 \\ 0&1&0&0 \\ 0&0&1&0 \\ 0&0&0&-1 \end{pmatrix}, \qquad \text{CZ}\,|{+}{+}\rangle = \tfrac12\left(|00\rangle + |01\rangle + |10\rangle - |11\rangle\right)
$$

**Conta:** a CZ só troca o sinal de |11⟩. Em |++⟩ = (1, 1, 1, 1)/2 o resultado é (1, 1, 1, −1)/2. Teste: a·d = −1/4 e b·c = 1/4. Emaranhado, sem nenhum qubit "virar".

**Na esfera:** quando um é 1, o outro dá 180° em z. A matriz é simétrica: tanto faz quem é controle. Esse é o ponto físico mais interessante da CZ.

**Física:** nativa nos chips do Google e nos átomos neutros. Nos supercondutores, o estado |11⟩ é aproximado em energia do estado |02⟩ (o transmon tem um terceiro nível). Após uma volta completa entre os dois, |11⟩ retorna com fase π, ou seja, sinal −1. A relação com a CNOT é CNOT = (I⊗H)·CZ·(I⊗H).

### CH — Hadamard controlada

$$
\text{CH} = \begin{pmatrix} I & 0 \\ 0 & H \end{pmatrix}, \qquad \text{CH}\,\frac{|00\rangle + |10\rangle}{\sqrt2} = \frac{1}{\sqrt2}|00\rangle + \frac12|10\rangle + \frac12|11\rangle
$$

**Conta:** o ramo |00⟩ fica igual. O ramo |10⟩ vira |1⟩⊗|+⟩ = (|10⟩ + |11⟩)/√2, e o 1/√2 que já estava na frente multiplica: 1/√2 · 1/√2 = 1/2. Probabilidades: 00 → 50%, 10 → 25%, 11 → 25%. Soma 100%.

**Na esfera:** quando o controle é 1, o alvo dá 180° em torno do eixo diagonal x+z.

**Física:** montada com uma CNOT e rotações Ry de ±π/4 no alvo. É útil para preparar estados com probabilidades desiguais, como os 50/25/25 acima.

### SWAP — Troca

$$
\text{SWAP} = \begin{pmatrix} 1&0&0&0 \\ 0&0&1&0 \\ 0&1&0&0 \\ 0&0&0&1 \end{pmatrix}, \qquad \text{SWAP}\,|a\rangle|b\rangle = |b\rangle|a\rangle
$$

**Conta:** troca as amplitudes de |01⟩ e |10⟩. Com (α|0⟩ + β|1⟩)⊗|0⟩ = (α, 0, β, 0), o resultado é (α, β, 0, 0) = |0⟩⊗(α|0⟩ + β|1⟩). O estado inteiro mudou de qubit.

**Na esfera:** as duas esferas trocam de lugar. Não cria emaranhamento.

**Física:** num chip, cada qubit só conversa com os vizinhos. Para fazer uma porta entre qubits distantes, o compilador vai "andando" com o estado usando SWAPs. Cada SWAP custa 3 CNOTs (CNOT a→b, CNOT b→a, CNOT a→b), por isso a ligação entre os qubits do chip pesa tanto no desempenho.

### iSWAP — Troca imaginária

$$
\text{iSWAP} = \begin{pmatrix} 1&0&0&0 \\ 0&0&i&0 \\ 0&i&0&0 \\ 0&0&0&1 \end{pmatrix} = e^{\,i\frac{\pi}{4}(X\otimes X + Y\otimes Y)}
$$

**Conta:** igual à SWAP, mas quem troca de lugar ganha um fator i: |01⟩ → i|10⟩ e |10⟩ → i|01⟩. |00⟩ e |11⟩ não mudam.

**Na esfera:** troca os qubits e dá uma fase extra. Ao contrário da SWAP, a iSWAP emaranha: em |++⟩ = (1, 1, 1, 1)/2 ela gera (1, i, i, 1)/2. Teste: a·d = 1/4 e b·c = i·i/4 = −1/4, emaranhado.

**Física:** é a porta mais "natural" de todas. Dois qubits supercondutores acoplados e na mesma frequência trocam uma excitação de energia de um para o outro, como dois pêndulos ligados por uma mola. O Hamiltoniano desse acoplamento é proporcional a XX + YY. Deixando agir pelo tempo de uma troca completa, sai exatamente a iSWAP (e o i vem do e^{−iHt}).

### √SWAP — Raiz de SWAP

$$
\sqrt{\text{SWAP}} = \begin{pmatrix} 1&0&0&0 \\ 0&\frac{1+i}{2}&\frac{1-i}{2}&0 \\ 0&\frac{1-i}{2}&\frac{1+i}{2}&0 \\ 0&0&0&1 \end{pmatrix}, \qquad \sqrt{\text{SWAP}}\,|01\rangle = \frac{1+i}{2}|01\rangle + \frac{1-i}{2}|10\rangle
$$

**Conta:** P(01) = |1+i|²/4 = 1/2 e P(10) = 1/2. O estado está "no meio da troca" e é emaranhado (a·d = 0, b·c ≠ 0). Aplicando duas vezes, √SWAP·√SWAP = SWAP.

**Na esfera:** cada qubit fica no centro da esfera no meio da troca, porque o par está emaranhado.

**Física:** foi a porta proposta por Loss e DiVincenzo (1998) para spins de elétrons em pontos quânticos. Os dois spins interagem pela troca de Heisenberg (H ∝ XX + YY + ZZ). Ligando a interação pela metade do tempo de uma SWAP completa, sai a √SWAP. Junto com portas de 1 qubit, ela é universal.

### CRx, CRy, CRz — Rotações controladas

$$
CR_x(\theta) = \begin{pmatrix} I & 0 \\ 0 & R_x(\theta) \end{pmatrix}, \quad CR_y(\theta) = \begin{pmatrix} I & 0 \\ 0 & R_y(\theta) \end{pmatrix}, \quad CR_z(\theta) = \text{diag}\left(1,\ 1,\ e^{-i\theta/2},\ e^{i\theta/2}\right)
$$

**Conta (θ = π/2):**

- CRx em (|00⟩ + |10⟩)/√2: o ramo do 1 recebe Rx(π/2)|0⟩ = (|0⟩ − i|1⟩)/√2. Resultado: |00⟩/√2 + |10⟩/2 − i|11⟩/2.
- CRy em |10⟩ dá |1⟩|+⟩, igual à CH. Mas em |11⟩ dá |1⟩(−|0⟩ + |1⟩)/√2, enquanto a CH dá |1⟩(|0⟩ − |1⟩)/√2. Diferem por um sinal, que vira fase relativa se o controle estiver em superposição.
- CRz em |1⟩|+⟩: o alvo vira e^{−iπ/4}|+i⟩. Aquele e^{−iπ/4} não é mais fase global: ele só aparece no ramo em que o controle é 1.

**Na esfera:** quando o controle é 1, o alvo gira θ em torno de x, y ou z.

**Física:** montadas com 2 CNOTs e rotações de ±θ/2 no alvo. Por exemplo, CRz(θ) = (I⊗Rz(θ/2))·CNOT·(I⊗Rz(−θ/2))·CNOT. Quando o controle é 0, os dois giros se cancelam; quando é 1, as CNOTs invertem o segundo giro e eles se somam.

### CP(λ) — Fase controlada

$$
CP(\lambda) = \text{diag}\left(1,\ 1,\ 1,\ e^{i\lambda}\right), \qquad CP(\lambda) = \left(P(\lambda/2)\otimes I\right)\cdot CR_z(\lambda)
$$

**Conta:** só |11⟩ ganha a fase e^{iλ}. CP(π) = CZ. Em |+⟩|1⟩: (|01⟩ + e^{iλ}|11⟩)/√2 = (|0⟩ + e^{iλ}|1⟩)/√2 ⊗ |1⟩. Quem mudou foi o **controle**, que girou λ em z. Isso é phase kickback de novo.

**CP × CRz:** P(λ) e Rz(λ) diferem só por fase global. Controladas, essa fase vira uma rotação real do controle, e por isso CP e CRz são portas diferentes. A fórmula da direita mostra exatamente quanto: um P(λ/2) extra no controle.

**Na esfera:** simétrica como a CZ. Quando um qubit é 1, o outro gira λ em z.

**Física:** é o tijolo da Transformada de Fourier Quântica (QFT). O kickback é a base da estimativa de fase, que está por trás do algoritmo de Shor.

### CU — Unitária controlada

$$
CU(\theta,\varphi,\lambda,\gamma) = |0\rangle\langle0|\otimes I + e^{i\gamma}\,|1\rangle\langle1|\otimes U(\theta,\varphi,\lambda)
$$

**Conta:** a CU é a fórmula geral das controladas aplicada à U. O ângulo extra γ existe por causa da lição da CP: a fase global da U vira relativa quando controlada, então o Qiskit deixa você escolhê-la. Equivalências (com γ = 0): CU(π, 0, π) = CNOT, CU(π/2, 0, π) = CH, CU(0, 0, λ) = CP(λ).

**Na esfera:** quando o controle é 1, o alvo recebe qualquer rotação.

**Física:** qualquer porta controlada de 1 alvo sai de no máximo 2 CNOTs mais portas de 1 qubit. É o que o compilador faz com a CU.

### Rxx, Ryy, Rzz — Portas de Ising

$$
R_{xx}(\theta) = e^{-i\frac\theta2 X\otimes X} = \cos\tfrac\theta2\, I - i\sin\tfrac\theta2\, X\otimes X, \qquad R_{zz}(\theta) = \text{diag}\left(e^{-i\theta/2},\ e^{i\theta/2},\ e^{i\theta/2},\ e^{-i\theta/2}\right)
$$

A Ryy é igual à Rxx com Y⊗Y no lugar de X⊗X. A fórmula cos·I − i·sin·M vale porque (X⊗X)² = I, a mesma ideia das rotações de 1 qubit.

**Conta (θ = π/2):**

- X⊗X vira os dois qubits: XX|00⟩ = |11⟩. Então Rxx(π/2)|00⟩ = (|00⟩ − i|11⟩)/√2, um estado tipo Bell numa porta só.
- Y⊗Y também vira os dois, mas com sinais: YY|00⟩ = (i)(i)|11⟩ = −|11⟩. Então Ryy(π/2)|00⟩ = (|00⟩ + i|11⟩)/√2.
- Z⊗Z só olha a paridade: +1 se os bits são iguais, −1 se diferentes. A Rzz dá fase e^{−iθ/2} para 00 e 11 e e^{+iθ/2} para 01 e 10.
- Rxx(π/2)·Ryy(π/2) = iSWAP†, a relação da fase 56 do jogo.

**Na esfera:** os dois qubits giram "juntos". Com Rxx ou Ryy em |00⟩ e θ = π/2, cada um termina no centro da esfera (emaranhamento máximo). A Rzz não mexe em |00⟩ (só dá fase): ela emaranha estados do equador, como |++⟩.

**Física:** o nome vem do modelo de Ising do magnetismo, onde spins vizinhos têm energia J·Z⊗Z: preferem ficar alinhados (ou opostos). A Rzz é essa energia ligada por um tempo, e é a peça central do algoritmo QAOA. Em íons presos, a Rxx é nativa: a porta de Mølmer–Sørensen usa lasers que empurram os íons, e a vibração compartilhada deles acopla os spins. Num chip com CNOT, a Rzz é montada como CNOT·(I⊗Rz(θ))·CNOT: a primeira CNOT guarda a paridade no alvo, a Rz dá a fase de acordo com ela, e a segunda CNOT desfaz.

## Portas de 3 qubits ou mais

Com 3 qubits o vetor tem 8 amplitudes (|000⟩ a |111⟩) e as matrizes são 8×8. Não precisa escrevê-las inteiras: as quatro portas abaixo são a identidade com uma pequena mudança no canto de baixo, então basta saber o que acontece em cada estado de base.

**Física comum a todas.** Quase nenhum hardware faz portas de 3 qubits diretamente. Elas são decompostas em portas de 1 e 2 qubits. A exceção são átomos de Rydberg e íons, onde há demonstrações de portas multiqubit nativas.

### Toffoli (CCX, CCNOT) — NOT com dois controles

$$
\text{Toffoli}\,|a, b, c\rangle = |a,\ b,\ c \oplus (a \cdot b)\rangle, \qquad \text{Toffoli} = \begin{pmatrix} I_6 & 0 \\ 0 & X \end{pmatrix}
$$

**Conta:** o alvo só vira quando os dois controles são 1. Partindo de c = 0, o alvo termina com a AND b:

| Entrada \|a b 0⟩ | Saída | a AND b |
| --- | --- | --- |
| \|000⟩ | \|000⟩ | 0 |
| \|010⟩ | \|010⟩ | 0 |
| \|100⟩ | \|100⟩ | 0 |
| \|110⟩ | \|111⟩ | 1 |

Na matriz, I₆ é a identidade nos 6 primeiros estados e a X troca as amplitudes de |110⟩ e |111⟩.

**Na esfera:** o alvo dá 180° em x somente no ramo a = b = 1.

**Física:** a Toffoli é a AND reversível. Uma AND comum perde informação (de 0 na saída não dá para saber a entrada), e o princípio de Landauer diz que apagar um bit dissipa no mínimo kT·ln 2 de calor. Guardando a e b, nada é apagado. Com ela dá para fazer qualquer conta clássica dentro de um computador quântico. No chip, a decomposição padrão da Toffoli usa 6 CNOTs, 7 portas T ou T† e algumas H.

### Fredkin (CSWAP) — SWAP controlada

$$
\text{Fredkin}\,|0, a, b\rangle = |0, a, b\rangle, \qquad \text{Fredkin}\,|1, a, b\rangle = |1, b, a\rangle
$$

**Conta:** com controle 1, troca os outros dois. Exemplo: |101⟩ → |110⟩. Repare que a quantidade de 1s não muda nunca: é uma porta conservativa.

**Na esfera:** se o controle é 1, as esferas dos dois alvos trocam de lugar.

**Física:** foi pensada por Fredkin e Toffoli no "computador de bolas de bilhar": a conservação dos 1s imita a conservação de partículas. Em computação quântica ela aparece no **teste SWAP**, que mede o quanto dois estados são parecidos. Decomposição: CNOT(b→a) · Toffoli(controle, a → b) · CNOT(b→a), a mesma ideia de "SWAP = 3 CNOTs" com a do meio controlada.

### CCZ — Z com dois controles

$$
\text{CCZ} = \text{diag}(1, 1, 1, 1, 1, 1, 1, -1), \qquad \text{Toffoli} = (I\otimes I\otimes H)\cdot\text{CCZ}\cdot(I\otimes I\otimes H)
$$

**Conta:** só |111⟩ troca de sinal. Em |+++⟩ = (1, 1, 1, 1, 1, 1, 1, 1)/√8 o resultado é (1, 1, 1, 1, 1, 1, 1, −1)/√8. A medição não muda (12,5% para cada), mas o estado agora tem um "marcador" no 111.

**Na esfera:** como a CZ, é simétrica: não existe controle e alvo, os três qubits têm o mesmo papel.

**Física:** marcar um estado com sinal −1 é exatamente o oráculo do algoritmo de Grover com 3 qubits. A CCZ e a Toffoli são a mesma porta vista em bases diferentes (as H trocam z por x no alvo, como HZH = X).

### MCX — X multicontrolada

$$
\text{MCX}\,|x_1, x_2, \ldots, x_n,\ t\rangle = |x_1, x_2, \ldots, x_n,\ t \oplus (x_1 \cdot x_2 \cdots x_n)\rangle
$$

**Conta:** com n controles, o alvo vira só quando todos são 1. Com 3 controles, só |1110⟩ ↔ |1111⟩ trocam; os outros 14 estados ficam iguais. A matriz é 2^(n+1) × 2^(n+1): com 3 controles, 16×16. CNOT (n = 1) e Toffoli (n = 2) são casos particulares.

**Na esfera:** o alvo dá 180° em x somente no ramo em que todos os controles são 1.

**Física:** é a AND de n entradas, e a base dos oráculos de Grover. O custo cresce com n: sem qubits extras, a decomposição fica bem longa; com qubits auxiliares (ancilas), dá para montar a MCX com uma cadeia de Toffolis, o que a fase "MCX montada com Toffolis" do jogo mostra. Cada ancila precisa voltar a |0⟩ no fim, senão fica emaranhada com o resultado e estraga a interferência.

## Exercícios para fazer no papel

Faça a conta à mão primeiro e só depois confira com os testes abaixo. As respostas estão no fim de cada item.

1. Calcule H·X·H|0⟩ multiplicando as matrizes. Resposta: HXH = Z, então o resultado é |0⟩.
2. Calcule S·H|0⟩ e diga em que ponto da esfera ele fica. Resposta: (|0⟩ + i|1⟩)/√2 = |+i⟩, no eixo +y.
3. Mostre que T⁸ = I. Resposta: cada T soma 45° de fase; 8 × 45° = 360°, e e^{i2π} = 1.
4. Mostre que Rx(π) = −iX e explique por que, mesmo assim, as duas dão a mesma medição. Resposta: cos(π/2) = 0 e sin(π/2) = 1; o −i é fase global.
5. Aplique a CNOT em |1⟩|+⟩. Por que nada muda? Resposta: o controle é 1, então o alvo recebe X, mas X|+⟩ = |+⟩ (|+⟩ está no eixo da rotação).
6. Use o teste a·d = b·c em (|00⟩ + |01⟩ + |10⟩ + |11⟩)/2. Resposta: a·d = b·c = 1/4, então não está emaranhado: é |+⟩|+⟩.
7. Calcule CZ em |+⟩|1⟩ e diga qual qubit mudou. Resposta: (|01⟩ − |11⟩)/√2 = |−⟩|1⟩. Quem mudou foi o de cima (phase kickback).

## Testes que conferem as contas

Cada relação citada no guia tem um teste automático, no mesmo formato pytest dos testes do jogo. São 26 testes, e todos passam. Eles ficam em dois arquivos do Qubit\_Lab:

| Arquivo | O que tem |
| --- | --- |
| `docs/estudo_portas/portas_conferir.py` | só as definições: estados, matrizes das portas e ferramentas (`bloch`, `emaranhado`, `controlada`) |
| `tests/test_guia_portas.py` | os testes, um por relação do guia |

Para rodar, com o `.venv` ativado e dentro da pasta do Qubit\_Lab:

```bash
pytest tests/test_guia_portas.py -v
```

O `-v` mostra o nome de cada teste com PASSED (passou) ou FAILED (falhou). Rodando só `pytest`, eles entram junto com os testes do jogo.

Cada teste é uma função com nome começando em `test_`, e o `assert` diz o que precisa ser verdade. Três exemplos do arquivo:

```python
def test_h_vezes_h_e_identidade():
    assert np.allclose(H @ H, I)


def test_rx_de_360_graus_e_menos_identidade():
    """O espinor: girar 2π dá -I, e só 4π volta a I."""
    assert np.allclose(Rx(2 * np.pi), -I)
    assert np.allclose(Rx(4 * np.pi), I)


def test_estado_de_bell():
    bell = CNOT @ np.kron(H, I) @ np.kron(ket0, ket0)
    assert np.allclose(bell, np.array([1, 0, 0, 1]) / np.sqrt(2))
    assert emaranhado(bell)
```

No NumPy, `@` é a multiplicação de matrizes e `np.kron` é o produto tensorial ⊗. A ordem das matrizes no código segue a regra da seção 2: a porta aplicada primeiro fica à direita. O `np.allclose` compara ignorando a sobra minúscula de arredondamento do computador. Para treinar, troque um número num teste e veja ele falhar.

## Fontes

O guia foi escrito a partir de conhecimento padrão da área, e as contas foram conferidas com o script acima. As fontes abaixo confirmam cada parte e servem para aprofundar.

**Matemática das portas (matrizes, unitárias, composição)**

- [Basics of Quantum Information — IBM Quantum Learning (John Watrous)](https://quantum.cloud.ibm.com/learning/courses/basics-of-quantum-information): curso gratuito, do estado de 1 qubit até emaranhamento e teleporte. O melhor ponto de partida.
- [Quantum logic gate — Wikipedia](https://en.wikipedia.org/wiki/Quantum_logic_gate) e [List of quantum logic gates — Wikipedia](https://en.wikipedia.org/wiki/List_of_quantum_logic_gates): as matrizes de quase todas as 34 portas numa página só.
- [Qiskit Circuit Library — documentação IBM](https://quantum.cloud.ibm.com/docs/api/qiskit/circuit_library): a matriz oficial de cada porta como o Qiskit define (U, CU, P, RXX, RYY, RZZ, iSWAP, MCX). Lembre que o Qiskit usa a ordem de qubits invertida.
- [iSwapGate — código-fonte do Qiskit](https://qiskit.org/documentation/_modules/qiskit/circuit/library/standard_gates/iswap.html): confirma iSWAP = exp(iπ/4·(XX + YY)).
- [Barenco et al., "Elementary gates for quantum computation" (1995)](https://arxiv.org/abs/quant-ph/9503016): decomposição de portas controladas, Toffoli e MCX em portas de 1 e 2 qubits.
- Livro: Nielsen e Chuang, *Quantum Computation and Quantum Information* (Cambridge). A referência clássica de toda a área; a decomposição da Toffoli com 6 CNOTs e 7 T está no capítulo 4.

**Física (como as portas são feitas)**

- [Krantz et al., "A Quantum Engineer's Guide to Superconducting Qubits" (2019)](https://arxiv.org/abs/1904.06560): pulsos de micro-ondas, oscilação de Rabi, CZ, iSWAP e cross-resonance em qubits supercondutores.
- [McKay et al., "Efficient Z-Gates for Quantum Computing" (2017)](https://arxiv.org/abs/1612.00858): a Z virtual, de duração zero.
- [Loss e DiVincenzo, "Quantum Computation with Quantum Dots" (1998)](https://arxiv.org/abs/cond-mat/9701055): a √SWAP com spins de elétrons.
- [Sørensen e Mølmer, "Quantum computation with ions in thermal motion" (1999)](https://arxiv.org/abs/quant-ph/9810039): a porta de Mølmer–Sørensen (tipo Rxx) em íons presos.
- [Rauch et al., "Verification of Coherent Spinor Rotation of Fermions" (1975)](https://www.oeaw.ac.at/fileadmin/Institute/IQOQI-Vienna/PDF/publications-zeilinger/1975_Verification_of_Coherent_Spinor_Rotation_of_Fermions.pdf): o experimento com nêutrons que mostrou o sinal −1 depois de 360° (o "por que θ/2").
- [Landauer, "Irreversibility and Heat Generation in the Computing Process" (1961)](https://doi.org/10.1147/rd.53.0183): o custo kT·ln 2 de apagar um bit, citado na Toffoli.
