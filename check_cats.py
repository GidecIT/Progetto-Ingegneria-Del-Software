from participium.app import create_app
from participium.models.category import Category
app = create_app()
with app.app_context():
    print([c.name for c in Category.query.all()])
