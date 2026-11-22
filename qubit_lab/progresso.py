"""Progresso do jogador, salvo num JSON na pasta do usuário."""

import json
import os

from .caminhos import pasta_progresso


class Progresso:
    def __init__(self, arquivo=None):
        self.arquivo = arquivo or (pasta_progresso() / "progresso.json")
        self.concluidas: set[int] = set()
        self.portas_vistas: set[str] = set()
        self.som = True
        self.recorde_colapso = 0          # fase mais alta vencida no Modo Colapso
        # modo de teste (python main.py --liberar): tudo liberado, sem mexer no progresso salvo
        self.tudo_liberado = os.environ.get("QUBIT_LAB_LIBERAR") == "1"
        self.carregar()

    def carregar(self):
        try:
            with open(self.arquivo, encoding="utf-8") as f:
                dados = json.load(f)
        except (OSError, ValueError):
            return                      # primeira vez jogando, ou arquivo corrompido
        self.concluidas = set(dados.get("concluidas", []))
        self.portas_vistas = set(dados.get("portas_vistas", []))
        self.som = bool(dados.get("som", True))
        self.recorde_colapso = int(dados.get("recorde_colapso", 0))

    def salvar(self):
        dados = {
            "concluidas": sorted(self.concluidas),
            "portas_vistas": sorted(self.portas_vistas),
            "som": self.som,
            "recorde_colapso": self.recorde_colapso,
        }
        try:
            with open(self.arquivo, "w", encoding="utf-8") as f:
                json.dump(dados, f, ensure_ascii=False, indent=2)
        except OSError:
            pass                        # sem permissão de escrita: o jogo segue

    def concluir(self, id_fase: int):
        self.concluidas.add(id_fase)
        self.salvar()

    def ver_porta(self, nome: str):
        self.portas_vistas.add(nome)
        self.salvar()

    def registrar_colapso(self, id_fase: int):
        if id_fase > self.recorde_colapso:
            self.recorde_colapso = id_fase
            self.salvar()

    def colapso_liberado(self) -> bool:
        from .colapso import FASE_LIBERA
        return self.tudo_liberado or FASE_LIBERA in self.concluidas

    def liberada(self, id_fase: int) -> bool:
        """Uma fase está liberada se for a 1 ou se a anterior foi concluída (ou no modo de teste)."""
        return self.tudo_liberado or id_fase == 1 or (id_fase - 1) in self.concluidas

    def proxima(self, total: int) -> int:
        """A primeira fase ainda não concluída (ou a última, se terminou tudo)."""
        for i in range(1, total + 1):
            if i not in self.concluidas:
                return i
        return total
