from __future__ import annotations
from datetime import datetime
from unittest.mock import Mock

import pytest


class TestPublicStatistics:
    def test_public_statistics_empty(self,statistics_service):
        statistics_service.report_repository.list_reports.return_value = []
        statistics_service._aggregate_trends = Mock(return_value={})

        result = statistics_service.public_statistics()
        assert result["reports_by_category"] == {}
        assert result["trends"] == {}
        assert result["total_reports"] == 0
    
    def test_public_statistics_2_iterations(self, statistics_service):
        """più report presentir"""
        report1 = Mock()
        report1.category.name = "Ambiente"
        
        report2 = Mock()
        report2.category.name = "Strade"
   
        report3 = Mock()
        report3.category.name = "Ambiente"  # stessa categoria di report1

        reports_list = [report1, report2, report3]
        statistics_service.report_repository.list_reports.return_value = reports_list
        
        mock_trends = {"Ambiente": 2, "Strade": 1} 
        statistics_service._aggregate_trends = Mock(return_value=mock_trends)

        result = statistics_service.public_statistics(granularity="year")

        assert result["reports_by_category"] == {"Ambiente": 2, "Strade": 1}
        assert result["trends"] == mock_trends
        assert result["total_reports"] == 3
        statistics_service.report_repository.list_reports.assert_called_once_with(public_only=True)
        statistics_service._aggregate_trends.assert_called_once_with(reports_list, "year")
    
class TestAdminStatistics:
    def test_admin_statistics_empty(self, statistics_service):
        """Nessun report presente"""
        statistics_service.report_repository.list_all.return_value = []
        statistics_service._top_percent_breakdown = Mock(return_value={})
        result = statistics_service.admin_statistics()

        assert result["reports_by_status"] == {}
        assert result["reports_by_type"] == {}
        assert result["reports_by_type_and_status"] == {}
        assert result["reports_by_reporter"] == {}
        assert result["reports_by_reporter_and_type"] == {}
        assert result["reports_by_reporter_type_and_status"] == {}
        assert result["top_1_percent_by_type"] == {}
        assert result["top_5_percent_by_type"] == {}
        statistics_service.report_repository.list_all.assert_called_once()
        assert statistics_service._top_percent_breakdown.call_count == 2
        statistics_service._top_percent_breakdown.assert_any_call([], 1)
        statistics_service._top_percent_breakdown.assert_any_call([], 5)
    
    def test_admin_statistics_2_iterations(self, statistics_service):
        """più report presentir"""
        report1 = Mock()
        report1.status = Mock()
        report1.status.value = "pending"
        report1.category = Mock()
        report1.category.name = "Ambiente"

        report2 = Mock()
        report2.status = Mock()
        report2.status.value = "approved"
        report2.category = Mock()
        report2.category.name = "Strade"

        report3 = Mock()
        report3.status = Mock()
        report3.status.value = "pending" #come report 1
        report3.category = Mock()
        report3.category.name = "Ambiente" #come report 1

        reports_list = [report1, report2, report3]
        statistics_service.report_repository.list_all.return_value = reports_list
        statistics_service._reporter_label = Mock(side_effect=lambda r: "Cittadino" if r.category.name == "Ambiente" else "Anonimo")
        
        mock_top_1 = {"Ambiente": ["rep1"]}
        mock_top_5 = {"Ambiente": ["rep1"], "Strade": ["rep2"]}
        statistics_service._top_percent_breakdown = Mock(side_effect=[mock_top_1, mock_top_5])

        result = statistics_service.admin_statistics()

        assert result["reports_by_status"] == {"pending": 2, "approved": 1}
        assert result["reports_by_type"] == {"Ambiente": 2, "Strade": 1}
        assert result["reports_by_type_and_status"] == {"Ambiente | pending": 2, "Strade | approved": 1}
        assert result["reports_by_reporter"] == {"Cittadino": 2, "Anonimo": 1}
        assert result["reports_by_reporter_and_type"] == {"Cittadino | Ambiente": 2, "Anonimo | Strade": 1}
        assert result["reports_by_reporter_type_and_status"] == {"Cittadino | Ambiente | pending": 2,"Anonimo | Strade | approved": 1}
        assert result["top_1_percent_by_type"] == mock_top_1
        assert result["top_5_percent_by_type"] == mock_top_5

        statistics_service.report_repository.list_all.assert_called_once()
        statistics_service._top_percent_breakdown.assert_any_call(reports_list, 1)
        statistics_service._top_percent_breakdown.assert_any_call(reports_list, 5)

