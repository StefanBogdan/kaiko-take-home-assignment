"""Tests for model service."""

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
    assert data["service"] == "model-service"


def test_list_models_empty():
    """Test listing models when none are trained."""
    response = client.get("/models")
    assert response.status_code == 200
    data = response.json()
    assert "models" in data


def test_train_model():
    """Test model training."""
    training_data = {
        "data": [
            {"feature1": 1.0, "feature2": 2.0, "target": 0},
            {"feature1": 2.0, "feature2": 3.0, "target": 1},
            {"feature1": 3.0, "feature2": 4.0, "target": 1},
            {"feature1": 0.5, "feature2": 1.0, "target": 0}
        ],
        "target_column": "target",
        "model_name": "test_model",
        "features": ["feature1", "feature2"]
    }

    response = client.post("/train", json=training_data)
    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "success"
    assert data["model_name"] == "test_model"
    assert "accuracy" in data
    assert data["stats"]["training_samples"] == 4


def test_predict_with_trained_model():
    """Test prediction with previously trained model."""
    # First train a model
    training_data = {
        "data": [
            {"feature1": 1.0, "feature2": 2.0, "target": 0},
            {"feature1": 2.0, "feature2": 3.0, "target": 1},
            {"feature1": 3.0, "feature2": 4.0, "target": 1}
        ],
        "target_column": "target",
        "model_name": "predict_test_model"
    }

    train_response = client.post("/train", json=training_data)
    assert train_response.status_code == 200

    # Now make predictions
    prediction_data = {
        "data": [
            {"feature1": 1.5, "feature2": 2.5},
            {"feature1": 2.5, "feature2": 3.5}
        ],
        "model_name": "predict_test_model"
    }

    response = client.post("/predict", json=prediction_data)
    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "success"
    assert data["model_name"] == "predict_test_model"
    assert len(data["predictions"]) == 2


def test_predict_with_nonexistent_model():
    """Test prediction with model that doesn't exist."""
    prediction_data = {
        "data": [{"feature1": 1.0, "feature2": 2.0}],
        "model_name": "nonexistent_model"
    }

    response = client.post("/predict", json=prediction_data)
    assert response.status_code == 404


def test_train_model_missing_target():
    """Test training with missing target column."""
    training_data = {
        "data": [
            {"feature1": 1.0, "feature2": 2.0}
        ],
        "target_column": "missing_target",
        "model_name": "invalid_model"
    }

    response = client.post("/train", json=training_data)
    assert response.status_code == 400
