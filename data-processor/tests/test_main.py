"""Tests for data processor service."""

import pytest
from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_health_check():
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "data-processor"


def test_process_aggregate():
    """Test data aggregation processing."""
    request_data = {
        "data": [
            {"category": "A", "value": 10},
            {"category": "A", "value": 20},
            {"category": "B", "value": 15}
        ],
        "operation": "aggregate",
        "parameters": {"group_by": ["category"]}
    }

    response = client.post("/process", json=request_data)
    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "success"
    assert data["stats"]["input_records"] == 3
    assert len(data["processed_data"]) == 2


def test_process_filter():
    """Test data filtering processing."""
    request_data = {
        "data": [
            {"id": 1, "value": 5},
            {"id": 2, "value": 15},
            {"id": 3, "value": 25}
        ],
        "operation": "filter",
        "parameters": {"min_value": 10, "max_value": 20}
    }

    response = client.post("/process", json=request_data)
    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "success"
    assert len(data["processed_data"]) == 1
    assert data["processed_data"][0]["value"] == 15


def test_process_validate():
    """Test data validation processing."""
    request_data = {
        "data": [
            {"id": 1, "value": 5},
            {"id": 2, "value": 15}
        ],
        "operation": "validate",
        "parameters": {"min_value": 0, "max_value": 20}
    }

    response = client.post("/process", json=request_data)
    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "success"


def test_process_invalid_operation():
    """Test invalid operation handling."""
    request_data = {
        "data": [{"id": 1, "value": 5}],
        "operation": "unknown_operation"
    }

    response = client.post("/process", json=request_data)
    assert response.status_code == 400