class TestAggregateTrends:
    def test_aggregate_trends_zero_iterations(self, statistics_service):
        """0 iterazioni"""
        reports_list = []
        result = statistics_service._aggregate_trends(reports_list, granularity="day")
        assert result == {}

    def test_aggregate_trends_one_iteration_month(self, statistics_service, mock_report):
        """1 iterazione: month"""
        mock_report.created_at = datetime(2026, 5, 20)
        result = statistics_service._aggregate_trends([mock_report], granularity="month")
        assert result == {"2026-05": 1}

    def test_aggregate_trends_one_iteration_week(self, statistics_service, mock_report):
        """1 iterazione: week"""
        mock_report.created_at = datetime(2026, 5, 20)
        result = statistics_service._aggregate_trends([mock_report], granularity="week")
        assert result == {"2026-W21": 1}

    def test_aggregate_trends_one_iteration_default(self, statistics_service, mock_report):
        """1 iterazione: day"""
        mock_report.created_at = datetime(2026, 5, 20)
        result = statistics_service._aggregate_trends([mock_report], granularity="day")
        assert result == {"2026-05-20": 1}

    def test_aggregate_trends_two_iterations_sorting_and_buckets(self, statistics_service):
        """2 iterazioni"""

        report1 = Mock()
        report1.created_at = datetime(2026, 5, 22) 
        report2 = Mock()
        report2.created_at = datetime(2026, 5, 21) # Giorno prima
        report3 = Mock()
        report3.created_at = datetime(2026, 5, 21) # Stesso giorno di report2 per testare l'incremento (+1)

        result = statistics_service._aggregate_trends([report1, report2, report3], granularity="day")
        
        assert result == {"2026-05-21": 2,"2026-05-22": 1}
        assert list(result.keys()) == ["2026-05-21", "2026-05-22"]

class TestTopPercentBreakdown:
    def test_top_percent_breakdown_zero_iterations(self, statistics_service):
        """0 report"""
        result = statistics_service._top_percent_breakdown([], percent=5)
        assert result == {}

    def test_top_percent_breakdown_one_iteration(self, statistics_service, mock_report):
        """1 report"""
        mock_report.category = Mock()
        mock_report.category.name = "Strade"
        statistics_service._reporter_label = Mock(return_value="Cittadino_42")
        result = statistics_service._top_percent_breakdown([mock_report], percent=100)
        assert result == {"Strade": 1}
        statistics_service._reporter_label.assert_called()

    def test_top_percent_breakdown_two_iterations_filtering(self, statistics_service):
        """3 report, con 2 diversi"""
        report1 = Mock()
        report1.category = Mock()
        report1.category.name = "Ambiente"

        report2 = Mock()
        report2.category = Mock()
        report2.category.name = "Ambiente"

        report3 = Mock()
        report3.category = Mock()
        report3.category.name = "Strade"

        reports_list = [report1, report2, report3]

        statistics_service._reporter_label = Mock(side_effect=lambda r: (
            "Cittadino" if r in [report1, report2] else "Anonimo"
        ))
        result = statistics_service._top_percent_breakdown(reports_list, percent=50)

        assert result == {"Ambiente": 2}
        assert "Strade" not in result

class TestReporterLabel:
    def test_reporter_label(self,statistics_service, mock_report):
        mock_report.reporter.username = "test_user"
        mock_report.reporter.id = 1
        result = statistics_service._reporter_label(mock_report)
        assert result == f"{mock_report.reporter.username} ({mock_report.reporter.id})"
    
    def test_reporter_label_deleted(self,statistics_service, mock_report):
        mock_report.reporter = None
        result = statistics_service._reporter_label(mock_report)
        assert result == "Deleted Citizen"



        

