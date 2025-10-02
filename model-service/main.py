"""Model Service - Handles ML model inference and predictions."""

import time
from typing import Dict, List, Optional

import numpy as np
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

from utils.validation import validate_dataframe_schema, sanitize_input_data, validate_numeric_range
from utils.logging_config import setup_logger, log_request_info, log_data_processing_stats


app = FastAPI(title="Model Service", version="1.0.0")
logger = setup_logger("model-service")

# Simple in-memory model storage
models = {}
scalers = {}


class TrainingRequest(BaseModel):
    data: List[Dict]
    target_column: str
    model_name: str
    features: Optional[List[str]] = None


class PredictionRequest(BaseModel):
    data: List[Dict]
    model_name: str


class PredictionResponse(BaseModel):
    predictions: List[float]
    model_name: str
    stats: Dict
    status: str


class TrainingResponse(BaseModel):
    model_name: str
    accuracy: float
    stats: Dict
    status: str


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "model-service"}


@app.get("/models")
async def list_models():
    """List available trained models."""
    return {"models": list(models.keys())}


@app.post("/train", response_model=TrainingResponse)
async def train_model(request: TrainingRequest):
    """Train a new model with provided data."""
    start_time = time.time()

    try:
        # Sanitize input data
        sanitized_data = [sanitize_input_data(item) for item in request.data]
        df = pd.DataFrame(sanitized_data)

        # Validate required columns
        required_columns = [request.target_column]
        if request.features:
            required_columns.extend(request.features)

        validate_dataframe_schema(df, required_columns)

        # Prepare features and target
        if request.features:
            feature_columns = request.features
        else:
            feature_columns = [col for col in df.columns if col != request.target_column]

        X = df[feature_columns].select_dtypes(include=[np.number])
        y = df[request.target_column]

        if X.empty:
            raise ValueError("No numeric features found for training")

        # Validate feature ranges
        for col in X.columns:
            for value in X[col]:
                validate_numeric_range(float(value), -1000000, 1000000)

        # Scale features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        # Train model
        model = RandomForestClassifier(n_estimators=10, random_state=42)
        model.fit(X_scaled, y)

        # Store model and scaler
        models[request.model_name] = {
            "model": model,
            "feature_columns": feature_columns
        }
        scalers[request.model_name] = scaler

        # Calculate accuracy on training data (for demo purposes)
        predictions = model.predict(X_scaled)
        accuracy = np.mean(predictions == y)

        duration = time.time() - start_time

        # Log training stats
        log_data_processing_stats(logger, f"model_training_{request.model_name}",
                                len(request.data), duration)

        response = TrainingResponse(
            model_name=request.model_name,
            accuracy=round(accuracy, 3),
            stats={
                "training_samples": len(request.data),
                "features_used": len(feature_columns),
                "duration_seconds": round(duration, 3)
            },
            status="success"
        )

        return response

    except Exception as e:
        duration = time.time() - start_time
        logger.error(f"Training failed after {duration:.3f}s: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    """Make predictions using a trained model."""
    start_time = time.time()

    try:
        if request.model_name not in models:
            raise HTTPException(status_code=404, detail=f"Model '{request.model_name}' not found")

        # Sanitize input data
        sanitized_data = [sanitize_input_data(item) for item in request.data]
        df = pd.DataFrame(sanitized_data)

        # Get model and scaler
        model_info = models[request.model_name]
        model = model_info["model"]
        feature_columns = model_info["feature_columns"]
        scaler = scalers[request.model_name]

        # Validate required columns
        validate_dataframe_schema(df, feature_columns)

        # Prepare features
        X = df[feature_columns].select_dtypes(include=[np.number])

        # Validate feature ranges
        for col in X.columns:
            for value in X[col]:
                validate_numeric_range(float(value), -1000000, 1000000)

        # Scale features and predict
        X_scaled = scaler.transform(X)
        predictions = model.predict(X_scaled)

        duration = time.time() - start_time

        # Log prediction stats
        log_data_processing_stats(logger, f"model_prediction_{request.model_name}",
                                len(request.data), duration)

        response = PredictionResponse(
            predictions=predictions.tolist(),
            model_name=request.model_name,
            stats={
                "input_samples": len(request.data),
                "duration_seconds": round(duration, 3)
            },
            status="success"
        )

        return response

    except Exception as e:
        duration = time.time() - start_time
        logger.error(f"Prediction failed after {duration:.3f}s: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


@app.middleware("http")
async def log_requests(request, call_next):
    """Log all HTTP requests."""
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    log_request_info(logger, request.method, str(request.url.path),
                    response.status_code, duration)
    return response


if __name__ == "__main__":
    logger.info("Starting Model Service...")
    uvicorn.run(app, host="0.0.0.0", port=8001)
