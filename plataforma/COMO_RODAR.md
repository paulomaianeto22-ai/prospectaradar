# Como rodar a plataforma (MVP)

## 1. Instalar
cd plataforma
pip install -r requirements.txt

## 2. Rodar
uvicorn app.main:app --reload
# abre em http://localhost:8000

## Login admin (Paulo)
email: admin@prospecta.com   senha: admin123
(troque via variáveis ADMIN_EMAIL / ADMIN_SENHA)

## Fluxo de teste
1. /cadastro  -> cria conta de cliente (ganha 25 leads)
2. /pedir     -> pede leads (tipo, cidade, qtd)
3. (admin) entra em /admin -> roda o script, cola o CSV, "Entregar"
4. cliente vê em /historico -> /pedido/<id> -> marca o desfecho de cada lead
5. /extra     -> só libera +10 após feedback de todos + WhatsApp
