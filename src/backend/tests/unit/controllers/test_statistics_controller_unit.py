from __future__ import annotations
import pytest
from unittest.mock import Mock


class TestStatisticsController:
    def test_public_statistics_delegates_to_service_with_default_granularity(
        self, statistics_controller
    ):
        mock_result = {"2026-05-28": {"reports_count": 5}, "total": 5}
        statistics_controller.statistics_service.public_statistics = Mock(return_value=mock_result)

        result = statistics_controller.public_statistics()

        assert result == mock_result
        statistics_controller.statistics_service.public_statistics.assert_called_once_with("day")

    def test_public_statistics_delegates_to_service_with_custom_granularity(
        self, statistics_controller
    ):
        mock_result = {"2026-05": {"reports_count": 120}, "total": 120}
        statistics_controller.statistics_service.public_statistics = Mock(return_value=mock_result)

        result = statistics_controller.public_statistics(granularity="month")

        assert result == mock_result
        statistics_controller.statistics_service.public_statistics.assert_called_once_with("month")

    def test_public_statistics_propagates_service_errors(
        self, statistics_controller
    ):
        expected_exception = ValueError("Invalid granularity level specified")
        statistics_controller.statistics_service.public_statistics = Mock(side_effect=expected_exception)

        with pytest.raises(ValueError) as exc_info:
            statistics_controller.public_statistics(granularity="invalid_value")

        assert exc_info.value is expected_exception
        statistics_controller.statistics_service.public_statistics.assert_called_once_with("invalid_value")