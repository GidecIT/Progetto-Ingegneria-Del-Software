from participium.app import create_app
from participium.models.user import User
from participium.models.enums import Role
from participium.repositories.report_repository import ReportRepository
from participium.database import get_session

app = create_app()
with app.app_context():
    session = get_session()
    repo = ReportRepository(session)
    op = session.query(User).filter_by(role=Role.OPERATOR).first()
    if op:
        reports = repo.list_operator_reports(op.role, op.category_id)
        print(f"Loaded {len(reports)} assigned reports for operator")
    else:
        print("No operator found")
