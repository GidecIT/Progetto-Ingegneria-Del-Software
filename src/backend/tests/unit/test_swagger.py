from __future__ import annotations

import pytest
from unittest.mock import MagicMock, patch
from participium.api.swagger import _array_of, _message_response, _definitions, init_swagger

def test_array_of():
    """Test the _array_of helper function."""
    result = _array_of("TestDefinition")
    assert result == {
        "type": "array",
        "items": {"$ref": "#/definitions/TestDefinition"},
    }

def test_message_response():
    """Test the _message_response helper function."""
    message = "Test message"
    result = _message_response(message)
    assert result["type"] == "object"
    assert "message" in result["required"]
    assert result["properties"]["message"]["example"] == message

def test_definitions_contains_key_entities():
    """Test that _definitions returns a dict containing essential API models."""
    definitions = _definitions()
    
    assert "Error" in definitions
    assert "Health" in definitions
    assert "User" in definitions
    assert "Category" in definitions
    assert "ReportSummary" in definitions
    assert "ReportDetail" in definitions
    assert "Message" in definitions
    assert "Notification" in definitions

def test_definitions_error_structure():
    """Test the structure of the Error definition."""
    definitions = _definitions()
    error_def = definitions["Error"]
    
    assert error_def["type"] == "object"
    assert "error" in error_def["required"]
    assert "error" in error_def["properties"]
    assert error_def["properties"]["error"]["type"] == "string"

def test_definitions_health_structure():
    """Test the structure of the Health definition."""
    definitions = _definitions()
    health_def = definitions["Health"]
    
    assert health_def["type"] == "object"
    assert "status" in health_def["required"]
    assert health_def["properties"]["status"]["example"] == "ok"

def test_definitions_enums():
    """Test that important enums are correctly defined."""
    definitions = _definitions()
    
    # Check User role enum (found in User definition or similar)
    user_def = definitions["User"]
    assert "role" in user_def["properties"]
    assert user_def["properties"]["role"]["enum"] == ["citizen", "operator", "admin"]
    
    # Check Report status enum
    report_def = definitions["ReportSummary"]
    assert "status" in report_def["properties"]
    expected_statuses = [
        "pending_approval",
        "rejected",
        "assigned",
        "in_progress",
        "resolved",
    ]
    assert report_def["properties"]["status"]["enum"] == expected_statuses

def test_init_swagger():
    """Test the init_swagger function."""
    app = MagicMock()
    with patch("participium.api.swagger.Swagger") as mock_swagger:
        init_swagger(app)
        
        # Verify Swagger was initialized with the app and a template
        mock_swagger.assert_called_once()
        args, kwargs = mock_swagger.call_args
        assert args[0] == app
        assert "template" in kwargs
        
        template = kwargs["template"]
        assert template["swagger"] == "2.0"
        assert template["info"]["title"] == "Participium API"
        assert "/api/v1" in template["basePath"]
        assert "definitions" in template
