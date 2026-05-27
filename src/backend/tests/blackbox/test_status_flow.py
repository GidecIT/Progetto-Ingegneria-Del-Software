from __future__ import annotations

from participium.core.status_flow import ensure_transition_allowed

import pytest
from participium.core.exceptions import ValidationError
from participium.models.enums import ReportStatus


@pytest.mark.parametrize(
    "current_status, next_status, expected_exception_or_result",
    [
        # --- PENDING APPROVAL (EC1) ---
        (ReportStatus.PENDING_APPROVAL, ReportStatus.PENDING_APPROVAL, True),            # TR1 
        (ReportStatus.PENDING_APPROVAL, ReportStatus.ASSIGNED, True),                    # TR2 
        (ReportStatus.PENDING_APPROVAL, ReportStatus.REJECTED, True),                    # TR3 
        (ReportStatus.PENDING_APPROVAL, ReportStatus.RESOLVED, ValidationError),          # TR4 

        # --- ASSIGNED (EC2) ---
        (ReportStatus.ASSIGNED, ReportStatus.ASSIGNED, True),                            # TR5 
        (ReportStatus.ASSIGNED, ReportStatus.IN_PROGRESS, True),                         # TR6 
        (ReportStatus.ASSIGNED, ReportStatus.SUSPENDED, True),                           # TR7 
        (ReportStatus.ASSIGNED, ReportStatus.RESOLVED, True),                            # TR8 
        (ReportStatus.ASSIGNED, ReportStatus.PENDING_APPROVAL, ValidationError),         # TR9 

        # --- IN PROGRESS (EC3) ---
        (ReportStatus.IN_PROGRESS, ReportStatus.IN_PROGRESS, True),                      # TR10 
        (ReportStatus.IN_PROGRESS, ReportStatus.SUSPENDED, True),                         # TR11
        (ReportStatus.IN_PROGRESS, ReportStatus.RESOLVED, True),                          # TR12 
        (ReportStatus.IN_PROGRESS, ReportStatus.ASSIGNED, ValidationError),              # TR13 

        # --- SUSPENDED (EC4) ---
        (ReportStatus.SUSPENDED, ReportStatus.SUSPENDED, True),                          # TR14 
        (ReportStatus.SUSPENDED, ReportStatus.IN_PROGRESS, True),                        # TR15 
        (ReportStatus.SUSPENDED, ReportStatus.RESOLVED, True),                           # TR16 
        (ReportStatus.SUSPENDED, ReportStatus.PENDING_APPROVAL, ValidationError),        # TR17 

        # --- REJECTED (EC5) ---
        (ReportStatus.REJECTED, ReportStatus.REJECTED, True),                            # TR18 
        (ReportStatus.REJECTED, ReportStatus.ASSIGNED, ValidationError),                 # TR19 

        # --- RESOLVED (EC6) ---
        (ReportStatus.RESOLVED, ReportStatus.RESOLVED, True),                            # TR20 
        (ReportStatus.RESOLVED, ReportStatus.IN_PROGRESS, ValidationError),              # TR21 
    ],
)
def test_ensure_transition_allowed(current_status: ReportStatus, next_status: ReportStatus, expected_exception_or_result: bool | type[Exception]):
    
    if expected_exception_or_result is ValidationError:
        with pytest.raises(ValidationError):
            ensure_transition_allowed(current_status, next_status)
    else:
        result = ensure_transition_allowed(current_status, next_status)
        assert result is True
