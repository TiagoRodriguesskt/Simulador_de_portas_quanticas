"""Textos das cartas de porta: analogia do dia a dia e o que acontece na esfera."""

CARTAS = {
    "X": {
        "subtitulo": "O NOT quântico",
        "analogia": "É como virar uma ampulheta de cabeça para baixo: o que estava em cima vai "
                    "para baixo. O |0⟩ vira |1⟩ e o |1⟩ vira |0⟩.",
        "esfera": "Meia volta em torno do eixo x. O polo norte vai para o polo sul.",
    },
    "H": {
        "subtitulo": "Cria a superposição",
        "analogia": "É como lançar uma moeda para o alto: enquanto gira, ela não é cara nem coroa. "
                    "A diferença é que, aplicando a H de novo, a moeda volta exatamente para onde "
                    "estava. Isso é interferência.",
        "esfera": "Meia volta em torno do eixo diagonal entre x e z. O polo norte vai parar no equador.",
    },
    "Z": {
        "subtitulo": "Inverte a fase",
        "analogia": "É como inverter o sentido de uma onda: ela continua com o mesmo tamanho, mas "
                    "agora sobe onde antes descia. Sozinha, você não percebe a diferença; somada "
                    "a outra onda, ela muda tudo.",
        "esfera": "Meia volta em torno do eixo z. Os polos não se mexem, mas o equador gira.",
    },
    "CNOT": {
        "subtitulo": "O X condicional",
        "analogia": "É como um interruptor que só funciona se outro estiver ligado: o qubit de "
                    "controle decide se o alvo é invertido. Com o controle em superposição, os "
                    "dois qubits ficam emaranhados.",
        "esfera": "Quando os qubits se emaranham, a esfera de cada um perde o vetor: o estado "
                  "passa a pertencer ao par, não a cada qubit sozinho.",
    },
    "S": {
        "subtitulo": "Um quarto de volta",
        "analogia": "É como o ponteiro de um relógio andando de 12 para 3: um quarto de volta. "
                    "Duas S seguidas dão meia volta, que é exatamente um Z.",
        "esfera": "Um quarto de volta em torno do eixo z. Do eixo x, o qubit vai para o eixo y.",
    },
    "T": {
        "subtitulo": "Um oitavo de volta",
        "analogia": "É o ajuste mais fino da fase: meio quarto de volta. Duas T formam uma S, "
                    "quatro formam um Z. Com H e T dá para chegar perto de qualquer estado.",
        "esfera": "Um oitavo de volta (45°) em torno do eixo z. Os polos não se mexem.",
    },
    "TOFFOLI": {
        "subtitulo": "O AND reversível",
        "analogia": "É como uma porta com duas fechaduras: o terceiro qubit só é invertido se os "
                    "dois de cima forem 1. Com o alvo em 0, ele vira o AND dos dois, sem apagar "
                    "as entradas.",
        "esfera": "Com controles em superposição, o alvo se emaranha com eles e o vetor encolhe.",
    },
    "CZ": {
        "subtitulo": "A fase condicional",
        "analogia": "É uma marca invisível: só o |11⟩ ganha um sinal de menos. Nada muda nas "
                    "probabilidades, mas a marca aparece quando as ondas se somam. É assim que "
                    "o oráculo de Grover 'aponta' a resposta.",
        "esfera": "Com os dois qubits em |+⟩, a CZ os emaranha: os dois vetores somem para o centro.",
    },
    "Y": {
        "subtitulo": "O giro que faltava",
        "analogia": "O X gira em torno do eixo x, o Z em torno do eixo z, e o Y completa o trio: "
                    "meia volta em torno do eixo y. Nos polos ele age como o X (troca |0⟩ e |1⟩); "
                    "no equador, como o Z (troca |+⟩ e |−⟩).",
        "esfera": "Meia volta em torno do eixo y. Só os pontos sobre o eixo y ficam parados.",
    },
    "SDG": {
        "subtitulo": "A S ao contrário",
        "analogia": "Se a S é o ponteiro andando de 12 para 3, a S† é o ponteiro voltando de 3 para "
                    "12. Uma desfaz a outra: S seguida de S† é como não fazer nada. O † (lê-se "
                    "'adaga') marca a porta inversa.",
        "esfera": "Um quarto de volta em torno do eixo z, no sentido contrário ao da S.",
    },
    "TDG": {
        "subtitulo": "A T ao contrário",
        "analogia": "A T† desfaz a T: um oitavo de volta para trás. Assim como duas T formam uma S, "
                    "duas T† formam uma S†.",
        "esfera": "Um oitavo de volta (45°) em torno do eixo z, no sentido contrário ao da T.",
    },
    "SX": {
        "subtitulo": "Meio NOT",
        "analogia": "Se o X é virar a ampulheta de cabeça para baixo, a √X é deitá-la de lado: só "
                    "metade do caminho. Aplicada duas vezes, ela completa a virada e vira um X. "
                    "Por isso o nome: raiz quadrada de X.",
        "esfera": "Um quarto de volta em torno do eixo x. Do polo norte, o qubit vai para o eixo y.",
    },
    "SWAP": {
        "subtitulo": "A troca de lugar",
        "analogia": "É como dois copos trocando o conteúdo: o que estava no qubit de cima vai para o "
                    "de baixo, e vice-versa. E não é só o 0 ou o 1 que muda de lugar: a superposição "
                    "e a fase vão juntas, inteirinhas.",
        "esfera": "Os dois vetores trocam de esfera. No meio do caminho eles encolhem: meia SWAP "
                  "emaranha os qubits.",
    },
    "ISWAP": {
        "subtitulo": "A troca com fase",
        "analogia": "É a SWAP com um carimbo: quando os qubits são diferentes, o que muda de lugar "
                    "chega com um i de fase, um quarto de volta. Em vários computadores quânticos, "
                    "é a troca que o hardware faz de forma natural.",
        "esfera": "Os vetores trocam de esfera, e o que chega ganha um quarto de volta em z: "
                  "um |+⟩ chega como |+i⟩.",
    },
    "CSWAP": {
        "subtitulo": "A troca com chave",
        "analogia": "É uma SWAP com interruptor: o qubit de cima é a chave. Se ele for 1, os outros "
                    "dois trocam de lugar; se for 0, nada acontece. Com a chave em superposição, a "
                    "troca acontece e não acontece ao mesmo tempo.",
        "esfera": "Com o controle em |+⟩, os três qubits se emaranham e os vetores somem para o centro.",
    },
    "CY": {
        "subtitulo": "O Y com interruptor",
        "analogia": "Toda porta de um qubit pode ganhar um interruptor: a bolinha é o controle, e a "
                    "caixa é a porta que só age quando ele vale 1. A CNOT é um X controlado; a CY "
                    "é o mesmo, com um Y na caixa. Por isso ela inverte o alvo e ainda põe um i.",
        "esfera": "Com o controle em |+⟩, os dois qubits se emaranham e os vetores encolhem.",
    },
    "CH": {
        "subtitulo": "Superposição sob condição",
        "analogia": "É um H com interruptor: se o controle for 1, o alvo entra em superposição; se "
                    "for 0, fica como está. Com o controle em superposição, metade das vezes o alvo "
                    "é sorteado, e as probabilidades deixam de ser iguais.",
        "esfera": "Com o controle em |+⟩, o alvo vai só até o meio do caminho, e os dois encolhem "
                  "um pouco: emaranhamento parcial.",
    },
    "CCZ": {
        "subtitulo": "A marca para três",
        "analogia": "É a CZ com mais um qubit: só o |111⟩ ganha o sinal de menos. Como na CZ, não "
                    "importa quem é controle e quem é alvo: os três fios ganham uma bolinha. Com "
                    "H no terceiro qubit antes e depois, ela vira uma Toffoli.",
        "esfera": "Com os três qubits em |+⟩, eles se emaranham e os vetores encolhem.",
    },
    "RX": {
        "subtitulo": "O giro com ângulo",
        "analogia": "Até aqui cada porta tinha um giro fixo. As rotações têm um ângulo no nome: "
                    "Rx(π/2) é um quarto de volta em torno do eixo x. É o mesmo giro da √X; as duas "
                    "diferem só por uma fase global, que nenhuma medida percebe.",
        "esfera": "Um quarto de volta em torno do eixo x. Do polo norte, o qubit vai para o lado "
                  "negativo do eixo y.",
    },
    "RY": {
        "subtitulo": "O giro sem números complexos",
        "analogia": "A Ry gira em torno do eixo y, e a matriz dela só tem números reais. Do polo "
                    "norte, Ry(π/2) leva o qubit para |+⟩, como a H. A diferença: a H é um espelho "
                    "(duas H voltam ao início), e a Ry é um giro (duas Ry seguem em frente, até |1⟩).",
        "esfera": "Um quarto de volta em torno do eixo y. Do polo norte, o qubit vai para o eixo x.",
    },
    "RZ": {
        "subtitulo": "A S com fase global",
        "analogia": "A Rz(π/2) gira um quarto de volta em torno do eixo z, como a S. A diferença é "
                    "uma fase global: a Rz divide o giro entre |0⟩ e |1⟩ (−π/4 e +π/4), e a S põe "
                    "tudo em |1⟩. Sozinhas, ninguém nota a diferença.",
        "esfera": "Um quarto de volta em torno do eixo z: |+⟩ vai para |+i⟩. Os polos não se mexem.",
    },
    "P": {
        "subtitulo": "A família da fase",
        "analogia": "A P(θ) gira só a amplitude de |1⟩ pelo ângulo θ. Várias portas que você já "
                    "conhece são da família dela: P(π) é o Z, P(π/2) é a S, P(π/4) é a T. Com o "
                    "ângulo no nome, fica claro que todas fazem a mesma coisa, em doses diferentes.",
        "esfera": "Um quarto de volta em torno do eixo z, igualzinho à S.",
    },
    "CP": {
        "subtitulo": "A S controlada",
        "analogia": "É a P(π/2) com interruptor: se os dois qubits forem 1, a amplitude ganha um i. "
                    "A CZ põe um −1 no |11⟩; a CP(π/2) põe só metade disso. Duas CP(π/2) formam "
                    "uma CZ.",
        "esfera": "Com os dois qubits em |+⟩, o i no |11⟩ emaranha os qubits e os vetores encolhem.",
    },
    "CRZ": {
        "subtitulo": "Quando a fase global aparece",
        "analogia": "Sozinhas, Rz(π/2) e P(π/2) são a mesma porta, a menos de uma fase global. "
                    "Com interruptor, não: a fase extra da Rz só acontece quando o controle é 1, "
                    "e uma fase que depende de outro qubit é uma fase de verdade.",
        "esfera": "Com os dois qubits em |+⟩, eles se emaranham, mas de um jeito diferente da CP.",
    },
    "CRX": {
        "subtitulo": "Meio NOT condicional",
        "analogia": "Se o controle for 1, o alvo gira um quarto de volta em torno do eixo x. Duas "
                    "CRx(π/2) quase formam uma CNOT: só sobra uma fase no controle.",
        "esfera": "Com o controle em |+⟩, o alvo vai até o meio do caminho e os dois encolhem.",
    },
    "CRY": {
        "subtitulo": "A Ry com interruptor",
        "analogia": "Se o controle for 1, o alvo gira um quarto de volta em torno do eixo y. Com o "
                    "alvo em |0⟩, faz o mesmo que a CH. Com o alvo em |1⟩, a diferença entre um "
                    "giro e um espelho aparece no sinal.",
        "esfera": "Com o controle em |+⟩, o alvo vai até o meio do caminho e os dois encolhem.",
    },
    "RXX": {
        "subtitulo": "Giro de dois qubits juntos",
        "analogia": "Até aqui, as portas de dois qubits tinham um controle e um alvo. A Rxx não tem "
                    "chefe: gira os dois qubits juntos, como uma peça só. De |00⟩, ela chega direto a um "
                    "estado de Bell, sem H e sem CNOT. Em computadores de íons presos, é a porta nativa.",
        "esfera": "Partindo de |00⟩, os dois vetores encolhem juntos até o centro: emaranhamento.",
    },
    "RYY": {
        "subtitulo": "O giro YY",
        "analogia": "A irmã da Rxx, girando em torno de Y⊗Y. Também cria um estado de Bell a partir de "
                    "|00⟩, mas com o sinal da fase trocado. Rxx e Ryy, uma depois da outra, formam uma "
                    "troca de qubits com fase.",
        "esfera": "Partindo de |00⟩, os dois vetores encolhem juntos até o centro.",
    },
    "RZZ": {
        "subtitulo": "A interação de Ising",
        "analogia": "A Rzz só mexe nas fases: qubits iguais (|00⟩, |11⟩) ganham uma fase, e qubits "
                    "diferentes (|01⟩, |10⟩) ganham a oposta. É a energia entre dois ímãs vizinhos no "
                    "modelo de Ising, e a peça principal de algoritmos de otimização como o QAOA.",
        "esfera": "Com os dois qubits em |+⟩, eles se emaranham e os vetores encolhem.",
    },
    "SQSWAP": {
        "subtitulo": "Meia troca",
        "analogia": "Assim como a √X é meio X, a √SWAP é meia troca: os qubits param no meio do "
                    "caminho, emaranhados. Duas meias trocas fazem uma troca inteira. É a porta "
                    "natural dos computadores quânticos de spin.",
        "esfera": "Partindo de |10⟩, os dois vetores encolhem até o centro: no meio da troca, os "
                  "qubits estão emaranhados.",
    },
    "U": {
        "subtitulo": "A porta de três ângulos",
        "analogia": "A U é a porta que descreve todas as outras de um qubit: três ângulos, θ, φ e λ, "
                    "dizem para onde o vetor vai. Esta carta tem os ângulos (π/2, 0, π). Coloque-a no "
                    "circuito e compare: com esses ângulos, ela trabalha igual a uma porta que você "
                    "conhece bem.",
        "esfera": "Do polo norte, o vetor vai para |+⟩.",
    },
    "UX": {
        "subtitulo": "A mesma U, outros ângulos",
        "analogia": "A mesma letra U, com os ângulos (π, 0, π). O θ é o quanto o vetor se afasta do "
                    "polo: com θ = π, ele vai até o polo oposto. Duas cartas U diferentes podem "
                    "trabalhar como duas portas completamente diferentes.",
        "esfera": "Meia volta: do polo norte ao polo sul.",
    },
    "US": {
        "subtitulo": "A U que só gira a fase",
        "analogia": "Com θ = 0, a U não afasta o vetor do polo; só o ângulo λ trabalha, girando a "
                    "fase. Esta carta tem λ = π/2. Uma volta de um quarto em torno do eixo z: você "
                    "já viu essa porta muitas vezes.",
        "esfera": "Um quarto de volta em torno do eixo z: |+⟩ vai para |+i⟩.",
    },
    "CU": {
        "subtitulo": "A controlada de três ângulos",
        "analogia": "A U com interruptor: se o controle for 1, o alvo recebe uma U(π, 0, π). Toda "
                    "controlada de um alvo é uma CU com os ângulos certos. Com estes ângulos, ela "
                    "trabalha igual à primeira porta de dois qubits do jogo.",
        "esfera": "Com o controle em |+⟩, os dois qubits se emaranham.",
    },
    "CUH": {
        "subtitulo": "A mesma CU, outros ângulos",
        "analogia": "A mesma U controlada, agora com (π/2, 0, π) dentro da caixa. Mude os ângulos e "
                    "ela vira outra controlada que você já conhece.",
        "esfera": "Com o controle em |+⟩, o alvo vai só até o meio do caminho.",
    },
    "I": {
        "subtitulo": "A porta que não faz nada",
        "analogia": "A identidade não muda nada: o qubit sai como entrou. É o que sobra quando uma "
                    "porta encontra a inversa dela, como X·X ou H·H. Às vezes, não estragar é a "
                    "resposta certa.",
        "esfera": "Nada se mexe: o vetor fica onde estava.",
    },
    "MCX": {
        "subtitulo": "Muitos controles",
        "analogia": "A CNOT tem um controle, a Toffoli tem dois, e a MCX tem quantos se quiser: aqui, "
                    "três. Ela inverte o alvo só se todos os controles forem 1, como um AND de três "
                    "entradas. É a primeira porta de quatro qubits do laboratório.",
        "esfera": "Com um controle em |+⟩ e os outros em 1, o alvo se emaranha com ele.",
    },
}


