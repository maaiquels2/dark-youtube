@echo off
title Dark Studio - Chrome de Automacao do TikTok
cd /d "C:\Users\Admin\Documents\Codex\2026-09-10\Dark YouTube"

echo ========================================================
echo    Dark Studio - Iniciando Chrome de Automacao
echo ========================================================
echo.
echo Abrindo navegador dedicado com porta de automacao ativa...
echo.
echo 1. Se a tela de login aparecer, basta clicar em "Continuar com Google"
echo    ou escanear o QR Code uma unica vez.
echo 2. A sessao ficara salva permanentemente para o robo postar 3x ao dia.
echo.

start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" --user-data-dir="C:\Users\Admin\Documents\Codex\2026-09-10\Dark YouTube\tiktok_bot_profile" --remote-debugging-port=9333 --remote-allow-origins=* --start-maximized "https://www.tiktok.com/login?redirect_url=https%3A%2F%2Fwww.tiktok.com%2Ftiktokstudio%2Fupload"

echo Chrome aberto com sucesso na porta 9333!
echo Voce pode deixar esta janela aberta ou minimizada.
pause

