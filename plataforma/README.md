# ProspectaRadar — Scaffold do MVP (stack-neutro)

Estrutura inicial pra o dev construir a plataforma. A stack é livre;
aqui estão as peças que **independem** de framework.

## Mapa
- `db/schema.sql`         → banco (Postgres) — roda direto no Supabase ou qualquer Postgres
- `engine/datasource.py`  → interface de dados TROCÁVEL (Google agora, CNPJ depois)
- `api/CONTRACT.md`       → contrato dos endpoints (resumo; detalhe no Blueprint)
- `frontend/`             → telas: leads.html (= Lead Viewer), cadastro/pedido (stubs)
- `../Blueprint_Plataforma_MVP.md` → o blueprint completo (dados, API, fluxo)
- `../PRD_ProspectaRadar_MVP.md`   → o PRD (escopo, regras, porquê)

## Motor de coleta (Mágico de Oz)
No MVP o admin roda os scripts que já existem em `../sistema/scripts/`
(`prospectar_radar.py`, `buscar.py`) e sobe os leads pela rota admin.
A automação (chamar via DataSource) é Fase 1.

## Cores da marca
roxo #5B1FA0 · roxo escuro #43167A · laranja #F97316 · lilás #F5F1FB · texto #1F2733
