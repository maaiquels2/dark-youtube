@echo off
title TikTok Automation - Login Setup
echo Abrindo janela de login do TikTok para o Dark Studio...
echo.
echo Faca login com QR Code, Google ou usuario/senha nesta janela.
echo A sessao ficara salva permanentemente para o publicador automatico.
echo.
start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" --user-data-dir="C:\Users\Admin\Documents\Codex\2026-09-10\Dark YouTube\tiktok_bot_profile" --start-maximized "https://www.tiktok.com/login?redirect_url=https%3A%2F%2Fwww.tiktok.com%2Ftiktokstudio%2Fupload"
