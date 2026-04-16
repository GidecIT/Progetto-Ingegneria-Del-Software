import pytest
from bb_examples1 import *
@pytest.mark.parametrize("price, customer_type, expected", [
    (-10,"regular", -1),    #CD1
    (100, "regular", 95.0), #CD2
(100, "premium", 80.0),      # CD3 (= CDB7)
        (100, "guest", 100),         # CD4
        # Boundary: price = 0
        (0, "regular", 0.0),         # CDB1
        (0.01, "regular", 0.0095),   # CDB2
        (-0.01, "regular", -1),      # CDB3
        # Boundary: "regular"
        (100, "regularx", 100.0),    # CDB5
        (100, "regula", 100.0),      # CDB6
        # Boundary: "premium"
        (100, "premiumx", 100.0),    # CDB8
        (100, "premiu", 100.0),      # CDB9
])
def test_calculate_discount(price, customer_type, expected):
    assert calculate_discount(price, customer_type) == expected

@pytest.mark.parametrize(
    "email,expected",[
        # Equivalence classes
        ("", False),  # EM1 (= EMB1)
        ("abc.example.com", False),  # EM2
        ("@example.com", False),  # EM3
        ("user@", False),  # EM4 (= EMB10)
        ("user@examplecom", False),  # EM5
        ("user@example.com", True),  # EM6 (= EMB6)
        # Boundary: empty vs non-empty
        ("a", False),  # EMB2 (= EMB5')
        # Boundary: presence of "@"
        ("user@example", False),  # EMB4
        ("userexample", False),  # EMB5
        # Boundary: "@" minimal form
        ("a@", False),  # EMB4'
        ("a@b", False),  # EMB6'
        # Boundary: local part emptiness
        ("@x.y", False),  # EMB7
        ("a@x.y", True),  # EMB8
        # Boundary: domain part emptiness
        ("user@a", False),  # EMB11
        # Boundary: "." in domain
        ("user@abc", False),  # EMB13
        ("user@abc.d", True),  # EMB14
        ("user@ab", False),  # EMB15
    ])
def test_valid_email(email, expected):
        assert is_valid_email(email) == expected


@pytest.mark.parametrize(
    "a,b,expected_exception,expected_result",
    [
        # Equivalence classes
        ("ab", 2, TypeError, None),          # DV1
        (10, "ab", TypeError, None),         # DV2
        (10, 0, ZeroDivisionError, None),    # DV3 (= DVB1)
        (10, 2, None, 5.0),                  # DV4
        (-10, 2, None, -5.0),                # DV5
        (0, 2, None, 0.0),                   # DV6
        (10, -2, None, -5.0),                # DV7
        # Boundary: b = 0
        (10, 0.01, None, 1000.0),            # DVB2
        (10, -0.01, None, -1000.0),          # DVB3
        # Boundary: type a
        ("1", 2, TypeError, None),           # DVB4
        (1, 2, None, 0.5),                   # DVB5
        (None, 2, TypeError, None),          # DVB6
        # Boundary: type b
        (10, "1", TypeError, None),          # DVB7
        (10, 1, None, 10.0),                 # DVB8
        (10, None, TypeError, None),         # DVB9
    ],
)
def test_divide(a, b, expected_exception, expected_result):
    if expected_exception:
        with pytest.raises(expected_exception):
            divide(a, b)
    else:
        assert divide(a, b) == pytest.approx(expected_result)


@pytest.mark.parametrize(
    "balance,amount,expected",
    [
        # Equivalence classes
        (100, 0, "Invalid amount"),            # WD1 (= WDB1)
        (100, -10, "Invalid amount"),          # WD2
        (100, 150, "Insufficient funds"),      # WD3
        (100, 50, "Withdrawal successful"),    # WD4
        (100, 100, "Withdrawal successful"),   # WD5 (= WDB4)
        # Boundary: amount = 0
        (100, 0.01, "Withdrawal successful"),  # WDB2
        (100, -0.01, "Invalid amount"),        # WDB3
        # Boundary: amount = balance
        (100, 100.01, "Insufficient funds"),   # WDB5
        (100, 99.99, "Withdrawal successful"), # WDB6
        # Boundary: balance = 0
        (0, 0, "Invalid amount"),              # WDB7
        (0.01, 0.01, "Withdrawal successful"), # WDB8
        (-0.01, 0.01, "Insufficient funds"),   # WDB9
    ],
)
def test_withdraw(balance, amount, expected):
    assert withdraw(balance, amount) == expected