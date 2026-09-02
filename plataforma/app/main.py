"""ProspectaRadar — Plataforma MVP (FastAPI).

Fase 0 / Mágico de Oz: cliente pede leads; admin (Paulo) roda os scripts e
cola o CSV; cliente vê no painel e marca o feedback de cada lead.
"""
import os, csv, io
from datetime import datetime
from fastapi import FastAPI, Request, Depends, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from sqlmodel import Session, select

from app.db import engine, init_db, get_session
from app.models import User, LeadRequest, Lead, LeadFeedback, Grant
from app.security import hash_senha, verificar_senha

BASE = os.path.dirname(__file__)
app = FastAPI(title="ProspectaRadar")
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SECRET_KEY", "troque-isto-em-producao"))
templates = Jinja2Templates(directory=os.path.join(BASE, "templates"))

WHATSAPP = os.getenv("WHATSAPP_SUPORTE", "5541999999999")
STATUS_OPCOES = ["nao_contatado", "contatado", "respondeu", "em_negociacao",
                 "fechou", "sem_interesse", "contato_errado"]


@app.on_event("startup")
def _startup():
    init_db()
    # semeia um admin (edite via env ADMIN_EMAIL / ADMIN_SENHA)
    with Session(engine) as s:
        email = os.getenv("ADMIN_EMAIL", "admin@prospecta.com")
        if not s.exec(select(User).where(User.email == email)).first():
            s.add(User(nome="Admin", email=email,
                       senha_hash=hash_senha(os.getenv("ADMIN_SENHA", "admin123")),
                       is_admin=True))
            s.commit()


def atual(request: Request, s: Session) -> User | None:
    uid = request.session.get("user_id")
    return s.get(User, uid) if uid else None


def restantes(u: User) -> int:
    return max(0, u.leads_gratis_liberados - u.leads_gratis_usados)


# ---------------- AUTH ----------------
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return RedirectResponse("/pedir" if request.session.get("user_id") else "/login", 302)


@app.get("/cadastro", response_class=HTMLResponse)
def cadastro_get(request: Request):
    return templates.TemplateResponse(request, "cadastro.html", {})


@app.post("/cadastro")
def cadastro_post(request: Request, nome: str = Form(...), email: str = Form(...),
                  senha: str = Form(...), s: Session = Depends(get_session)):
    if s.exec(select(User).where(User.email == email)).first():
        return templates.TemplateResponse(request, "cadastro.html", {"erro": "Email já cadastrado."})
    u = User(nome=nome, email=email, senha_hash=hash_senha(senha))
    s.add(u); s.commit()
    request.session["user_id"] = u.id
    return RedirectResponse("/pedir", 302)


@app.get("/login", response_class=HTMLResponse)
def login_get(request: Request):
    return templates.TemplateResponse(request, "login.html", {})


@app.post("/login")
def login_post(request: Request, email: str = Form(...), senha: str = Form(...),
               s: Session = Depends(get_session)):
    u = s.exec(select(User).where(User.email == email)).first()
    if not u or not verificar_senha(senha, u.senha_hash):
        return templates.TemplateResponse(request, "login.html", {"erro": "Email ou senha inválidos."})
    request.session["user_id"] = u.id
    return RedirectResponse("/admin" if u.is_admin else "/pedir", 302)


@app.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/login", 302)


# ---------------- PEDIR LEADS ----------------
@app.get("/pedir", response_class=HTMLResponse)
def pedir_get(request: Request, s: Session = Depends(get_session)):
    u = atual(request, s)
    if not u: return RedirectResponse("/login", 302)
    return templates.TemplateResponse(request, "pedir.html", {"u": u, "restantes": restantes(u)})


@app.post("/pedir")
def pedir_post(request: Request, tipo_comercio: str = Form(...), cidade: str = Form(...),
               uf: str = Form(...), quantidade: int = Form(...),
               s: Session = Depends(get_session)):
    u = atual(request, s)
    if not u: return RedirectResponse("/login", 302)
    if quantidade > restantes(u):
        return templates.TemplateResponse(request, "pedir.html", {"u": u, "restantes": restantes(u),
             "erro": f"Você só tem {restantes(u)} leads disponíveis."})
    req = LeadRequest(user_id=u.id, tipo_comercio=tipo_comercio, cidade=cidade,
                      uf=uf, quantidade=quantidade)
    s.add(req); s.commit()
    return RedirectResponse("/historico", 302)


# ---------------- HISTÓRICO ----------------
@app.get("/historico", response_class=HTMLResponse)
def historico(request: Request, s: Session = Depends(get_session)):
    u = atual(request, s)
    if not u: return RedirectResponse("/login", 302)
    pedidos = s.exec(select(LeadRequest).where(LeadRequest.user_id == u.id)
                     .order_by(LeadRequest.criado_em.desc())).all()
    return templates.TemplateResponse(request, "historico.html", {"u": u, "pedidos": pedidos, "restantes": restantes(u)})


