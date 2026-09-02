# Contrato da API (resumo) — detalhe no ../../Blueprint_Plataforma_MVP.md §3

POST /auth/signup        {nome,email,senha}
POST /auth/verify        {token}
POST /auth/login         {email,senha}
GET  /me                 -> {plano, leads_restantes, precisa_feedback}
POST /requests           {tipo_comercio,cidade,uf,quantidade}   (valida cota)
GET  /requests           -> histórico
GET  /requests/:id/leads -> leads do pedido
PUT  /leads/:id/feedback {status,observacao}
POST /requests/extra     -> só se lote anterior 100% com feedback (dispara WhatsApp)
-- admin --
GET  /admin/requests?status=pendente
POST /admin/requests/:id/leads          (upload dos leads gerados -> entregue)
POST /admin/users/:id/grant {quantidade,motivo}   (+10)
