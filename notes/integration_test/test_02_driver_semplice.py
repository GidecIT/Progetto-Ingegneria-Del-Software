import importlib.util, sys, pathlib
import importlib
import pytest

spec = importlib.util.spec_from_file_location(
    "modulo_driver",
    pathlib.Path(__file__).parent / "../src/02_semplice_driver.py"
)

modulo_driver = importlib.util.module_from_spec(spec)
sys.modules["modulo_driver"] = modulo_driver
spec.loader.exec_module(modulo_driver)

def driver_function4(inputs):
    return [modulo_driver.function4(x) for x in inputs  ]

def test_driver_pilota_function4():

    risultati = driver_function4([1,2,3,0,-5])
    assert risultati ==[2,4,6,0,-10]


def test_driver_segnala_input_non_valido():
    with pytest.raises(TypeError):
        driver_function4(["non un int"])