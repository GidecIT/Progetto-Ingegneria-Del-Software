## Function calculate_discount

```python
def calculate_discount(price: float, customer_type: str) -> float:
```

### Requirement

The system shall calculate the final price after applying a discount based on the customer type.

If the input price is negative, the system shall return -1 to indicate invalid input.

If the customer type is "regular", the system shall apply a 5% discount.

If the customer type is "premium", the system shall apply a 20% discount.

For any other customer type, the system shall return the original price unchanged.

Criterion: 

- price

Predicate:

- price < 0 → invalid
- price >= 0 → valid

Criterion: 

- customer_type

Predicate:

- customer_type == "regular" → valid
- customer_type == "premium" → valid
- customer_type != "regular" and != "premium" → valid


Equivalence Classes

Per price:
    
- EC1: price < 0
- EC2: price >= 0

Per customer_type:

- EC3: "regular"
- EC4: "premium"
- EC5: other

Combinations of equivalence classes

Since the function has two inputs, valid combinations must be considered.
    
    EC1 × EC3
    EC1 × EC4
    EC1 × EC5
    EC2 × EC3
    EC2 × EC4
    EC2 × EC5
    
    
| TC  | price | customer_type | EC covered | Expected |
| --- | ----: | ------------- | ---------- | -------: |
| CD1 |   -10 | `"regular"`   | EC1        |       -1 |
| CD2 |   100 | `"regular"`   | EC2, EC3   |     95.0 |
| CD3 |   100 | `"premium"`   | EC2, EC4   |     80.0 |
| CD4 |   100 | `"guest"`     | EC2, EC5   |      100 |

Boundary: price = 0

This is the decision boundary between invalid and valid price.


| TC   | price | customer_type | Boundary covered  | Expected |
| ---- | ----: | ------------- | ----------------- | -------: |
| CDB1 |     0 | `"regular"`   | exact boundary    |      0.0 |
| CDB2 |  0.01 | `"regular"`   | immediately above |  0.0095? |
| CDB3 | -0.01 | `"regular"`     | immediately below | -1       |

Boundary: customer type recognition

This is not numeric, but there are lexical boundaries at the exact accepted values.

Boundary around "regular":

| TC   | price | customer_type | Boundary covered  | Expected |
| ---- | ----: | ------------- | ----------------- | -------: |
| CDB4 |   100 | `"regular"`   | exact boundary    |     95.0 |
| CDB5 |   100 | `"regularx"`  | immediately above |    100.0 |
| CDB6 |   100 | `"regula"`    | immediately below |    100.0 |

Boundary around "premium":

| TC   | price | customer_type | Boundary covered  | Expected |
| ---- | ----: | ------------- | ----------------- | -------: |
| CDB7 |   100 | `"premium"`   | exact boundary    |     80.0 |
| CDB8 |   100 | `"premiumx"`  | immediately above |    100.0 |
| CDB9 |   100 | `"premiu"`    | immediately below |    100.0 |


## Function is\_valid\_email

```python
def is_valid_email(email: str) -> bool:
```

### Requirement
The system shall validate whether a given string represents a syntactically valid email address.

The system shall reject empty inputs and inputs not containing the "@" separator.

The system shall reject inputs with an empty local part, an empty domain part, or a domain part
not containing at least one dot.

The system shall return True only when all required structural conditions are satisfied.

Criterion: 

- email

Predicates:

- email is empty or null-like → invalid
- "@" not in email → invalid
- "@" in email and local part is empty → invalid
- "@" in email and domain part is empty → invalid
- "@" in email and domain part does not contain "." → invalid
- "@" in email and local part not empty and domain part not empty and "." in domain → valid

Equivalence Classes

- EC1: email empty
- EC2: email without @
- EC3: email with local part empty
- EC4: email with domain empty
- EC5: email with domain without .
- EC6: email valid according to spec.

| TC  | email                | EC covered | Expected |
| --- | -------------------- | ---------- | -------- |
| EM1 | `""`                 | EC1        | `False`  |
| EM2 | `"abc.example.com"`  | EC2        | `False`  |
| EM3 | `"@example.com"`     | EC3        | `False`  |
| EM4 | `"user@"`            | EC4        | `False`  |
| EM5 | `"user@examplecom"`  | EC5        | `False`  |
| EM6 | `"user@example.com"` | EC6        | `True`   |

