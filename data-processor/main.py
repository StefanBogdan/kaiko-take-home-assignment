"""Data Processing Service - Handles medical data transformation and validation."""

import time
from typing import Dict, List

import pandas as pd
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from utils.validation import validate_dataframe_schema, sanitize_input_data, validate_numeric_range
from utils.logging_config import setup_logger, log_request_info, log_data_processing_stats


app = FastAPI(title="Data Processor Service", version="1.0.0")
logger = setup_logger("data-processor")


class ProcessingRequest(BaseModel):
    data: List[Dict]
    operation: str
    parameters: Dict = {}


class ProcessingResponse(BaseModel):
    processed_data: List[Dict]
    stats: Dict
    status: str


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "data-processor"}


@app.post("/process", response_model=ProcessingResponse)
async def process_data(request: ProcessingRequest):
    """Process incoming data with specified operation."""
    start_time = time.time()

    try:
        # Sanitize input data
        sanitized_data = [sanitize_input_data(item) for item in request.data]

        # Convert to DataFrame for processing
        df = pd.DataFrame(sanitized_data)

        if request.operation == "aggregate":
            # Validate required columns for aggregation
            required_cols = request.parameters.get("group_by", [])
            if required_cols:
                validate_dataframe_schema(df, required_cols)

            # Perform aggregation
            if required_cols and "value" in df.columns:
                result_df = df.groupby(required_cols)["value"].sum().reset_index()
            else:
                result_df = df.describe()

        elif request.operation == "filter":
            # Filter data based on parameters
            min_val = request.parameters.get("min_value")
            max_val = request.parameters.get("max_value")

            if "value" in df.columns and (min_val is not None or max_val is not None):
                mask = pd.Series([True] * len(df))
                if min_val is not None:
                    mask &= df["value"] >= min_val
                if max_val is not None:
                    mask &= df["value"] <= max_val
                result_df = df[mask]
            else:
                result_df = df

        elif request.operation == "validate":
            # Validate numeric ranges if specified
            if "value" in df.columns:
                min_val = request.parameters.get("min_value")
                max_val = request.parameters.get("max_value")
                for value in df["value"]:
                    validate_numeric_range(float(value), min_val, max_val)
            result_df = df

        else:
            raise HTTPException(status_code=400, detail=f"Unknown operation: {request.operation}")

        # Convert back to list of dicts
        processed_data = result_df.to_dict("records")

        duration = time.time() - start_time

        # Log processing stats
        log_data_processing_stats(logger, request.operation, len(processed_data), duration)

        response = ProcessingResponse(
            processed_data=processed_data,
            stats={
                "input_records": len(request.data),
                "output_records": len(processed_data),
                "duration_seconds": round(duration, 3),
                "operation": request.operation
            },
            status="success"
        )

        return response

    except Exception as e:
        duration = time.time() - start_time
        logger.error(f"Processing failed after {duration:.3f}s: {str(e)}")
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
    logger.info("Starting Data Processor Service...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
