"""Renova o META_PAGE_TOKEN do .env a partir de um token de usuario curto do Graph API Explorer.

Uso (o Maiquel roda; o token e digitado escondido e nunca aparece na tela nem no log):
    .venv\\Scripts\\python.exe tools\\meta_token.py

1. troca o token curto (1 h) por um de longa duracao (60 dias), com META_APP_ID e META_APP_SECRET do .env;
2. pede a esse token o token da Pagina META_PAGE_ID (token de Pagina vindo de token longo nao expira);
3. confere se a Pagina e o Instagram sao os esperados (meta_publish.EXPECT) e se o token publica Reels;
4. so entao grava META_PAGE_TOKEN e META_USER_TOKEN no .env.
"""
import getpass, re, sys
from datetime import datetime
from pathlib import Path
import requests

ROOT = Path(__file__).resolve().parents[1]; ENV = ROOT / ".env"
sys.path.insert(0, str(ROOT / "tools"))
from meta_publish import G, V, EXPECT  # noqa: E402

NEED = {"pages_show_list", "pages_manage_posts", "pages_read_engagement", "instagram_basic", "instagram_content_publish"}


def get(path, **params):
    try: j = requests.get(f"{G}/{V}/{path}", params=params, timeout=60).json()
    except requests.RequestException: sys.exit(f"Erro de rede em {path} (detalhe omitido para nao vazar o token).")
    if "error" in j: sys.exit(f"A Meta recusou ({path}): {j['error'].get('message')}")
    return j


def main():
    txt = ENV.read_text(encoding="utf-8")
    e = {m.group(1): m.group(2).strip().strip('"').strip("'") for m in re.finditer(r"(?m)^(META_[A-Z_]+)=(.*)$", txt)}
    for k in ("META_APP_ID", "META_APP_SECRET", "META_PAGE_ID"):
        if not e.get(k): sys.exit(f"{k} faltando no .env")

    short = getpass.getpass("Cole o token do Graph API Explorer e aperte Enter (nao aparece na tela): ").strip()
    if not short: sys.exit("Nenhum token colado.")

    long_user = get("oauth/access_token", grant_type="fb_exchange_token", client_id=e["META_APP_ID"],
                    client_secret=e["META_APP_SECRET"], fb_exchange_token=short)["access_token"]
    app_tok = f"{e['META_APP_ID']}|{e['META_APP_SECRET']}"

    d = get("debug_token", input_token=long_user, access_token=app_tok)["data"]
    falta = NEED - set(d.get("scopes") or [])
    if falta: sys.exit("Faltou marcar no Explorer: " + ", ".join(sorted(falta)) + ". Gere de novo com essas permissoes.")

    p = get(e["META_PAGE_ID"], fields="name,access_token,instagram_business_account{id,username}", access_token=long_user)
    ig = p.get("instagram_business_account") or {}
    print(f"Pagina: {p.get('name')} | Instagram: {ig.get('username')}")
    if p.get("name") != EXPECT["page"] or ig.get("username") != EXPECT["ig"]:
        sys.exit(f"Conta errada: esperava {EXPECT['page']} / {EXPECT['ig']}. Nada foi gravado.")
    page_tok = p.get("access_token")
    if not page_tok: sys.exit("A Meta nao devolveu o token da Pagina (falta permissao de admin?). Nada foi gravado.")

    pd = get("debug_token", input_token=page_tok, access_token=app_tok)["data"]
    exp = pd.get("expires_at", 0)
    print("Token da Pagina:", "nao expira" if not exp else "expira em " + datetime.fromtimestamp(exp).strftime("%d/%m/%Y %H:%M"))

    for k, v in (("META_PAGE_TOKEN", page_tok), ("META_USER_TOKEN", long_user)):
        txt = re.sub(rf"(?m)^{k}=.*$", lambda _: f"{k}={v}", txt) if re.search(rf"(?m)^{k}=", txt) else txt.rstrip("\n") + f"\n{k}={v}\n"
    ENV.write_text(txt, encoding="utf-8")
    print("Gravado no .env (META_PAGE_TOKEN e META_USER_TOKEN). Pode fechar esta janela.")


if __name__ == "__main__":
    main()