def carta(nome: str) -> dict:
    return CARTAS.get(nome, {"subtitulo": "", "analogia": "", "esfera": ""})


# ------------------------------------------------------------------ glossário ---
# Uma entrada por porta do jogo, na ordem em que elas aparecem nas fases.
GLOSSARIO = {
    "X": {
        "resumo": "Inverte o qubit: |0⟩ vira |1⟩ e |1⟩ vira |0⟩.",
        "faz": "É o equivalente quântico da porta NOT da lógica clássica. Numa superposição, troca as "
               "amplitudes de |0⟩ e |1⟩ entre si: α|0⟩ + β|1⟩ vira β|0⟩ + α|1⟩.",
        "esfera": "Meia volta (180°) em torno do eixo x. Os polos trocam de lugar.",
        "relacoes": ["X·X = I: aplicar duas vezes desfaz", "H·X·H = Z", "Também chamada de Pauli-X ou NOT"],
        "qiskit": "qc.x(0)",
    },
    "H": {
        "resumo": "Leva |0⟩ a (|0⟩ + |1⟩)/√2 e |1⟩ a (|0⟩ − |1⟩)/√2.",
        "faz": "Transforma cada estado da base numa mistura igual dos dois, com 50% de chance cada. "
               "H|0⟩ e H|1⟩ diferem só no sinal (a fase); por isso, aplicar a H de novo faz as "
               "amplitudes interferirem e o qubit volta ao estado inicial.",
        "esfera": "Meia volta em torno do eixo diagonal entre x e z. O polo norte vai para o eixo x.",
        "relacoes": ["H·H = I", "H·Z·H = X e H·X·H = Z: a H troca os eixos x e z",
                     "Abre quase todo algoritmo quântico"],
        "qiskit": "qc.h(0)",
    },
    "Z": {
        "resumo": "Troca o sinal da amplitude de |1⟩: α|0⟩ + β|1⟩ vira α|0⟩ − β|1⟩.",
        "faz": "Não muda as probabilidades: medir antes ou depois do Z dá as mesmas chances. Muda o "
               "sinal da amplitude de |1⟩, e esse sinal decide o resultado quando há interferência, "
               "por exemplo entre duas H.",
        "esfera": "Meia volta em torno do eixo z. Os polos ficam parados; o equador gira 180°.",
        "relacoes": ["Z·Z = I", "S·S = Z", "H·Z·H = X"],
        "qiskit": "qc.z(0)",
    },
    "CNOT": {
        "resumo": "Se o controle for 1, inverte o alvo.",
        "faz": "Age em dois qubits: o controle (bolinha) e o alvo (⊕). Com entradas clássicas, o alvo "
               "vira controle XOR alvo e o controle não muda. Com o controle em superposição, a CNOT "
               "emaranha os qubits: H seguida de CNOT gera o estado de Bell (|00⟩ + |11⟩)/√2.",
        "esfera": "Ao emaranhar os qubits, o vetor de cada esfera encolhe até o centro.",
        "relacoes": ["CNOT·CNOT = I", "Com H no alvo antes e depois, vira uma CZ",
                     "Também chamada de CX"],
        "qiskit": "qc.cx(0, 1)",
    },
    "S": {
        "resumo": "Multiplica a amplitude de |1⟩ por i.",
        "faz": "Como o Z, não muda as probabilidades, só a fase de |1⟩, mas gira metade do que o Z "
               "gira: α|0⟩ + β|1⟩ vira α|0⟩ + iβ|1⟩.",
        "esfera": "90° em torno do eixo z: do eixo x, o qubit vai para o eixo y.",
        "relacoes": ["S·S = Z", "T·T = S", "Quatro S dão uma volta inteira: S·S·S·S = I"],
        "qiskit": "qc.s(0)",
    },
    "T": {
        "resumo": "Multiplica a amplitude de |1⟩ por e^(iπ/4).",
        "faz": "O ajuste mais fino de fase do jogo. Junto com a H, forma um conjunto universal: "
               "combinando H e T, dá para chegar tão perto quanto se queira de qualquer porta de "
               "um qubit.",
        "esfera": "45° em torno do eixo z. Os polos não se mexem.",
        "relacoes": ["T·T = S", "T·T·T·T = Z", "Quatro T são um Z; oito T, uma volta inteira"],
        "qiskit": "qc.t(0)",
    },
    "TOFFOLI": {
        "resumo": "Se os dois controles forem 1, inverte o alvo.",
        "faz": "Uma CNOT com dois controles. Com o alvo em 0, ele vira o AND dos dois controles, e as "
               "entradas continuam lá. Por isso a Toffoli é o AND reversível: com ela dá para fazer "
               "qualquer conta clássica num computador quântico.",
        "esfera": "Com um controle em superposição, o alvo se emaranha e o vetor dele encolhe.",
        "relacoes": ["Toffoli·Toffoli = I", "Universal para a computação clássica reversível",
                     "Também chamada de CCX ou CCNOT"],
        "qiskit": "qc.ccx(0, 1, 2)",
    },
    "CZ": {
        "resumo": "Inverte a fase só de |11⟩.",
        "faz": "Se os dois qubits forem 1, a amplitude ganha um sinal de menos; nos outros casos, nada "
               "muda. É simétrica: não importa qual qubit é o controle. Não muda probabilidades, mas a "
               "marca aparece na interferência. É o oráculo da busca de Grover (fase 19).",
        "esfera": "Com os dois qubits em |+⟩, a CZ os emaranha e os dois vetores somem no centro.",
        "relacoes": ["CZ·CZ = I", "É um Z controlado", "Com H no alvo antes e depois, vira uma CNOT"],
        "qiskit": "qc.cz(0, 1)",
    },
    "Y": {
        "resumo": "Troca |0⟩ e |1⟩ e ainda ajusta a fase: |0⟩ vira i|1⟩ e |1⟩ vira −i|0⟩.",
        "faz": "É a terceira porta de Pauli, junto com X e Z. Como o X, inverte as probabilidades de 0 e "
               "1; como o Z, troca |+⟩ e |−⟩. Na prática, o Y faz o trabalho dos dois de uma vez: "
               "Y = i·X·Z.",
        "esfera": "Meia volta em torno do eixo y. Polos trocam de lugar e o eixo x se inverte.",
        "relacoes": ["Y·Y = I", "Y = i·X·Z", "H·Y·H = −Y: entre duas H, o Y continua um Y"],
        "qiskit": "qc.y(0)",
    },
    "SDG": {
        "resumo": "Multiplica a amplitude de |1⟩ por −i: a S ao contrário.",
        "faz": "A S† (S conjugada, ou S-adaga) é a inversa da S: gira a fase um quarto de volta no "
               "sentido negativo. α|0⟩ + β|1⟩ vira α|0⟩ − iβ|1⟩. Toda porta quântica tem uma inversa, e "
               "o † é o símbolo dela.",
        "esfera": "90° em torno do eixo z, no sentido contrário ao da S: do eixo x para o −y.",
        "relacoes": ["S·S† = I: uma desfaz a outra", "S† = S·S·S", "T†·T† = S†"],
        "qiskit": "qc.sdg(0)",
    },
    "TDG": {
        "resumo": "Multiplica a amplitude de |1⟩ por e^(−iπ/4): a T ao contrário.",
        "faz": "A T† é a inversa da T: um oitavo de volta de fase no sentido negativo. Junto com H, T e "
               "CNOT, ela aparece em quase toda receita de circuito em computadores quânticos reais.",
        "esfera": "45° em torno do eixo z, no sentido contrário ao da T.",
        "relacoes": ["T·T† = I", "T†·T† = S†", "Oito T† dão uma volta inteira"],
        "qiskit": "qc.tdg(0)",
    },
    "SX": {
        "resumo": "Um quarto de volta em torno do eixo x: duas √X formam um X.",
        "faz": "Leva |0⟩ a (|0⟩ − i|1⟩)/√2, a menos de uma fase global: 50% de chance para cada "
               "resultado, como a H, mas num ponto diferente do equador. É uma das portas nativas de "
               "computadores quânticos reais, como os da IBM.",
        "esfera": "90° em torno do eixo x. Do polo norte, o qubit vai para o lado negativo do eixo y.",
        "relacoes": ["√X·√X = X", "H·S·H = √X (a menos de uma fase global)",
                     "Quatro √X dão uma volta inteira"],
        "qiskit": "qc.sx(0)",
    },
    "SWAP": {
        "resumo": "Troca o estado de dois qubits.",
        "faz": "|01⟩ vira |10⟩ e |10⟩ vira |01⟩; |00⟩ e |11⟩ ficam como estão. Como é uma porta "
               "quântica, troca o estado inteiro, com superposição e fase. Em chips reais, só qubits "
               "vizinhos conversam, e a SWAP é usada para levar um qubit até o outro.",
        "esfera": "Os dois vetores trocam de esfera. No meio do caminho, eles encolhem.",
        "relacoes": ["SWAP·SWAP = I", "Três CNOTs alternando o controle formam uma SWAP",
                     "É simétrica: tanto faz qual qubit vem primeiro"],
        "qiskit": "qc.swap(0, 1)",
    },
    "ISWAP": {
        "resumo": "Troca dois qubits e dá um i de fase quando eles são diferentes.",
        "faz": "|01⟩ vira i|10⟩ e |10⟩ vira i|01⟩; |00⟩ e |11⟩ não mudam. Com entradas da base, "
               "o i é só uma fase global e o resultado parece uma SWAP. Com superposição, a fase "
               "aparece: |+⟩|0⟩ vira |0⟩|+i⟩.",
        "esfera": "Os vetores trocam de esfera e o que chega gira um quarto de volta em z.",
        "relacoes": ["iSWAP = SWAP + CZ + S nos dois qubits", "iSWAP·iSWAP = Z⊗Z, não a identidade",
                     "Quatro iSWAP dão a identidade"],
        "qiskit": "qc.iswap(0, 1)",
    },
    "CSWAP": {
        "resumo": "Se o controle for 1, troca os outros dois qubits.",
        "faz": "Também chamada de porta de Fredkin. O primeiro qubit é o controle; os outros dois só "
               "trocam de lugar se ele for 1. Assim como a Toffoli, é universal para a computação "
               "clássica reversível, e a quantidade de 1s nunca muda.",
        "esfera": "Com o controle em superposição, os três qubits se emaranham.",
        "relacoes": ["CSWAP·CSWAP = I", "É uma SWAP controlada",
                     "Mantém o número de 1s: |101⟩ vira |110⟩"],
        "qiskit": "qc.cswap(0, 1, 2)",
    },
    "CY": {
        "resumo": "Se o controle for 1, aplica Y no alvo.",
        "faz": "Uma porta controlada genérica: bolinha no controle, caixa com a letra no alvo. "
               "Com o controle em 0, nada muda; em 1, o alvo recebe um Y: |10⟩ vira i|11⟩ e |11⟩ "
               "vira −i|10⟩. Com o controle em |+⟩, gera o Bell com fase (|00⟩ + i|11⟩)/√2.",
        "esfera": "Com o controle em |+⟩, os dois qubits se emaranham e os vetores encolhem.",
        "relacoes": ["CY·CY = I", "S† no alvo, CNOT, S no alvo = CY", "É um Y controlado"],
        "qiskit": "qc.cy(0, 1)",
    },
    "CH": {
        "resumo": "Se o controle for 1, aplica H no alvo.",
        "faz": "Com o controle em 1, o alvo entra em superposição; com 0, nada acontece. Com o "
               "controle em |+⟩ e o alvo em |0⟩, o resultado é |00⟩/√2 + |10⟩/2 + |11⟩/2: "
               "probabilidades de 50%, 25% e 25%. É um jeito de criar superposições desiguais.",
        "esfera": "Com o controle em |+⟩, o alvo vai só até o meio do caminho: emaranhamento parcial.",
        "relacoes": ["CH·CH = I", "É um H controlado", "Probabilidades desiguais: 50%, 25%, 25%"],
        "qiskit": "qc.ch(0, 1)",
    },
    "CCZ": {
        "resumo": "Inverte a fase só de |111⟩.",
        "faz": "A CZ com dois controles. Só o |111⟩ ganha um sinal de menos, e por isso ela é "
               "simétrica: os três fios ganham uma bolinha, sem caixa. Não muda probabilidades "
               "sozinha, mas é o oráculo da busca de Grover com 3 qubits.",
        "esfera": "Com os três qubits em |+⟩, eles se emaranham e os vetores encolhem.",
        "relacoes": ["CCZ·CCZ = I", "H no alvo, CCZ, H no alvo = Toffoli",
                     "Simétrica: tanto faz qual qubit é o alvo"],
        "qiskit": "qc.ccz(0, 1, 2)",
    },
    "RX": {
        "resumo": "Um quarto de volta em torno do eixo x.",
        "faz": "Rx(θ) gira o vetor θ radianos em torno do eixo x; no jogo, θ = π/2. Leva |0⟩ a "
               "(|0⟩ − i|1⟩)/√2, como a √X. As rotações são o jeito mais comum de descrever portas "
               "em computadores reais: o ângulo é ajustado por um pulso de micro-ondas.",
        "esfera": "90° em torno do eixo x: do polo norte para o lado negativo do eixo y.",
        "relacoes": ["Rx(π/2) = √X, a menos de uma fase global", "Duas Rx(π/2) = X, a menos de fase",
                     "Quatro Rx(π/2) = −I: uma volta inteira troca o sinal"],
        "qiskit": "qc.rx(pi / 2, 0)",
    },
    "RY": {
        "resumo": "Um quarto de volta em torno do eixo y.",
        "faz": "Ry(θ) gira o vetor θ radianos em torno do eixo y; no jogo, θ = π/2. A matriz só tem "
               "números reais. Leva |0⟩ a |+⟩ e |+⟩ a |1⟩: é o giro mais simples para criar "
               "superposições sem fase complexa.",
        "esfera": "90° em torno do eixo y: do polo norte para o eixo x.",
        "relacoes": ["Z, depois Ry(π/2) = H", "Duas Ry(π/2) = Y, a menos de uma fase global",
                     "Quatro Ry(π/2) = −I"],
        "qiskit": "qc.ry(pi / 2, 0)",
    },
    "RZ": {
        "resumo": "Um quarto de volta em torno do eixo z.",
        "faz": "Rz(θ) gira θ radianos em torno do eixo z; no jogo, θ = π/2. Multiplica |0⟩ por "
               "e^(−iπ/4) e |1⟩ por e^(iπ/4). Como a fase relativa é i, faz o mesmo que a S, a "
               "menos de uma fase global.",
        "esfera": "90° em torno do eixo z: |+⟩ vai para |+i⟩. Os polos não se mexem.",
        "relacoes": ["Rz(π/2) = S, a menos de uma fase global", "H, Rz(π/2), H = Rx(π/2)",
                     "Quatro Rz(π/2) = −I"],
        "qiskit": "qc.rz(pi / 2, 0)",
    },
    "P": {
        "resumo": "Multiplica a amplitude de |1⟩ por e^(iθ); no jogo, θ = π/2.",
        "faz": "A porta de fase. Não toca no |0⟩ e gira a fase de |1⟩ pelo ângulo θ. Com θ = π/2 é "
               "exatamente a S. Ela reúne numa família só várias portas do jogo: Z, S e T são P(π), "
               "P(π/2) e P(π/4).",
        "esfera": "90° em torno do eixo z, igual à S.",
        "relacoes": ["P(π/2) = S, P(π/4) = T, P(π) = Z", "Duas P(π/2) = Z",
                     "Rz(θ) = P(θ) vezes a fase global e^(−iθ/2)"],
        "qiskit": "qc.p(pi / 2, 0)",
    },
    "CP": {
        "resumo": "Se os dois qubits forem 1, multiplica a amplitude por i.",
        "faz": "A P(π/2) controlada, ou seja, a S controlada. Só o |11⟩ muda: ganha um i. Como a CZ, "
               "é simétrica. Fases controladas como essa são a peça principal da transformada de "
               "Fourier quântica, usada no algoritmo de Shor.",
        "esfera": "Com os dois qubits em |+⟩, eles se emaranham e os vetores encolhem.",
        "relacoes": ["Duas CP(π/2) = CZ", "CP(π/2) = CRz(π/2) seguida de T no controle",
                     "Simétrica: tanto faz qual qubit é o controle"],
        "qiskit": "qc.cp(pi / 2, 0, 1)",
    },
    "CRZ": {
        "resumo": "Se o controle for 1, aplica Rz(π/2) no alvo.",
        "faz": "Parece a CP, mas não é. Com o controle em 1, |10⟩ ganha e^(−iπ/4) e |11⟩ ganha "
               "e^(iπ/4). A fase global da Rz virou uma fase do controle: a diferença entre CRz e "
               "CP é uma T no qubit de controle.",
        "esfera": "Com os dois qubits em |+⟩, eles se emaranham.",
        "relacoes": ["CRz(π/2) seguida de T no controle = CP(π/2)",
                     "Sozinhas, Rz e P são iguais; controladas, não",
                     "Quatro CRz(π/2) = Z no controle"],
        "qiskit": "qc.crz(pi / 2, 0, 1)",
    },
    "CRX": {
        "resumo": "Se o controle for 1, aplica Rx(π/2) no alvo.",
        "faz": "Com o controle em 1, o alvo gira um quarto de volta em torno do eixo x. Com o "
               "controle em |+⟩ e o alvo em |0⟩, as probabilidades ficam em 50%, 25% e 25%, com "
               "uma fase −i no |11⟩.",
        "esfera": "Com o controle em |+⟩, o alvo vai até o meio do caminho.",
        "relacoes": ["Duas CRx(π/2) = CNOT com S† no controle", "Quatro CRx(π/2) = Z no controle",
                     "Controlada, a fase global vira local"],
        "qiskit": "qc.crx(pi / 2, 0, 1)",
    },
    "CRY": {
        "resumo": "Se o controle for 1, aplica Ry(π/2) no alvo.",
        "faz": "Com o controle em 1, o alvo gira um quarto de volta em torno do eixo y. Com o alvo "
               "em |0⟩, o resultado é o mesmo da CH. Com o alvo em |1⟩, não: a H é um espelho e a "
               "Ry é um giro, e a diferença aparece no sinal.",
        "esfera": "Com o controle em |+⟩, o alvo vai até o meio do caminho.",
        "relacoes": ["Com o alvo em |0⟩, igual à CH", "Matriz só com números reais",
                     "Quatro CRy(π/2) = Z no controle"],
        "qiskit": "qc.cry(pi / 2, 0, 1)",
    },
    "RXX": {
        "resumo": "Gira os dois qubits ao mesmo tempo em torno de X⊗X.",
        "faz": "Rxx(θ) = e^(−iθ·X⊗X/2). Com θ = π/2, leva |00⟩ direto a um estado de Bell, numa porta "
               "só. É a porta nativa dos computadores de íons presos (Mølmer–Sørensen) e aparece em "
               "simulações do modelo de Ising.",
        "esfera": "Partindo de |00⟩, os dois vetores encolhem juntos até o centro: emaranhamento.",
        "relacoes": ["Rxx(π/2)|00⟩ = (|00⟩ − i|11⟩)/√2", "Rxx(π) = −i·X⊗X",
                     "H nos dois qubits antes e depois: Rzz vira Rxx"],
        "qiskit": "qc.rxx(pi / 2, 0, 1)",
    },
    "RYY": {
        "resumo": "Gira os dois qubits ao mesmo tempo em torno de Y⊗Y.",
        "faz": "Ryy(θ) = e^(−iθ·Y⊗Y/2). Como a Rxx, cria um estado de Bell a partir de |00⟩, mas com o "
               "sinal da fase trocado. Junto com Rxx e Rzz, forma o trio de interações entre spins.",
        "esfera": "Partindo de |00⟩, os dois vetores encolhem juntos até o centro.",
        "relacoes": ["Ryy(π/2)|00⟩ = (|00⟩ + i|11⟩)/√2", "Ryy(π) = −i·Y⊗Y",
                     "Rxx(π/2) e Ryy(π/2) juntas = iSWAP†, a troca com −i"],
        "qiskit": "qc.ryy(pi / 2, 0, 1)",
    },
    "RZZ": {
        "resumo": "Dá fases opostas a qubits iguais e diferentes.",
        "faz": "Rzz(θ) é diagonal: multiplica |00⟩ e |11⟩ por e^(−iθ/2), e |01⟩ e |10⟩ por e^(iθ/2). "
               "Não muda probabilidades, só fases. É a interação ZZ do modelo de Ising e a peça "
               "central do algoritmo de otimização QAOA.",
        "esfera": "Com os dois qubits em |+⟩, eles se emaranham e os vetores encolhem.",
        "relacoes": ["CNOT, Rz(θ) no alvo, CNOT = Rzz(θ)", "Rzz(π) = −i·Z⊗Z",
                     "Diagonal: não muda probabilidades"],
        "qiskit": "qc.rzz(pi / 2, 0, 1)",
    },
    "SQSWAP": {
        "resumo": "Metade de uma SWAP: duas formam uma troca completa.",
        "faz": "Assim como a √X é meio X, a √SWAP é meia troca. No meio do caminho, os qubits ficam "
               "emaranhados: |10⟩ vira uma superposição de |10⟩ e |01⟩. Com √SWAP e portas de um "
               "qubit dá para montar qualquer circuito. É natural em qubits de spin.",
        "esfera": "Partindo de |10⟩, os dois vetores encolhem até o centro: os qubits se emaranham.",
        "relacoes": ["√SWAP·√SWAP = SWAP", "√SWAP, Z no 1º qubit, √SWAP, S e S† = CZ",
                     "Em |01⟩ e |10⟩, igual à Rxx(π/2); em |00⟩, não"],
        "qiskit": "qc.append(SwapGate().power(1 / 2), [0, 1])",
    },
    "U": {
        "resumo": "A porta geral de um qubit, aqui com os ângulos (π/2, 0, π).",
        "faz": "U(θ, φ, λ) descreve qualquer porta de um qubit com três ângulos: θ diz o quanto o vetor "
               "se afasta do polo, e φ e λ ajustam as fases. Toda porta de um qubit do jogo é uma U com "
               "os ângulos certos. Com (π/2, 0, π), ela trabalha igual à H.",
        "esfera": "Com U(π/2, 0, π), o polo norte vai para |+⟩, como na H.",
        "relacoes": ["U(π/2, 0, π) = H", "U(π, 0, π) = X e U(0, 0, π/2) = S",
                     "U(θ, −π/2, π/2) = Rx(θ) e U(0, 0, λ) = P(λ)"],
        "qiskit": "qc.u(pi / 2, 0, pi, 0)",
    },
    "UX": {
        "resumo": "A porta geral de um qubit, aqui com os ângulos (π, 0, π).",
        "faz": "A mesma porta U, com outros ângulos. Com θ = π, o vetor vai de um polo ao outro: é o "
               "X. A letra é a mesma da U(π/2, 0, π), mas os ângulos mudam tudo.",
        "esfera": "Meia volta: do polo norte ao polo sul, como no X.",
        "relacoes": ["U(π, 0, π) = X", "U(π, π/2, π/2) = Y", "U(π/2, 0, π) = H"],
        "qiskit": "qc.u(pi, 0, pi, 0)",
    },
    "US": {
        "resumo": "A porta geral de um qubit, aqui com os ângulos (0, 0, π/2).",
        "faz": "Com θ = 0, a U não afasta o vetor do polo: só gira a fase de |1⟩ pelo ângulo λ. É a "
               "porta P(λ). Com λ = π/2, trabalha igual à S; com λ = π/4, à T; com λ = π, ao Z.",
        "esfera": "Um quarto de volta em torno do eixo z, como na S.",
        "relacoes": ["U(0, 0, π/2) = S", "U(0, 0, π/4) = T e U(0, 0, π) = Z", "U(0, 0, λ) = P(λ)"],
        "qiskit": "qc.u(0, 0, pi / 2, 0)",
    },
    "CU": {
        "resumo": "Se o controle for 1, aplica U(π, 0, π) no alvo.",
        "faz": "Qualquer porta controlada de um alvo é uma CU com os ângulos certos. Com (π, 0, π), a U "
               "é um X, e a CU trabalha igual à CNOT. No Qiskit, a CU tem um quarto ângulo, γ, para a "
               "fase que o controle ganha.",
        "esfera": "Com o controle em |+⟩, a CU(π, 0, π) emaranha os qubits, como a CNOT.",
        "relacoes": ["CU(π, 0, π) = CNOT", "CU(π/2, 0, π) = CH", "CU(π, π/2, π/2) = CY"],
        "qiskit": "qc.cu(pi, 0, pi, 0, 0, 1)",
    },
    "CUH": {
        "resumo": "Se o controle for 1, aplica U(π/2, 0, π) no alvo.",
        "faz": "A mesma CU, com os ângulos (π/2, 0, π). A U dentro dela é uma H, então a CU trabalha "
               "igual à CH: com o controle em |+⟩ e o alvo em |0⟩, as probabilidades ficam em 50%, 25% "
               "e 25%.",
        "esfera": "Com o controle em |+⟩, o alvo vai só até o meio do caminho: emaranhamento parcial.",
        "relacoes": ["CU(π/2, 0, π) = CH", "CU(π, 0, π) = CNOT", "Duas CU(π/2, 0, π) = I"],
        "qiskit": "qc.cu(pi / 2, 0, pi, 0, 0, 1)",
    },
    "I": {
        "resumo": "Deixa o qubit exatamente como está.",
        "faz": "A identidade é a matriz que não muda nenhum estado. Parece inútil, mas aparece o tempo "
               "todo: é o que sobra quando uma porta encontra a sua inversa (X·X, H·H, S·S†), e nos "
               "computadores reais marca um intervalo em que o qubit só espera.",
        "esfera": "Nada se mexe: o vetor fica onde estava.",
        "relacoes": ["X·X = H·H = S·S† = I", "U(0, 0, 0) = I",
                     "Rx(2π) = −I: igual à I a menos de fase global"],
        "qiskit": "qc.id(0)",
    },
    "MCX": {
        "resumo": "Se todos os controles forem 1, inverte o alvo.",
        "faz": "A X multicontrolada generaliza a CNOT (1 controle) e a Toffoli (2 controles) para "
               "quantos controles se queira; o exemplo aqui tem 3. É o AND de muitas entradas, e "
               "aparece nos oráculos da busca de Grover com muitos qubits.",
        "esfera": "Com um controle em |+⟩ e os outros em 1, o alvo se emaranha com ele.",
        "relacoes": ["Com 1 controle é a CNOT; com 2, a Toffoli", "MCX·MCX = I",
                     "Com H no alvo antes e depois, vira uma Z multicontrolada"],
        "qiskit": "qc.mcx([0, 1, 2], 3)",
    },
}

