@echo off
cd /d "C:\Users\Admin\Documents\Codex\2026-09-10\Dark YouTube"
set PYTHONIOENCODING=utf-8
.venv\Scripts\python.exe tools\meta_publish.py run >> social\meta_run.log 2>&1

