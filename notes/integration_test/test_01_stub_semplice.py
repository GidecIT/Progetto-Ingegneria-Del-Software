import importlib.util, sys, pathlib
import importlib
import pytest

spec = importlib.util.spec_from_file_location(
    "semplice",
    pathlib.Path(__file__).parent / "../src/01_semplice_stub.py"
)

modulo_semplice = importlib.util.module_from_spec(spec)
sys.modules["modulo_semplice"] = modulo_semplice
spec.loader.exec_module(modulo_semplice)

def stub_function2(x):
    return 10

def stub_function3(x):
    return 5

def test_function1_con_stub(monkeypatch):
    monkeypatch.setattr(modulo_semplice, "function2", stub_function2)
    monkeypatch.setattr(modulo_semplice, "function3", stub_function3)

    assert modulo_semplice.function1(99) == 15

def test_function1_con_stub_diversi(monkeypatch):
    monkeypatch.setattr(modulo_semplice,"function2", lambda x: 100)
    monkeypatch.setattr(modulo_semplice, "function3", lambda x: 1)

    assert modulo_semplice.function1(0) == 101

