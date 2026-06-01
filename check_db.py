from participium.app import create_app
from participium.models.category import Category
from participium.models.user import User
from participium.database import get_session
import os

app = create_app()
with app.app_context():
    session = get_session()
    cats = session.query(Category).all()
    users = session.query(User).all()
    print(f"Categories: {[c.name for c in cats]}")
    print(f"Users: {[u.email for u in users]}")