# Portas que não aparecem nas fases, só na seção "Outras portas" do glossário.
# Têm os mesmos campos do GLOSSARIO, mais o subtítulo (elas não têm carta).
OUTRAS_PORTAS = {
}


def entrada_glossario(nome: str) -> dict:
    """Os textos de uma porta do glossário, seja do jogo ou da seção "Outras portas"."""
    return GLOSSARIO.get(nome) or OUTRAS_PORTAS[nome]


# Conceitos que aparecem no jogo, para consultar junto com as portas.
CONCEITOS = {
    "Qubit": "A unidade de informação quântica. Um bit clássico é 0 ou 1; um qubit pode estar em "
             "α|0⟩ + β|1⟩, onde α e β são números complexos chamados amplitudes, com |α|² + |β|² = 1. "
             "Ao medir, sai 0 com chance |α|² e 1 com chance |β|².",
    "Superposição": "Quando α e β são os dois diferentes de zero, o qubit está em superposição: não é 0 "
                    "nem 1 até ser medido. O exemplo mais comum é (|0⟩ + |1⟩)/√2, criado pela porta H, "
                    "com 50% de chance para cada resultado.",
    "Fase": "O sinal (ou, em geral, o ângulo complexo) de uma amplitude. (|0⟩ + |1⟩)/√2 e (|0⟩ − |1⟩)/√2 "
            "têm as mesmas probabilidades e diferem só na fase. Medir não revela a fase; a interferência "
            "revela. As portas Z, S e T mexem só na fase.",
    "Interferência": "Amplitudes se somam como ondas: com o mesmo sinal se reforçam, com sinais opostos se "
                     "cancelam. É o motor dos algoritmos quânticos: o circuito é montado para que as "
                     "respostas erradas se cancelem e a certa se reforce. Exemplo: H seguida de H devolve "
                     "|0⟩, porque as duas contribuições para |1⟩ se cancelam.",
    "Emaranhamento": "Quando o estado de dois ou mais qubits não pode ser descrito qubit por qubit. No "
                     "estado de Bell (|00⟩ + |11⟩)/√2, cada qubit sozinho é 50/50, mas os dois sempre dão "
                     "o mesmo resultado. Na esfera de Bloch, o vetor de um qubit emaranhado encolhe.",
    "Medição": "Ler o qubit. O resultado é sorteado com as probabilidades |α|² e |β|², e depois o estado "
               "colapsa para o resultado obtido: a superposição se perde. Por isso o Modo Colapso só "
               "deixa espiar uma vez.",
    "Esfera de Bloch": "Um jeito de desenhar o estado de um qubit como um ponto numa esfera: |0⟩ no polo "
                       "norte, |1⟩ no polo sul e as superposições iguais no equador. A altura dá as "
                       "probabilidades, e o ângulo em volta do eixo z dá a fase. Toda porta de um qubit "
                       "é uma rotação dessa esfera.",
    "Oráculo": "Uma caixa-preta que calcula uma função f e escreve o resultado num qubit extra. Nos "
               "algoritmos, o oráculo é consultado com as entradas em superposição, todas de uma vez. "
               "Com o qubit extra em |−⟩, a resposta vira uma fase. Fases 18, 83, 84, 85 e 86.",
    "Retorno de fase": "Quando o alvo de uma porta controlada está num estado que a porta não muda (só "
                       "ganha um sinal ou uma fase), essa fase vai para o controle. É o truque por trás "
                       "de Deutsch, Grover e da estimativa de fase. Fases 74, 89 e 90.",
    "Codificação superdensa": "Com um par de Bell dividido, Alice manda dois bits clássicos enviando um "
                              "qubit só: nada, X, Z ou X e Z viram 00, 01, 10 ou 11. Bob desfaz o par "
                              "com CNOT e H e lê os dois bits. Fases 87 e 91.",
    "Transformada de Fourier quântica": "A QFT leva cada número x a um estado em que as fases giram no "
                                        "ritmo de x. Com dois qubits: H, uma fase controlada de π/2, H e "
                                        "uma SWAP. É o coração do algoritmo de Shor. Fase 88.",
    "Estimativa de fase": "Descobre quanto uma porta gira a fase de um autoestado dela: o controle em "
                          "|+⟩, a porta controlada, e uma H (ou uma QFT inversa, com mais bits) para "
                          "transformar a fase em bits medidos. Fases 89 e 90.",
    "Troca de emaranhamento": "Dois pares de Bell, uma medição de Bell nos qubits do meio e correções: "
                              "os qubits das pontas ficam emaranhados sem nunca terem interagido. É a "
                              "base das redes quânticas de longa distância. Fase 92.",
}
