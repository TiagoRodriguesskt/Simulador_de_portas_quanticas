# Qubit Lab — Documento de design

Referência visual e sonora do jogo. Qualquer tela ou som novo deve seguir este documento.

## Conceito

**Laboratório criogênico.** O jogador trabalha dentro de um computador quântico real: um refrigerador de diluição, com placas douradas em temperaturas cada vez mais baixas (50 K → 10 mK) e o chip do qubit brilhando no fundo. Frio, preciso, científico, mas acolhedor.

## Paleta

| Uso | Cor | Hex |
|---|---|---|
| Fundo (vácuo do criostato) | Azul quase preto | `#060B14` |
| Painéis e placas | Azul aço escuro | `#101C2C` |
| Bordas sutis | Azul aço | `#1B2A3E` |
| Estrutura do lustre, fios do circuito | Cobre | `#C2703D` |
| Títulos, portas, botão principal | Ouro | `#E8B85C` |
| Estado \|0⟩, gelo, brilho frio | Ciano gelo | `#7FE3FF` |
| Estado \|1⟩, energia | Âmbar quente | `#FF9A3C` |
| Texto | Branco gelo | `#E6F1FA` |
| Texto secundário | Cinza azulado | `#A9BBD0` / `#8FA6BF` |
| Erro, colapso, vida queimada | Vermelho alerta | `#FF4D5E` |

**Regra de ouro:** ciano é sempre |0⟩ e âmbar é sempre |1⟩, em toda tela, barra, gráfico e esfera.

## Tipografia

- **IBM Plex Sans** para textos e títulos.
- **IBM Plex Mono** para notação (|ψ⟩, matrizes, temperaturas, contadores).
- Ambas têm licença livre (SIL Open Font License) e podem ir junto com o jogo em `assets/fontes/`.

## Telas

1. **Menu principal**: título em ouro, fórmula |ψ⟩ = α|0⟩ + β|1⟩ acima, botões (Jogar, Modo Colapso, Álbum de portas, Som) e o lustre animado à direita.
2. **Bancada (fase)**: esfera de Bloch à esquerda, circuito ao centro com slots e bandeja de portas, detector à direita, dica no rodapé.
3. **Carta de porta nova**: carta colecionável (símbolo, matriz, identidades) e painéis de analogia, rotação na esfera, som e mini demonstração.
4. **Álbum**: as cartas já conquistadas.
5. **Modo Colapso**: esferas cobertas de gelo; espiar quebra o gelo e colapsa o estado.

Os mockups das três primeiras telas estão no canvas de design do projeto.

## Sons

| Arquivo | Quando toca | O que representa |
|---|---|---|
| `01_estado_0.wav` | Qubit em \|0⟩ | Lá, 220 Hz |
| `02_estado_1.wav` | Qubit em \|1⟩ | Mi, 330 Hz (a quinta) |
| `03_hadamard_superposicao.wav` | Porta H | Uma nota vira acorde |
| `04_interferencia_HH.wav` | H seguida de H | O Mi aparece e se cancela |
| `05_fase_Z_revelada.wav` | H, Z, H | A fase muda o resultado final |
| `06_colapso.wav` | Medição | Vidro quebrando, sobra uma nota |
| `07_emaranhamento.wav` | CNOT | Duas vozes pulsando juntas |
| `08_detector_acende.wav` | Fase vencida | Arpejo de sinos de vidro |
| `09_ambiente_criostato.wav` | Fundo, em loop | Zumbido elétrico e o "suspiro" do pulse-tube |

**Princípio:** o áudio é o estado. `s(t) = Σ Re(aₖ(t) · Wₖ(t))`, com cada porta animada como rotação contínua na esfera de Bloch. Assim, interferência e fase acontecem de verdade no som.

## Momentos de assinatura

- **Modo Colapso** no lugar de um "modo difícil": a regra do jogo é a regra da física.
- **Detector acendendo** com uma onda de luz e o arpejo de vidro.
- **Cartas de porta** colecionáveis, com álbum.
