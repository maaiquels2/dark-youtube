# -*- coding: utf-8 -*-
"""Chrome de automacao UNICO do Dark Studio (config/chrome.json).
Regra: so conecta no Chrome ja aberto na porta CDP; se nao houver, abre com o user-data-dir FIXO.
Nunca cria perfil temporario, nunca mata nem reinicia Chrome."""
import json, socket, subprocess, time
from pathlib import Path
CFG = json.loads((Path(__file__).resolve().parent / "config" / "chrome.json").read_text(encoding="utf-8"))
PORT = int(CFG["cdp_port"]); USER_DATA = Path(CFG["user_data_dir"]); PROFILE_DIR = CFG["profile_directory"]
CDP_URL = f"http://127.0.0.1:{PORT}"

def port_open():
    s = socket.socket(); s.settimeout(0.5)
    try:
        s.connect(("127.0.0.1", PORT)); return True
    except OSError:
        return False
    finally:
        s.close()

def ensure_chrome(url="https://grok.com/imagine"):
    """True se abriu agora, False se ja estava aberto."""
    if port_open():
        return False
    if not USER_DATA.is_dir():
        raise RuntimeError(f"Perfil fixo nao existe: {USER_DATA} (nao crio outro)")
    subprocess.Popen([CFG["chrome_path"], f"--user-data-dir={USER_DATA}", f"--profile-directory={PROFILE_DIR}",
                      f"--remote-debugging-port={PORT}", "--no-first-run", "--no-default-browser-check",
                      "--disable-session-crashed-bubble", "--new-window", url],
                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for _ in range(60):
        if port_open():
            return True
        time.sleep(0.5)
    raise RuntimeError("Chrome do Dark Studio esta aberto sem porta CDP (feche-o a mao) ou nao abriu.")
