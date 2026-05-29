from __future__ import annotations
from unittest.mock import patch
import pytest

from participium.core.exceptions import ValidationError
from participium.models.enums import ReportStatus
from participium.core.status_flow import ensure_transition_allowed


MOCK_STATUS_TRANSITIONS = {
    ReportStatus.PENDING_APPROVAL: {ReportStatus.ASSIGNED, ReportStatus.REJECTED},
    ReportStatus.ASSIGNED: {ReportStatus.IN_PROGRESS, ReportStatus.SUSPENDED, ReportStatus.RESOLVED},
    ReportStatus.IN_PROGRESS: {ReportStatus.SUSPENDED, ReportStatus.RESOLVED},
    ReportStatus.SUSPENDED: {ReportStatus.IN_PROGRESS, ReportStatus.RESOLVED},
    ReportStatus.REJECTED: set(),
    ReportStatus.RESOLVED: set(),
}


class TestEnsureTransitionAllowed:
    @pytest.mark.parametrize("status", list(ReportStatus))
    def test_self_transition_always_allowed(self, status):
        with patch("participium.core.status_flow.DEFAULT_STATUS_TRANSITIONS", MOCK_STATUS_TRANSITIONS):
            assert ensure_transition_allowed(status, status) is True

    @pytest.mark.parametrize(
        "current,next_status",
        [
            (ReportStatus.PENDING_APPROVAL, ReportStatus.ASSIGNED),
            (ReportStatus.PENDING_APPROVAL, ReportStatus.REJECTED),
            (ReportStatus.ASSIGNED, ReportStatus.IN_PROGRESS),
            (ReportStatus.ASSIGNED, ReportStatus.SUSPENDED),
            (ReportStatus.ASSIGNED, ReportStatus.RESOLVED),
            (ReportStatus.IN_PROGRESS, ReportStatus.SUSPENDED),
            (ReportStatus.IN_PROGRESS, ReportStatus.RESOLVED),
            (ReportStatus.SUSPENDED, ReportStatus.IN_PROGRESS),
            (ReportStatus.SUSPENDED, ReportStatus.RESOLVED),
        ],
    )
    def test_valid_transitions_allowed(self, current, next_status):
        with patch("participium.core.status_flow.DEFAULT_STATUS_TRANSITIONS", MOCK_STATUS_TRANSITIONS):
            assert ensure_transition_allowed(current, next_status) is True

    @pytest.mark.parametrize(
        "current,next_status",
        [
            (ReportStatus.PENDING_APPROVAL, ReportStatus.IN_PROGRESS),
            (ReportStatus.PENDING_APPROVAL, ReportStatus.RESOLVED),
            (ReportStatus.ASSIGNED, ReportStatus.PENDING_APPROVAL),
            (ReportStatus.ASSIGNED, ReportStatus.REJECTED),
            (ReportStatus.IN_PROGRESS, ReportStatus.PENDING_APPROVAL),
            (ReportStatus.IN_PROGRESS, ReportStatus.ASSIGNED),
            (ReportStatus.IN_PROGRESS, ReportStatus.REJECTED),
            (ReportStatus.SUSPENDED, ReportStatus.PENDING_APPROVAL),
            (ReportStatus.SUSPENDED, ReportStatus.ASSIGNED),
            (ReportStatus.SUSPENDED, ReportStatus.REJECTED),
            (ReportStatus.REJECTED, ReportStatus.PENDING_APPROVAL),
            (ReportStatus.REJECTED, ReportStatus.ASSIGNED),
            (ReportStatus.RESOLVED, ReportStatus.IN_PROGRESS),
        ],
    )
    def test_invalid_transitions_raise_validation_error(self, current, next_status):
        with patch("participium.core.status_flow.DEFAULT_STATUS_TRANSITIONS", MOCK_STATUS_TRANSITIONS):
            with pytest.raises(ValidationError):
                ensure_transition_allowed(current, next_status)

    def test_empty_or_missing_status_transitions_raises_error(self):
        with patch("participium.core.status_flow.DEFAULT_STATUS_TRANSITIONS", {}):
            with pytest.raises(ValidationError):
                ensure_transition_allowed(ReportStatus.PENDING_APPROVAL, ReportStatus.ASSIGNED)