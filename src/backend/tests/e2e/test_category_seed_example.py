from __future__ import annotations

import pytest
from flask.testing import FlaskClient

from participium import create_app
from participium.database import close_connection, get_session
from participium.models.category import Category


@pytest.mark.e2e
@pytest.mark.skip(reason="This test is a crude example.")
def test_get_categories_after_inserting_category_with_flask_test_client(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("DATABASE_URL", "sqlite+pysqlite:///:memory:")




    monkeypatch.setenv("AUTO_INIT_DB", "true")
    monkeypatch.setenv("BOOTSTRAP_REFERENCE_DATA", "false")
    monkeypatch.setenv("BOOTSTRAP_DEMO_DATA", "false")




    application = create_app()
    application.config.update(TESTING=True)
    client: FlaskClient = application.test_client()




    with application.app_context():
        session = get_session()
        session.add(Category(name="Example E2E Category", is_active=True))
        session.commit()



    response = client.get("/api/v1/categories")

    assert response.status_code == 200
    category_names = [category["name"] for category in response.get_json()]
    assert "Example E2E Category" in category_names



    close_connection()
