from participium.app import create_app
from participium.models.user import User
app = create_app()
with app.app_context():
    op = User.query.filter_by(email="operator@example.com").first()
    print(f"OP: {op.username}, Role: {op.role}, CatID: {op.category_id}")
