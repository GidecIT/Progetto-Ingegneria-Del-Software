import importlib.util, sys, pathlib
import pytest

spec = importlib.util.spec_from_file_location(
    "ecommerce",
    pathlib.Path(__file__).parent / "../src/03_esempio_ecommerce.py",
)
ecommerce = importlib.util.module_from_spec(spec)
sys.modules["ecommerce"] = ecommerce
spec.loader.exec_module(ecommerce)


CartItem = ecommerce.CartItem

def stub_get_price_fisso(product_id):
    return 10.0  # qualsiasi prodotto costa 10

def stub_charge_ok(user_id, amount):
    return {"id": "TX-FAKE-001", "status": "paid"}

def test_checkout_top_down(monkeypatch):
    monkeypatch.setattr(ecommerce, "get_price_from_db", stub_get_price_fisso)
    monkeypatch.setattr(ecommerce, "charge_payment", stub_charge_ok)

    cart = [CartItem("A", 2), CartItem("B", 3)]
    receipt = ecommerce.checkout_order("user42", cart)

    assert receipt["user_id"] == "user42"
    assert receipt["total"] == 50
    assert receipt["status"] == "paid"
    assert receipt["payment_id"] == "TX-FAKE-001"


def test_checkout_con_stub_tabellare(monkeypatch):
    prezzi = {"MELA": 0.50, "PANE": 2.00, "VINO": 8.90}

    def stub_get_price(product_id):
        return prezzi[product_id]

    def stub_charge(user_id, amount):
        # simulo un fallimento se amount > 100
        if amount > 100:
            return {"id": None, "status": "declined"}
        return {"id": "TX-OK", "status": "paid"}

    monkeypatch.setattr(ecommerce, "get_price_from_db", stub_get_price)
    monkeypatch.setattr(ecommerce, "charge_payment", stub_charge)

    cart = [CartItem("MELA", 4), CartItem("PANE", 1), CartItem("VINO", 2)]
    # 4*0.50 + 1*2.00 + 2*8.90 = 2 + 2 + 17.8 = 21.8
    receipt = ecommerce.checkout_order("luca", cart)

    assert receipt["total"] == 21.8
    assert receipt["status"] == "paid"

    cart = [CartItem("MELA", 4), CartItem("PANE", 1), CartItem("VINO", 20)]
    # 4*0.50 + 1*2.00 + 20*8.90 = 2 + 2 + 178 = 182
    receipt = ecommerce.checkout_order("luca", cart)

    assert receipt["total"] == 182.0
    assert receipt["status"] == "declined"

def test_checkout_carrello_vuoto(monkeypatch):
    """Nessun bisogno di vero stub: checkout fallisce prima delle dipendenze."""
    with pytest.raises(ValueError):
        ecommerce.checkout_order("user1", [])

def test_checkout_chiama_gateway_con_importo_giusto(monkeypatch):
    chiamate = []

    def stub_get_price(_pid):
        return 25.0

    def stub_charge(user_id, amount):
        chiamate.append((user_id, amount))
        return {"id": "TX-FAKE-001", "status": "paid"}

    monkeypatch.setattr(ecommerce, "get_price_from_db", stub_get_price)
    monkeypatch.setattr(ecommerce, "charge_payment", stub_charge)

    ecommerce.checkout_order("mario", [CartItem("P", 4)])

    assert chiamate == [("mario", 100.0)]


# BOTTOM-UP: uso un DRIVER per esercitare calculate_total

def test_driver_calculate_total(monkeypatch):
    prezzi = {"X": 3.0, "Y": 7.0}

    monkeypatch.setattr(ecommerce, "get_price_from_db", lambda pid: prezzi[pid])
    casi = [
        ([CartItem("X", 1)], 3.0),
        ([CartItem("Y", 2)], 14.0),
        ([CartItem("X", 3), CartItem("Y", 1)], 16.0),
        ([], 0.0),
    ]
    for cart, atteso in casi:
        assert ecommerce.calculate_total(cart) == atteso