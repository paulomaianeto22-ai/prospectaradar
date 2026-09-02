"""Modelos do banco (SQLModel) — MVP ProspectaRadar."""
from __future__ import annotations
from datetime import datetime
from typing import Optional
import uuid
from sqlmodel import SQLModel, Field


def _uid() -> str:
    return str(uuid.uuid4())


class User(SQLModel, table=True):
    id: str = Field(default_factory=_uid, primary_key=True)
    nome: str
    email: str = Field(index=True, unique=True)
    senha_hash: str
    email_verificado: bool = True   # MVP: já verificado (email real = Fase 1)
    is_admin: bool = False
    plano: str = "free"             # free | assinante
    leads_gratis_liberados: int = 25
    leads_gratis_usados: int = 0
    criado_em: datetime = Field(default_factory=datetime.utcnow)


class LeadRequest(SQLModel, table=True):
    id: str = Field(default_factory=_uid, primary_key=True)
    user_id: str = Field(index=True)
    tipo_comercio: str
    cidade: str
    uf: str
    quantidade: int
    status: str = "pendente"        # pendente | processando | entregue
    criado_em: datetime = Field(default_factory=datetime.utcnow)
    entregue_em: Optional[datetime] = None


class Lead(SQLModel, table=True):
    id: str = Field(default_factory=_uid, primary_key=True)
    request_id: str = Field(index=True)
    user_id: str = Field(index=True)
    empresa: str = ""
    cidade: str = ""
    telefone: str = ""
    email: str = ""
    canal: str = ""
    website: str = ""
    situacao: str = ""
    porte: str = ""
    instagram: str = ""
    nota_google: str = ""
    avaliacoes: str = ""


class LeadFeedback(SQLModel, table=True):
    id: str = Field(default_factory=_uid, primary_key=True)
    lead_id: str = Field(index=True, unique=True)
    user_id: str = Field(index=True)
    status: str = "nao_contatado"
    # nao_contatado|contatado|respondeu|em_negociacao|fechou|sem_interesse|contato_errado
    observacao: str = ""
    atualizado_em: datetime = Field(default_factory=datetime.utcnow)


class Grant(SQLModel, table=True):
    id: str = Field(default_factory=_uid, primary_key=True)
    user_id: str = Field(index=True)
    quantidade: int
    motivo: str = ""
    criado_em: datetime = Field(default_factory=datetime.utcnow)
