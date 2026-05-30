import pytest
from participium.models.message import Message
from participium.models.report import Report

pytestmark = pytest.mark.integration



def test_add_message(db_session, message_repository, test_report, test_user):

    new_message = Message(
        report_id=test_report.id,
        sender_id=test_user.id,
        body="I'm sending more photos soon."
    )

    added = message_repository.add(new_message)
    db_session.commit()

    assert added.id is not None
    assert added.body == "I'm sending more photos soon."
    assert added.report_id == test_report.id




def test_list_for_report_ordering_and_isolation(db_session, message_repository, test_report, test_user):

    report_b = Report(
        title="Buca profonda",
        description="Buca in Piazza Castello",
        latitude=45.1,
        longitude=7.1,
        category_id=test_report.category_id,
        reporter_id=test_user.id
    )
    db_session.add(report_b)
    db_session.commit()

    msg1 = Message(report_id=test_report.id, sender_id=test_user.id, body="First message")
    msg2 = Message(report_id=test_report.id, sender_id=test_user.id, body="Second message")

    msg_other = Message(report_id=report_b.id, sender_id=test_user.id, body="Invisible message")
    
    db_session.add_all([msg1, msg2, msg_other])
    db_session.commit()

    messages_a = message_repository.list_for_report(test_report.id)

    assert len(messages_a) == 2

    assert all(m.report_id == test_report.id for m in messages_a)

    assert messages_a[0].body == "First message"
    assert messages_a[1].body == "Second message"


def test_list_for_report_empty(message_repository):

    results = message_repository.list_for_report(100) 
    
    assert results == []