Boundary: empty vs non-empty email

Structural boundary at string length 0.

| TC   | email | Boundary covered  | Expected          |
| ---- | ----- | ----------------- | ----------------- |
| EMB1 | `""`  | exact boundary    | `False`           |
| EMB2 | `"a"` | immediately above | `False`           |

For strings, there is no representable value “below” the empty string. This boundary is one-sided in the input domain.

Boundary: presence of "@"

| TC   | email   | Boundary covered  | Expected |
| ---- | ------- | ----------------- | -------- |
| EMB4 | `"a@"`  | exact boundary    | `False`  |
| EMB5 | `"a"`   | immediately below | `False`  |
| EMB6 | `"a@b"` | immediately above | `False`  |

Boundary: domain part emptiness
Boundary at domain length = 0

| TC    | email      | Boundary covered  | Expected          |
| ----- | ---------- | ----------------- | ----------------- |
| EMB10 | `"user@"`  | exact boundary    | `False`           |
| EMB11 | `"user@a"` | immediately above | `False`           |


Boundary: "." inside domain
Structural boundary between domain without dot and domain with dot.

| TC    | email          | Boundary covered  | Expected |
| ----- | -------------- | ----------------- | -------- |
| EMB13 | `"user@abc"`   | exact boundary    | `False`  |
| EMB14 | `"user@abc.d"` | immediately above | `True`   |
| EMB15 | `"user@ab"`    | immediately below | `False`  |



## Function divide

```python
def divide(a: float, b: float) -> float:
```

### Requirement

The system shall divide the first input by the second input and return the result as a floating-point number.

If either input is not a number (int or float), the system shall raise a TypeError with message "Inputs must be numbers".

If the second input is zero, the system shall raise a ZeroDivisionError with message "Cannot divide by zero".


Criterion:

- a (type)

Predicate:

- a is not int/float → invalid (TypeError)
- a is int/float → valid

Criterion:

- b (type)

Predicate:

- b is not int/float → invalid (TypeError)
- b is int/float → valid

Criterion:

- b (value), when both a and b are numbers

Predicate:

- b == 0 → invalid (ZeroDivisionError)
- b != 0 → valid

Equivalence Classes

Per a (type):

- EC1: a is not a number
- EC2: a is a number

Per b (type):

- EC3: b is not a number
- EC4: b is a number

Per b (value), when EC2 and EC4:

- EC5: b == 0
- EC6: b > 0
- EC7: b < 0


Combinations of equivalence classes
Since the function has two inputs with type and value partitions, valid combinations must be considered.

    EC1 × EC3
    EC1 × EC4 (b number)
    EC2 × EC3
    EC2 × EC4, EC5
    EC2 × EC4, EC6
    EC2 × EC4, EC7
    
    
| TC  | a      | b      | EC covered   | Expected             |
| --- | -----: | -----: | ------------ | -------------------- |
| DV1 | `"ab"` | `"2"`    | EC1,EC2          | `TypeError`    |
| DV2 | `"ab"` | `2`    | EC1,EC4         | `TypeError`    |
| DV3 | `10`   | `"ab"` | EC2, EC3     | `TypeError`          |
| DV4 | `10`   | `0`    | EC2, EC4, EC5| `ZeroDivisionError`  |
| DV5 | `10`   | `2`    | EC2, EC4, EC6| `5.0`                |
| DV6 | `-10`  | `2`    | EC2, EC4, EC6| `-5.0`               |
| DV7 | `0`    | `2`    | EC2, EC4, EC6| `0.0`                |
| DV8 | `10`   | `-2`   | EC2, EC4, EC7| `-5.0`               |


Boundary: b = 0

This is the decision boundary between ZeroDivisionError and valid division.

| TC   | a    | b      | Boundary covered  | Expected             |
| ---- | ---: | -----: | ----------------- | -------------------- |
| DVB1 | `10` | `0`    | exact boundary    | `ZeroDivisionError`  |
| DVB2 | `10` | `0.01` | immediately above | `1000.0`             |
| DVB3 | `10` | `-0.01`| immediately below | `-1000.0`            |


Boundary: type recognition

This is a structural boundary between numeric and non-numeric types.

Boundary around a:

