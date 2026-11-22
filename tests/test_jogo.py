"""Testes do jogo de ponta a ponta: navegação, bancada, progresso e som."""

import os

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import numpy as np
import pygame
import pytest

from qubit_lab.audio.sintese import sintetizar
from qubit_lab.core import Circuito, resolver


@pytest.fixture
def app(tmp_path, monkeypatch):
    monkeypatch.setenv("QUBIT_LAB_DADOS", str(tmp_path))
    from qubit_lab.app import App
    a = App()
    yield a
    pygame.quit()


def tecla(k):
    return pygame.event.Event(pygame.KEYDOWN, key=k, mod=0, unicode="", scancode=0)


def rodar_ate_terminar(app, bancada, limite=2000):
    for _ in range(limite):
        app.passo(1 / 60, eventos=[])
        if bancada.modo != "animando":
            return
    raise AssertionError("a animação não terminou")


def test_todas_as_fases_podem_ser_vencidas_pela_bancada(app):
    from qubit_lab.telas.bancada import Bancada
    for fase in app.fases:
        b = Bancada(app, fase.id)
        app.ir(b)
        for slot, nome in resolver(fase).melhor.items():
            b.selecionada = nome          # (selecionar() alterna: a mesma porta duas vezes desmarca)
            b.clicar_slot(slot)
        b.ativar()
        assert b.modo == "animando"
        rodar_ate_terminar(app, b)
        assert b.venceu, f"fase {fase.id} não foi vencida"
    assert app.progresso.concluidas == {f.id for f in app.fases}


def test_fase_errada_nao_vence_e_mostra_a_chance(app):
    from qubit_lab.telas.bancada import Bancada
    b = Bancada(app, 3)
    app.ir(b)
    b.selecionar("X")
    b.clicar_slot(1)
    b.ativar()
    rodar_ate_terminar(app, b)
    assert not b.venceu
    assert "50%" in b.mensagem
    assert 3 not in app.progresso.concluidas


def test_clicar_slot_cheio_sem_selecao_esvazia(app):
    from qubit_lab.telas.bancada import Bancada
    b = Bancada(app, 4)
    b.selecionar("Z")
    b.clicar_slot(1)
    assert b.fase.escolhas == {1: "Z"}
    b.selecionar("Z")              # clicar de novo na mesma porta desmarca
    b.clicar_slot(1)
    assert b.fase.escolhas == {}


def test_fluxo_pelo_teclado_menu_carta_bancada(app):
    from qubit_lab.telas.bancada import Bancada
    from qubit_lab.telas.carta import Carta
    app.passo(1 / 60, eventos=[tecla(pygame.K_RETURN)])        # Jogar → fase 1 apresenta o X
    assert isinstance(app.atual, Carta)
    app.passo(1 / 60, eventos=[tecla(pygame.K_RETURN)])        # Entendi → bancada
    assert isinstance(app.atual, Bancada)
    assert "X" in app.progresso.portas_vistas
    b = app.atual
    app.passo(1 / 60, eventos=[tecla(pygame.K_1)])             # escolhe X
    b.clicar_slot(0)
    app.passo(1 / 60, eventos=[tecla(pygame.K_RETURN)])        # Ativar
    rodar_ate_terminar(app, b)
    assert b.venceu
    app.passo(1 / 60, eventos=[tecla(pygame.K_RETURN)])        # Próxima fase → carta da H
    assert isinstance(app.atual, Carta) and app.atual.nome == "H"


def test_progresso_fica_salvo(app, tmp_path):
    from qubit_lab.progresso import Progresso
    app.progresso.concluir(1)
    app.progresso.ver_porta("X")
    novo = Progresso()
    assert novo.concluidas == {1} and "X" in novo.portas_vistas
    assert novo.liberada(2) and not novo.liberada(3)


def test_som_do_estado_tem_interferencia_de_verdade():
    sr = 44100
    quadros = Circuito(1).adicionar("H", [0]).adicionar("H", [0]).animar(30)
    x = sintetizar(quadros + [quadros[-1]] * 60, fps=60, sr=sr, cauda=0.2)
    assert x.shape[1] == 2 and np.max(np.abs(x)) <= 1

    def energia(trecho, f):
        espectro = np.abs(np.fft.rfft(trecho * np.hanning(len(trecho))))
        freqs = np.fft.rfftfreq(len(trecho), 1 / sr)
        return espectro[(freqs > f - 5) & (freqs < f + 5)].max()

    meio = x[int(0.45 * sr):int(0.55 * sr), 0]       # entre as duas H: acorde
    fim = x[int(1.3 * sr):int(1.6 * sr), 0]          # depois da segunda H: só o Lá
    assert energia(meio, 330) > 0.2 * energia(meio, 220)
    assert energia(fim, 330) < 0.05 * energia(fim, 220)


