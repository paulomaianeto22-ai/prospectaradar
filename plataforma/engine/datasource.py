"""Interface de fonte de dados — TROCÁVEL.

O resto da plataforma SEMPRE chama isto, nunca o Google direto.
Trocar de fonte = trocar a linha SOURCE lá embaixo. Nada mais muda.
"""
from __future__ import annotations
from abc import ABC, abstractmethod


class DataSource(ABC):
    @abstractmethod
    def buscar(self, tipo_comercio: str, cidade: str, uf: str, quantidade: int) -> list[dict]:
        """Retorna lista de leads: [{empresa,cidade,telefone,celular,email,canal,
        website,situacao,porte,nota_google,avaliacoes,instagram}, ...]"""
        ...


class GoogleDataSource(DataSource):
    """AGORA (teste de 1 mês). Reusa os scripts existentes em ../sistema/scripts/.
    Só para uso interno/admin — NÃO expor a chave do Google ao cliente.
    ATENÇÃO: usar Google p/ redistribuir viola os termos; é temporário/validação."""
    def buscar(self, tipo_comercio, cidade, uf, quantidade):
        # TODO (dev): chamar o pipeline existente (coletar_e_qualificar) com estes
        # parâmetros e devolver a lista já no formato acima.
        raise NotImplementedError("Ligar ao pipeline em ../sistema (Fase 1).")


class CnpjDataSource(DataSource):
    """DEPOIS — Opção B (legal p/ escala): base aberta do CNPJ + enriquecimento."""
    def buscar(self, tipo_comercio, cidade, uf, quantidade):
        raise NotImplementedError("Implementar na migração p/ fonte legal.")


# >>> A ÚNICA linha que muda ao trocar de fonte <<<
SOURCE: DataSource = GoogleDataSource()
