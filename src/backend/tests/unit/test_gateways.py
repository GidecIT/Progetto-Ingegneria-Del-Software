from __future__ import annotations

import pytest
from participium.gateways.email_gateway import EmailGateway

pytestmark = pytest.mark.unit

def test_email_gateway_send():
    gateway = EmailGateway()
    gateway.send("test@example.com", "Title", "Body")
    assert True