# ------------------------------------------------------------ Modo Colapso ---
def test_colapso_bloqueado_ate_a_fase_10(app):
    assert not app.progresso.colapso_liberado()
    app.progresso.concluir(10)
    assert app.progresso.colapso_liberado()


def test_colapso_esconde_o_estado_e_queima_vidas(app):
    from qubit_lab.colapso import SessaoColapso
    from qubit_lab.telas.bancada import Bancada
    app.progresso.portas_vistas.update({"X", "H", "Z"})
    sessao = SessaoColapso()
    b = Bancada(app, 4, colapso=sessao)
    app.ir(b)
    assert b.escondido
    b.selecionada = "X"                     # errado: H·X·H = Z, o detector não acende
    b.clicar_slot(1)
    b.ativar()
    assert b.escondido                      # continua sob o gelo durante a animação
    rodar_ate_terminar(app, b)
    assert not b.venceu and sessao.vidas == 2
    assert not b.escondido                  # o gelo quebra para mostrar o erro
    b.selecionada = "Z"
    b.clicar_slot(1)
    b.ativar()
    rodar_ate_terminar(app, b)
    assert b.venceu and sessao.vidas == 3   # vidas renovadas
    assert app.progresso.recorde_colapso == 4
    assert 4 not in app.progresso.concluidas   # o Modo Colapso não mexe no progresso normal


def test_colapso_fim_de_jogo_volta_ao_inicio_do_capitulo(app):
    from qubit_lab.colapso import SessaoColapso, inicio_do_capitulo
    from qubit_lab.telas.bancada import Bancada
    app.progresso.portas_vistas.update({"X", "H", "Z", "CNOT", "S"})
    assert inicio_do_capitulo(5) == 4 and inicio_do_capitulo(18) == 15
    sessao = SessaoColapso()
    sessao.vidas = 1
    b = Bancada(app, 5, colapso=sessao)
    app.ir(b)
    b.ativar()                               # slots vazios: não acende
    rodar_ate_terminar(app, b)
    assert b.fim_de_jogo
    app.passo(1 / 60, eventos=[tecla(pygame.K_RETURN)])
    assert isinstance(app.atual, Bancada) and app.atual.fase.id == 4
    assert app.atual.colapso.vidas == 3


def test_espiar_mede_uma_vez_e_colapsa(app):
    from qubit_lab.colapso import SessaoColapso
    from qubit_lab.telas.bancada import Bancada
    b = Bancada(app, 2, colapso=SessaoColapso())
    b.selecionada = "H"
    b.clicar_slot(0)
    b.espiar()
    assert b.espiou and b.modo == "espiada"
    probs = b.estado_atual.probabilidades()
    assert sorted(probs.round(6)) == [0, 1]   # colapsou num ket da base
    b.espiar()                                # a segunda espiada não vale
    assert "uma única medição" in b.mensagem


# ------------------------------------------------------------------ Álbum ---
def test_album_abre_so_cartas_vistas(app):
    from qubit_lab.telas.album import Album
    from qubit_lab.telas.carta import Carta
    app.progresso.portas_vistas.add("H")
    album = Album(app)
    app.ir(album)
    clique = lambda r: pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=r.center)
    app.passo(1 / 60, eventos=[clique(album.cartoes["X"])])      # ainda não vista
    assert app.atual is album
    app.passo(1 / 60, eventos=[clique(album.cartoes["H"])])
    assert isinstance(app.atual, Carta) and app.atual.nome == "H"
    app.passo(1 / 60, eventos=[tecla(pygame.K_RETURN)])           # volta ao álbum
    assert app.atual is album


# ----------------------------------------------------------- explicações ---
def test_explicacao_aparece_mesmo_em_fase_concluida(app):
    from qubit_lab.telas.bancada import Bancada
    from qubit_lab.telas.carta import Carta
    from qubit_lab.telas.explicacao import Explicacao
    app.progresso.concluidas.update(range(1, 8))
    app.progresso.portas_vistas.update({"X", "H", "Z", "CNOT"})
    app.jogar(5)                                     # fase sem porta nova
    assert isinstance(app.atual, Explicacao)
    app.passo(1 / 60, eventos=[tecla(pygame.K_RETURN)])
    assert isinstance(app.atual, Bancada) and app.atual.fase.id == 5
    app.jogar(2)                                     # fase com porta nova, carta já vista
    assert isinstance(app.atual, Carta) and app.atual.nome == "H"
    for f in app.fases:                              # toda fase tem algum texto de explicação
        from qubit_lab.core.capitulos import porta_nova
        assert f.explicacao or porta_nova(f.id)