# ---------------- PAINEL (leads + feedback) ----------------
@app.get("/pedido/{rid}", response_class=HTMLResponse)
def painel(request: Request, rid: str, s: Session = Depends(get_session)):
    u = atual(request, s)
    if not u: return RedirectResponse("/login", 302)
    req = s.get(LeadRequest, rid)
    if not req or req.user_id != u.id: raise HTTPException(404)
    leads = s.exec(select(Lead).where(Lead.request_id == rid)).all()
    fb = {f.lead_id: f for f in s.exec(select(LeadFeedback)
          .where(LeadFeedback.user_id == u.id)).all()}
    return templates.TemplateResponse(request, "painel.html", {"u": u, "req": req, "leads": leads, "fb": fb,
         "status_opcoes": STATUS_OPCOES})


@app.post("/feedback")
def feedback(request: Request, lead_id: str = Form(...), status: str = Form(...),
             observacao: str = Form(""), s: Session = Depends(get_session)):
    u = atual(request, s)
    if not u: return RedirectResponse("/login", 302)
    lead = s.get(Lead, lead_id)
    if not lead or lead.user_id != u.id: raise HTTPException(404)
    f = s.exec(select(LeadFeedback).where(LeadFeedback.lead_id == lead_id)).first()
    if f:
        f.status, f.observacao, f.atualizado_em = status, observacao, datetime.utcnow()
    else:
        f = LeadFeedback(lead_id=lead_id, user_id=u.id, status=status, observacao=observacao)
    s.add(f); s.commit()
    return RedirectResponse(f"/pedido/{lead.request_id}", 302)


# ---------------- +10 (trava de feedback) ----------------
@app.get("/extra", response_class=HTMLResponse)
def extra(request: Request, s: Session = Depends(get_session)):
    u = atual(request, s)
    if not u: return RedirectResponse("/login", 302)
    total = len(s.exec(select(Lead).where(Lead.user_id == u.id)).all())
    com_fb = len(s.exec(select(LeadFeedback).where(LeadFeedback.user_id == u.id)).all())
    liberado = total > 0 and com_fb >= total
    return templates.TemplateResponse(request, "extra.html", {"u": u, "liberado": liberado, "total": total,
         "com_fb": com_fb, "whatsapp": WHATSAPP})


# ---------------- ADMIN (fulfillment) ----------------
@app.get("/admin", response_class=HTMLResponse)
def admin(request: Request, s: Session = Depends(get_session)):
    u = atual(request, s)
    if not u or not u.is_admin: raise HTTPException(403)
    pendentes = s.exec(select(LeadRequest).where(LeadRequest.status == "pendente")
                       .order_by(LeadRequest.criado_em)).all()
    users = {x.id: x for x in s.exec(select(User)).all()}
    return templates.TemplateResponse(request, "admin.html", {"u": u, "pendentes": pendentes, "users": users})


@app.post("/admin/entregar")
def admin_entregar(request: Request, request_id: str = Form(...), csv_texto: str = Form(...),
                   s: Session = Depends(get_session)):
    u = atual(request, s)
    if not u or not u.is_admin: raise HTTPException(403)
    req = s.get(LeadRequest, request_id)
    if not req: raise HTTPException(404)
    reader = csv.DictReader(io.StringIO(csv_texto.strip()))
    n = 0
    for r in reader:
        g = lambda *ks: next((r[k] for k in ks if k in r and r[k]), "")
        s.add(Lead(request_id=req.id, user_id=req.user_id,
                   empresa=g("empresa","company"), cidade=g("cidade","city"),
                   telefone=g("telefone","phone"), email=g("email"),
                   canal=g("canal"), website=g("website"),
                   situacao=g("situacao","problema","status"), porte=g("porte"),
                   instagram=g("instagram"), nota_google=g("nota_google"),
                   avaliacoes=g("avaliacoes"))); n += 1
    req.status = "entregue"; req.entregue_em = datetime.utcnow()
    dono = s.get(User, req.user_id)
    dono.leads_gratis_usados += n
    s.add(req); s.add(dono); s.commit()
    return RedirectResponse("/admin", 302)


@app.post("/admin/grant")
def admin_grant(request: Request, user_id: str = Form(...), quantidade: int = Form(10),
                s: Session = Depends(get_session)):
    u = atual(request, s)
    if not u or not u.is_admin: raise HTTPException(403)
    dono = s.get(User, user_id)
    if not dono: raise HTTPException(404)
    dono.leads_gratis_liberados += quantidade
    s.add(Grant(user_id=user_id, quantidade=quantidade, motivo="+10 pós feedback"))
    s.add(dono); s.commit()
    return RedirectResponse("/admin", 302)
