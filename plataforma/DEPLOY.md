# Publicar a plataforma (link permanente) — Render (grátis)

## 1. Suba o código pro GitHub
- Crie um repositório (github.com > New)
- Suba a pasta `plataforma/` (pode ser só ela)

## 2. Crie um banco Postgres (o SQLite reseta na nuvem)
Opção A — Supabase (grátis): crie projeto > Settings > Database > copie a "Connection string".
Opção B — Render: New > PostgreSQL (free) > copie a "Internal Database URL".
> Formato: postgresql://usuario:senha@host:5432/banco

## 3. Deploy no Render
- render.com > New > Web Service > conecte seu GitHub
- Root Directory: `plataforma`
- Build: `pip install -r requirements.txt`
- Start: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Em "Environment", adicione:
  - DATABASE_URL   = (a connection string do passo 2)
  - ADMIN_EMAIL    = seu email
  - ADMIN_SENHA    = uma senha forte
  - SECRET_KEY     = (deixe o Render gerar / qualquer texto aleatório longo)
  - WHATSAPP_SUPORTE = seu numero (ex: 5541999999999)
- Clique Create Web Service.

## 4. Pronto
Em ~2 min você tem: https://prospectaradar.onrender.com
Esse é o link que você manda pros clientes.

## Depois (opcional)
- Domínio próprio (prospectaradar.com.br) → aponta pro Render nas configs de domínio.
