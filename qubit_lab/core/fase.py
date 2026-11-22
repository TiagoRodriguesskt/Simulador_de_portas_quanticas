"""Fases do jogo: lidas de arquivos JSON.

Exemplo (fase 4, "Interferência"):

    {
      "id": 4,
      "titulo": "Interferência",
      "qubits": 1,
      "circuito": [
        {"porta": "H", "alvos": [0]},
        {"slot": true, "alvos": [0]},
        {"porta": "H", "alvos": [0]}
      ],
      "disponiveis": ["X", "Z"],
      "objetivo": {"tipo": "probabilidade", "ket": "1"},
      "dica": "O Z não muda as probabilidades… mas e a segunda H?"
    }

- Passos com "porta" já vêm colocados e não podem ser mexidos.
- Passos com "slot": true são os espaços que o jogador preenche com uma das
  portas "disponiveis" (ou deixa vazio).
- Objetivos:
    {"tipo": "probabilidade", "ket": "1", "minimo": 1.0}
        → medir |1⟩ com pelo menos 100% de chance (o padrão é 1.0)
    {"tipo": "estado", "alvo": [1, 1]}
        → chegar ao estado (|0⟩+|1⟩)/√2; o vetor é normalizado sozinho,
          e números complexos podem ser escritos como [real, imaginário]
    {"tipo": "qubit", "qubit": 0, "valor": 1}
        → medir SÓ o qubit 0 e obter 1 com 100% (os outros não importam)
    {"tipo": "bloch", "qubit": 2, "alvo": [1, 1]}
        → deixar o qubit 2 sozinho no estado alvo (os outros não importam);
          usado no teleporte
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

from .circuito import Circuito
from .estado import Estado

TOLERANCIA = 1e-6


@dataclass(frozen=True)
class Slot:
    alvos: tuple


@dataclass
class Objetivo:
    tipo: str                     # "probabilidade", "estado", "qubit" ou "bloch"
    ket: str | None = None
    minimo: float = 1.0
    alvo: Estado | None = None
    qubit: int = 0
    valor: int = 1
    formula: str = ""             # opcional: o alvo escrito à mão, para estados longos (16 termos)

    def chance(self, estado: Estado) -> float:
        """Quão perto o estado está do objetivo, de 0 a 1."""
        if self.tipo == "probabilidade":
            return estado.probabilidade(self.ket)
        if self.tipo == "qubit":
            return estado.probabilidade_qubit(self.qubit, self.valor)
        if self.tipo == "bloch":
            # ⟨alvo|ρ|alvo⟩: fidelidade entre o qubit (talvez emaranhado) e o alvo
            rho = estado.matriz_reduzida(self.qubit)
            v = self.alvo.vetor
            return float(np.real(np.conj(v) @ rho @ v))
        return estado.fidelidade(self.alvo)

    @property
    def ket_detector(self) -> str:
        """O rótulo que aparece no detector."""
        if self.tipo == "probabilidade":
            return f"|{self.ket}⟩"
        if self.tipo == "qubit":
            return f"q{self.qubit}={self.valor}"
        return "alvo"

    def cumprido(self, estado: Estado) -> bool:
        return self.chance(estado) >= self.minimo - TOLERANCIA

    def descrever(self) -> str:
        from .estado import formatar
        if self.tipo == "probabilidade":
            return f"Medir |{self.ket}⟩ com {self.minimo:.0%} de certeza"
        if self.tipo == "qubit":
            return f"Medir o qubit {self.qubit} e obter {self.valor} com {self.minimo:.0%} de certeza"
        if self.tipo == "bloch":
            return f"Deixar o qubit {self.qubit} no estado {formatar(self.alvo.vetor)}"
        return f"Chegar ao estado {self.formula_do_alvo()}"

    def formula_do_alvo(self) -> str:
        """O estado-alvo em notação de Dirac; a `formula` da fase, se houver (só o texto muda)."""
        from .estado import formatar
        return self.formula or formatar(self.alvo.vetor)


@dataclass
class Fase:
    id: int
    titulo: str
    n_qubits: int
    passos: list                  # mistura de Passo (fixo) e Slot (do jogador)
    disponiveis: list[str]
    objetivo: Objetivo
    dica: str = ""
    explicacao: str = ""          # texto da tela de explicação antes da fase
    completo: bool = False        # True: só vence com todos os slots preenchidos (fase da I)
    max_portas: int | None = None  # orçamento: só vence quem usar no máximo essa quantidade de portas
    escolhas: dict = field(default_factory=dict)   # índice do slot → porta escolhida

    # -------------------------------------------------------- leitura ---
    @classmethod
    def de_dict(cls, dados: dict) -> Fase:
        from .circuito import Passo

        n = int(dados["qubits"])
        passos = []
        for item in dados["circuito"]:
            alvos = tuple(item["alvos"])
            passos.append(Slot(alvos) if item.get("slot") else Passo(item["porta"], alvos))

        obj = dados["objetivo"]
        if obj["tipo"] == "probabilidade":
            objetivo = Objetivo("probabilidade", ket=obj["ket"], minimo=obj.get("minimo", 1.0))
        elif obj["tipo"] in ("estado", "bloch"):
            amps = [complex(*a) if isinstance(a, list) else a for a in obj["alvo"]]
            objetivo = Objetivo(obj["tipo"], alvo=Estado(amps), minimo=obj.get("minimo", 1.0),
                                qubit=obj.get("qubit", 0), formula=obj.get("formula", ""))
        elif obj["tipo"] == "qubit":
            objetivo = Objetivo("qubit", qubit=obj["qubit"], valor=obj.get("valor", 1),
                                minimo=obj.get("minimo", 1.0))
        else:
            raise ValueError(f"Tipo de objetivo desconhecido: {obj['tipo']!r}")

        return cls(
            id=int(dados["id"]),
            titulo=dados.get("titulo", ""),
            n_qubits=n,
            passos=passos,
            disponiveis=list(dados["disponiveis"]),
            objetivo=objetivo,
            dica=dados.get("dica", ""),
            explicacao=dados.get("explicacao", ""),
            completo=bool(dados.get("completo", False)),
            max_portas=dados.get("max_portas"),
        )

    @classmethod
    def de_arquivo(cls, caminho) -> Fase:
        with open(caminho, encoding="utf-8") as f:
            return cls.de_dict(json.load(f))

    # ----------------------------------------------------------- jogo ---
    @property
    def slots(self) -> list[int]:
        """Índices (em `passos`) dos espaços que o jogador preenche."""
        return [i for i, p in enumerate(self.passos) if isinstance(p, Slot)]

    def escolher(self, indice_slot: int, nome_porta: str | None):
        """Coloca uma porta num slot (ou tira, com None)."""
        if indice_slot not in self.slots:
            raise ValueError(f"O passo {indice_slot} não é um slot.")
        if nome_porta is None:
            self.escolhas.pop(indice_slot, None)
        elif nome_porta not in self.disponiveis:
            raise ValueError(f"A porta {nome_porta} não está disponível nesta fase.")
        else:
            self.escolhas[indice_slot] = nome_porta

    def circuito(self, escolhas: dict | None = None) -> Circuito:
        """Monta o circuito com as portas fixas e as escolhas do jogador."""
        escolhas = self.escolhas if escolhas is None else escolhas
        c = Circuito(self.n_qubits)
        for i, p in enumerate(self.passos):
            if isinstance(p, Slot):
                if i in escolhas:
                    c.adicionar(escolhas[i], p.alvos)
            else:
                c.adicionar(p.porta, p.alvos)
        return c

    def resultado(self, escolhas: dict | None = None) -> Estado:
        return self.circuito(escolhas).executar()

    def faltam_slots(self, escolhas: dict | None = None) -> bool:
        """Numa fase "completo", True enquanto houver slot vazio."""
        escolhas = self.escolhas if escolhas is None else escolhas
        return self.completo and len(escolhas) < len(self.slots)

    def estourou_orcamento(self, escolhas: dict | None = None) -> bool:
        """Numa fase com orçamento, True se o jogador usou portas demais."""
        escolhas = self.escolhas if escolhas is None else escolhas
        return self.max_portas is not None and len(escolhas) > self.max_portas

    def venceu(self, escolhas: dict | None = None) -> bool:
        if self.faltam_slots(escolhas) or self.estourou_orcamento(escolhas):
            return False
        return self.objetivo.cumprido(self.resultado(escolhas))


def carregar_fases(pasta=None) -> list[Fase]:
    """Lê todos os NN.json da pasta de fases (assets/fases), em ordem."""
    from ..caminhos import recurso

    pasta = Path(pasta) if pasta else recurso("fases")
    # pelo número, não pelo nome: como texto, "100.json" viria antes de "20.json"
    return [Fase.de_arquivo(a) for a in sorted(pasta.glob("*.json"), key=lambda a: int(a.stem))]
