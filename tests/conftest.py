"""Os testes daqui sao scripts (imprimem "ok"/"FALHA" e saem com 1 se algo falhou).
Este arquivo faz o `pytest tests` rodar cada test_*.py como script, em processo proprio."""
import subprocess, sys
from pathlib import Path
import pytest


def pytest_collect_file(parent, file_path):
    if file_path.suffix == ".py" and file_path.name.startswith("test_"):
        return ScriptFile.from_parent(parent, path=file_path)


class ScriptFile(pytest.File):
    def collect(self):
        yield ScriptItem.from_parent(self, name=self.path.stem)


class ScriptItem(pytest.Item):
    def runtest(self):
        r = subprocess.run([sys.executable, str(self.path)], cwd=self.path.parents[1], capture_output=True, text=True, encoding="utf-8", errors="replace")
        self.saida = r.stdout + r.stderr
        if r.returncode:
            raise AssertionError("\n".join(l for l in self.saida.splitlines() if "FALHA" in l or "Error" in l) or self.saida[-2000:])

    def repr_failure(self, excinfo):
        return str(excinfo.value)

    def reportinfo(self):
        return self.path, 0, self.name