def test_botao_ajuda_volta_para_a_mesma_bancada(app):
    from qubit_lab.telas.bancada import Bancada
    from qubit_lab.telas.explicacao import Explicacao
    b = Bancada(app, 5)
    app.ir(b)
    b.selecionada = "X"
    b.clicar_slot(0)
    app.passo(1 / 60, eventos=[tecla(pygame.K_i)])
    assert isinstance(app.atual, Explicacao)
    app.passo(1 / 60, eventos=[tecla(pygame.K_RETURN)])
    assert app.atual is b and b.fase.escolhas == {0: "X"}   # nada se perdeu


def test_sem_explicacao_no_modo_colapso(app):
    from qubit_lab.colapso import SessaoColapso
    from qubit_lab.telas.bancada import Bancada
    b = Bancada(app, 5, colapso=SessaoColapso())
    app.ir(b)
    app.passo(1 / 60, eventos=[tecla(pygame.K_i)])
    assert app.atual is b


# -------------------------------------------------------------- glossário ---
def test_glossario_tem_todas_as_portas_do_jogo():
    from qubit_lab.core.capitulos import APRESENTACAO
    from qubit_lab.textos import CARTAS, GLOSSARIO
    assert set(GLOSSARIO) == set(APRESENTACAO)
    assert set(CARTAS) >= set(APRESENTACAO)
    for nome, g in GLOSSARIO.items():
        assert {"resumo", "faz", "esfera", "relacoes", "qiskit"} <= set(g), nome


def test_glossario_navega_e_volta_para_a_bancada(app):
    from qubit_lab.telas.bancada import Bancada
    from qubit_lab.telas.glossario import Glossario
    b = Bancada(app, 4)
    app.ir(b)
    b.selecionada = "Z"
    app.passo(1 / 60, eventos=[tecla(pygame.K_g)])
    g = app.atual
    assert isinstance(g, Glossario)
    assert g.itens[g.indice] == ("porta", "Z")         # abre na porta selecionada
    for _ in range(len(g.itens)):                       # percorre todas as entradas desenhando cada uma
        app.passo(1 / 60, eventos=[tecla(pygame.K_DOWN)])
    app.passo(1 / 60, eventos=[tecla(pygame.K_ESCAPE)])
    assert app.atual is b and b.selecionada == "Z"


def test_glossario_fechado_no_modo_colapso(app):
    from qubit_lab.colapso import SessaoColapso
    from qubit_lab.telas.bancada import Bancada
    b = Bancada(app, 4, colapso=SessaoColapso())
    app.ir(b)
    app.passo(1 / 60, eventos=[tecla(pygame.K_g)])
    assert app.atual is b


def test_glossario_md_esta_atualizado():
    """docs/GLOSSARIO.md precisa bater com qubit_lab/textos.py (rode ferramentas/gerar_glossario.py)."""
    from pathlib import Path
    from qubit_lab.textos import GLOSSARIO
    texto = (Path(__file__).resolve().parent.parent / "docs" / "GLOSSARIO.md").read_text(encoding="utf-8")
    from qubit_lab.textos import OUTRAS_PORTAS
    for g in list(GLOSSARIO.values()) + list(OUTRAS_PORTAS.values()):
        assert g["faz"] in texto
    assert "## Outras portas" not in texto              # todas as portas já estão nas fases


def test_lista_do_glossario_rola_e_nada_passa_do_painel(app):
    from qubit_lab.telas.glossario import AREA_ITENS, Glossario
    g = Glossario(app)
    app.ir(g)
    assert g.rolagem_maxima > 0                        # 18 itens não cabem de uma vez
    for k in range(len(g.itens)):                      # ao navegar, o item escolhido fica sempre visível
        g.selecionar(k)
        r = g._na_tela(g.rects[k])
        assert AREA_ITENS.top <= r.top and r.bottom <= AREA_ITENS.bottom, g.itens[k]
    g.selecionar(0)
    assert g.rolagem == 0


def test_toda_porta_de_varios_qubits_tem_desenho():
    from qubit_lab.core.portas import PORTAS
    from qubit_lab.ui.simbolos import formas
    for nome, p in PORTAS.items():
        if p.n_qubits > 1:
            assert len(formas(nome)) == p.n_qubits, nome
    # controladas novas ganham o desenho genérico sozinhas
    assert formas("CY") == ["controle", "caixa:Y"]
    assert formas("CCH") == ["controle", "controle", "caixa:H"]


