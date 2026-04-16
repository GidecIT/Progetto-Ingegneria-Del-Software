def calculate_discount(price: float, customer_type: str) -> float:
    if price < 0:
        return -1
    if customer_type == "regular":
        return price * 0.95
    if customer_type == "premium":
        return price * 0.80
    return price


def is_valid_email(email: str) -> bool:
    if not email or "@" not in email:
        return False
    local, _, domain = email.partition("@")
    if not local or not domain or "." not in domain:
        return False
    return True


#EXCEPTIONS TESTING
def divide(a: float, b: float) -> float:
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("Inputs must be numbers")
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    return a / b


def withdraw(balance: float, amount: float) -> str:
    if amount <= 0:
        return "Invalid amount"
    if amount > balance:
        return "Insufficient funds"
    return "Withdrawal successful"


def login(username: str, password: str) -> str:
    if not username or not password:
        return "Missing credentials"
    if username == "admin" and password == "secret123":
        return "Login successful"
    return "Invalid username or password"


def grade_student(score: int) -> str:
    if score < 0 or score > 100:
        return "Invalid score"
    if score >= 90:
        return "A"
    if score >= 75:
        return "B"
    if score >= 50:
        return "C"
    return "F"


def search_product(products: list[str], keyword: str) -> list[str]:
    if not keyword:
        return []
    keyword = keyword.lower()
    return [p for p in products if keyword in p.lower()]