| TC   | a      | b    | Boundary covered                   | Expected             |
| ---- | -----: | ---: | ---------------------------------- | -------------------- |
| DVB4 | `"1"`  | `2`  | exact boundary (string that looks numeric) | `TypeError`  |
| DVB5 | `1`    | `2`  | immediately above (actual number)  | `0.5`                |
| DVB6 | `None` | `2`  | immediately below (non-string, non-number) | `TypeError`  |

Boundary around b:

| TC   | a    | b      | Boundary covered                   | Expected             |
| ---- | ---: | -----: | ---------------------------------- | -------------------- |
| DVB7 | `10` | `"1"`  | exact boundary (string that looks numeric) | `TypeError`  |
| DVB8 | `10` | `1`    | immediately above (actual number)  | `10.0`               |
| DVB9 | `10` | `None` | immediately below (non-string, non-number) | `TypeError`  |


## Function withdraw

```python
def withdraw(balance: float, amount: float) -> str:
```
    
### Requirement:
The system shall process a withdrawal request against the available account balance.

If the withdrawal amount is less than or equal to zero, the system shall return "Invalid amount".

If the withdrawal amount exceeds the current balance, the system shall return "Insufficient funds".

Otherwise, the system shall return "Withdrawal successful".

Criterion: 

- amount

Predicates:

- amount <= 0 → invalid
- amount > 0 → valid

Criterion: 

- balance

Predicates:

- balance < 0 → valid by implementation
- balance >= 0 → valid

Derived behavioral partition per amount > 0:
    
- amount > balance
- amount <= balance

Per amount:

- EC1: amount <= 0
- EC2: amount > 0

Relation with balance, when EC2 is valid:

- EC3: amount > balance
- EC4: amount <= balance

| TC  | balance | amount | EC coveded | Expected                  |
| --- | ------: | -----: | ---------- | ------------------------- |
| WD1 |     100 |      0 | EC1        | `"Invalid amount"`        |
| WD2 |     100 |    -10 | EC1        | `"Invalid amount"`        |
| WD3 |     100 |    150 | EC2, EC3   | `"Insufficient funds"`    |
| WD4 |     100 |     50 | EC2, EC4   | `"Withdrawal successful"` |
| WD5 |     100 |    100 | EC2, EC4   | `"Withdrawal successful"` |

Boundary: amount = 0

Boundary between invalid and valid amount.

| TC   | balance | amount | Boundary covered  | Expected                  |
| ---- | ------: | -----: | ----------------- | ------------------------- |
| WDB1 |     100 |      0 | exact boundary    | `"Invalid amount"`        |
| WDB2 |     100 |   0.01 | immediately above | `"Withdrawal successful"` |
| WDB3 |     100 |  -0.01 | immediately below | `"Invalid amount"`  

Boundary: amount = balance

Boundary between success and insufficient funds.

| TC   | balance | amount | Boundary covered  | Expected                  |
| ---- | ------: | -----: | ----------------- | ------------------------- |
| WDB4 |     100 |    100 | exact boundary    | `"Withdrawal successful"` |
| WDB5 |     100 | 100.01 | immediately above | `"Insufficient funds"`    |
| WDB6 |     100 |  99.99 | immediately below | `"Withdrawal successful"` |

Boundary: balance = 0

This is relevant only combined with amount.

| TC   | balance | amount | Boundary covered  | Expected                  |
| ---- | ------: | -----: | ----------------- | ------------------------- |
| WDB7 |       0 |      0 | exact boundary    | `"Invalid amount"`        |
| WDB8 |    0.01 |   0.01 | immediately above | `"Withdrawal successful"` |
| WDB9 |   -0.01 |   0.01 | immediately below | `"Insufficient funds"`    |  


## Function grade_student


```python
def grade_student(score: int) -> str:
```
    
### Requirement:
The system shall assign a grade based on the student's numeric score.

Scores lower than 0 or greater than 100 shall be considered invalid and shall produce "Invalid score".
Scores from 90 to 100 inclusive shall produce grade "A".

Scores from 75 to 89 inclusive shall produce grade "B".

Scores from 50 to 74 inclusive shall produce grade "C".

Scores from 0 to 49 inclusive shall produce grade "F".

## Function search_product


```python
def search_product(products: list[str], keyword: str) -> list[str]:
```

### Requirement:
The system shall search the input product list for all entries containing the given keyword.
The search shall be case-insensitive.
If the keyword is empty, the system shall return an empty list.
The system shall return all matching product names while preserving their original representation.
