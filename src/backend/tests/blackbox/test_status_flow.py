from __future__ import annotations

from participium.core.status_flow import ensure_transition_allowed

import pytest
from participium.core.exceptions import ValidationError
from participium.models.enums import ReportStatus


@pytest.mark.parametrize(
    "current_status, next_status, expected_exception_or_result",
    [
        (ReportStatus.PENDING_APPROVAL, ReportStatus.PENDING_APPROVAL, True),
        (ReportStatus.PENDING_APPROVAL, ReportStatus.ASSIGNED, True),
        (ReportStatus.PENDING_APPROVAL, ReportStatus.REJECTED, True),
        (ReportStatus.PENDING_APPROVAL, ReportStatus.RESOLVED, ValidationError),

        (ReportStatus.ASSIGNED, ReportStatus.ASSIGNED, True),
        (ReportStatus.ASSIGNED, ReportStatus.IN_PROGRESS, True),
        (ReportStatus.ASSIGNED, ReportStatus.SUSPENDED, True),
        (ReportStatus.ASSIGNED, ReportStatus.RESOLVED, True),
        (ReportStatus.ASSIGNED, ReportStatus.PENDING_APPROVAL, ValidationError),

        (ReportStatus.IN_PROGRESS, ReportStatus.IN_PROGRESS, True),
        (ReportStatus.IN_PROGRESS, ReportStatus.SUSPENDED, True),
        (ReportStatus.IN_PROGRESS, ReportStatus.RESOLVED, True),
        (ReportStatus.IN_PROGRESS, ReportStatus.ASSIGNED, ValidationError),

        (ReportStatus.SUSPENDED, ReportStatus.SUSPENDED, True),
        (ReportStatus.SUSPENDED, ReportStatus.IN_PROGRESS, True),
        (ReportStatus.SUSPENDED, ReportStatus.RESOLVED, True),
        (ReportStatus.SUSPENDED, ReportStatus.PENDING_APPROVAL, ValidationError),

        (ReportStatus.REJECTED, ReportStatus.REJECTED, True),
        (ReportStatus.REJECTED, ReportStatus.ASSIGNED, ValidationError),

        (ReportStatus.RESOLVED, ReportStatus.RESOLVED, True),
        (ReportStatus.RESOLVED, ReportStatus.IN_PROGRESS, ValidationError),
    ],
)
def test_ensure_transition_allowed(current_status: ReportStatus, next_status: ReportStatus, expected_exception_or_result: bool | type[Exception]):
    
    if expected_exception_or_result is ValidationError:
        with pytest.raises(ValidationError):
            ensure_transition_allowed(current_status, next_status)
    else:
        result = ensure_transition_allowed(current_status, next_status)
        assert result is True