def test_outras_portas_so_no_glossario(app):
    from qubit_lab.core.capitulos import APRESENTACAO
    from qubit_lab.core.portas import PORTAS
    from qubit_lab.telas.glossario import Glossario
    from qubit_lab.textos import CARTAS, GLOSSARIO, OUTRAS_PORTAS
    outras = set(OUTRAS_PORTAS)
    assert outras == set()                             # todas viraram fases (51–69)
    assert outras <= set(PORTAS)                       # o simulador conhece todas
    assert not outras & set(APRESENTACAO)              # mas nenhuma aparece nas fases...
    assert not outras & set(GLOSSARIO) and not outras & set(CARTAS)   # ...nem no álbum
    assert set(GLOSSARIO) | outras == set(PORTAS)      # toda porta do simulador está no glossário
    for nome, g in OUTRAS_PORTAS.items():
        assert {"subtitulo", "resumo", "faz", "esfera", "relacoes", "qiskit"} <= set(g), nome
    g = Glossario(app, selecionado="MCX")
    app.ir(g)
    assert g.itens[g.indice] == ("porta", "MCX")
    assert [t for _, t in g.secoes] == ["Portas", "Conceitos"]   # sem a seção vazia
    for _ in range(3):
        app.passo(1 / 60, eventos=[])                  # desenha a MCX (4 qubits) sem erro


def test_caixa_da_controlada_mostra_o_angulo_dela(monkeypatch):
    """A CU(π,0,π) mostra "π,0,π" na caixa, e não o ângulo do exemplo da U sozinha."""
    import pygame
    from qubit_lab.ui import simbolos
    vistos = []
    monkeypatch.setattr(simbolos, "caixa", lambda tela, cor, centro, nome, escala=1.0, fundo=None: vistos.append(nome))
    tela = pygame.Surface((200, 200))
    simbolos.desenhar_multi(tela, "CU", 100, [50, 150], (255, 255, 255))
    simbolos.desenhar_multi(tela, "CRX", 100, [50, 150], (255, 255, 255))
    simbolos.desenhar_multi(tela, "CY", 100, [50, 150], (255, 255, 255))
    assert vistos == [("U", "π,0,π"), ("Rx", "π/2"), ("Y", None)]


def test_toda_carta_abre_e_desenha(app):
    """A carta de toda porta abre sem erro (pegaria a trava da carta de 4 qubits da MCX)."""
    from qubit_lab.core.capitulos import APRESENTACAO
    from qubit_lab.telas.carta import Carta
    for nome, fase in APRESENTACAO.items():
        c = Carta(app, nome, fase)
        app.ir(c)
        for k in range(len(c.entradas)):               # testa cada botão do "Experimente"
            c.entrada = k
            app.passo(1 / 60, eventos=[])


def test_modo_de_teste_libera_tudo_sem_mexer_no_progresso(tmp_path, monkeypatch):
    from qubit_lab.progresso import Progresso
    normal = Progresso(tmp_path / "p.json")
    assert normal.liberada(1) and not normal.liberada(50) and not normal.colapso_liberado()
    monkeypatch.setenv("QUBIT_LAB_LIBERAR", "1")
    teste = Progresso(tmp_path / "p.json")
    assert teste.liberada(100) and teste.colapso_liberado()
    assert teste.concluidas == set()                    # nada foi marcado como concluído


def test_voltar_ao_menu_para_o_som_do_circuito(app, monkeypatch):
    """Bug: ativar o circuito e voltar ao menu deixava o som tocando."""
    from qubit_lab.telas.bancada import Bancada
    from qubit_lab.telas.menu import Menu
    paradas = []
    monkeypatch.setattr(app.audio, "parar_efeitos", lambda: paradas.append(True))
    b = Bancada(app, 1)
    app.ir(b)
    b.selecionada = "X"
    b.clicar_slot(b.fase.slots[0])
    b.ativar()                                          # o som do circuito começa
    paradas.clear()
    app.ir(Menu(app))                                   # volta ao menu no meio da animação
    assert paradas, "trocar de tela precisa parar o som"
    paradas.clear()
    app.ir(app.atual)                                   # "trocar" para a mesma tela não para nada
    assert not paradas


def test_parar_efeitos_mantem_o_ambiente():
    from qubit_lab.audio import Audio

    class SomFalso:
        def __init__(self):
            self.parado = False

        def stop(self):
            self.parado = True

    audio = Audio.__new__(Audio)                        # sem abrir o mixer de verdade
    audio.disponivel = True
    canal = SomFalso()
    audio._canal_estado = canal
    audio.sons = {"ambiente": SomFalso(), "detector": SomFalso(), "colapso": SomFalso()}
    audio.parar_efeitos()
    assert canal.parado and audio._canal_estado is None
    assert audio.sons["detector"].parado and audio.sons["colapso"].parado
    assert not audio.sons["ambiente"].parado            # a música de fundo continua
