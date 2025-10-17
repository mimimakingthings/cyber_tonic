"""
REST API for Cyber Tonic

This module provides a FastAPI-based REST API for external integrations
and programmatic access to Cyber Tonic functionality.

Features:
- Standards data access
- Assessment management
- Report generation
- Client management
- Authentication and authorization
"""

from fastapi import FastAPI, HTTPException, Depends, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
import json
from datetime import datetime
from pathlib import Path

# Import Cyber Tonic modules
from .standards_loader import standards_loader
from .data_persistence import DataManager
from .utils import validate_assessment_data, generate_report

# Initialize FastAPI app
app = FastAPI(
    title="Cyber Tonic API",
    description="REST API for Cyber Tonic cybersecurity compliance platform",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Pydantic models
class StandardResponse(BaseModel):
    """Response model for standard data."""
    standard_id: str
    name: str
    overview: str
    region: str
    version: str
    functions: Dict[str, Any]

class ControlResponse(BaseModel):
    """Response model for control data."""
    control_id: str
    description: str
    examples: str
    use_cases: str
    regional_relevance: str
    tech_recommendations: List[str]
    mappings: Dict[str, str]

class AssessmentRequest(BaseModel):
    """Request model for assessment data."""
    client_id: str
    standard_id: str = "nist-csf-2.0"
    scores: Dict[str, float] = Field(..., description="Control scores (0-10)")
    weights: Optional[Dict[str, float]] = None
    notes: Optional[str] = None

class AssessmentResponse(BaseModel):
    """Response model for assessment results."""
    assessment_id: str
    client_id: str
    standard_id: str
    overall_score: float
    function_scores: Dict[str, float]
    gap_analysis: Dict[str, Any]
    created_date: datetime
    last_updated: datetime

class ClientRequest(BaseModel):
    """Request model for client data."""
    name: str
    industry: str
    contact: Dict[str, str]
    size: str
    notes: Optional[str] = None

class ClientResponse(BaseModel):
    """Response model for client data."""
    id: str
    name: str
    industry: str
    contact: Dict[str, str]
    size: str
    notes: Optional[str] = None
    created_date: datetime

class ReportRequest(BaseModel):
    """Request model for report generation."""
    assessment_id: str
    format: str = Field(..., regex="^(markdown|pdf|csv)$")
    include_charts: bool = True
    include_gap_analysis: bool = True

# Authentication (placeholder - implement proper auth)
async def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    """Verify API token (placeholder implementation)."""
    # TODO: Implement proper JWT token verification
    if credentials.credentials != "your-api-token":
        raise HTTPException(status_code=401, detail="Invalid token")
    return credentials.credentials

# API Routes

@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Cyber Tonic API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "timestamp": datetime.now()}

# Standards endpoints
@app.get("/standards", response_model=List[Dict[str, Any]])
async def get_standards():
    """Get all available standards."""
    try:
        index = standards_loader.load_index()
        return [
            {
                "standard_id": std_id,
                "metadata": metadata
            }
            for std_id, metadata in index["standards"].items()
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading standards: {str(e)}")

@app.get("/standards/{standard_id}", response_model=StandardResponse)
async def get_standard(standard_id: str):
    """Get a specific standard by ID."""
    try:
        standard_data = standards_loader.load_standard(standard_id)
        return StandardResponse(**standard_data)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Standard not found: {str(e)}")

@app.get("/standards/{standard_id}/controls", response_model=List[ControlResponse])
async def get_controls(standard_id: str, function: Optional[str] = None):
    """Get controls for a standard, optionally filtered by function."""
    try:
        standard_data = standards_loader.load_standard(standard_id)
        controls = []
        
        for func_name, func_data in standard_data.get("functions", {}).items():
            if function and func_name != function:
                continue
                
            for control_id, control_data in func_data.get("subcategories", {}).items():
                controls.append(ControlResponse(
                    control_id=control_id,
                    **control_data
                ))
        
        return controls
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Error loading controls: {str(e)}")

@app.get("/standards/{standard_id}/search")
async def search_controls(standard_id: str, q: str):
    """Search controls within a standard."""
    try:
        results = standards_loader.search_controls(q, [standard_id])
        return results.get(standard_id, {})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search error: {str(e)}")

# Client endpoints
@app.get("/clients", response_model=List[ClientResponse])
async def get_clients(token: str = Depends(verify_token)):
    """Get all clients."""
    try:
        data_manager = DataManager()
        clients_data = data_manager.load_clients()
        return [
            ClientResponse(**client) for client in clients_data.get("clients", [])
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading clients: {str(e)}")

@app.post("/clients", response_model=ClientResponse)
async def create_client(client: ClientRequest, token: str = Depends(verify_token)):
    """Create a new client."""
    try:
        data_manager = DataManager()
        client_id = data_manager.add_client(
            name=client.name,
            industry=client.industry,
            contact=client.contact,
            size=client.size,
            notes=client.notes
        )
        
        # Return the created client
        clients_data = data_manager.load_clients()
        for c in clients_data.get("clients", []):
            if c["id"] == client_id:
                return ClientResponse(**c)
        
        raise HTTPException(status_code=500, detail="Error creating client")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating client: {str(e)}")

@app.get("/clients/{client_id}", response_model=ClientResponse)
async def get_client(client_id: str, token: str = Depends(verify_token)):
    """Get a specific client by ID."""
    try:
        data_manager = DataManager()
        clients_data = data_manager.load_clients()
        
        for client in clients_data.get("clients", []):
            if client["id"] == client_id:
                return ClientResponse(**client)
        
        raise HTTPException(status_code=404, detail="Client not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading client: {str(e)}")

# Assessment endpoints
@app.post("/assessments", response_model=AssessmentResponse)
async def create_assessment(assessment: AssessmentRequest, token: str = Depends(verify_token)):
    """Create a new assessment."""
    try:
        data_manager = DataManager()
        
        # Validate assessment data
        if not validate_assessment_data(assessment.scores):
            raise HTTPException(status_code=400, detail="Invalid assessment data")
        
        # Create assessment
        assessment_id = data_manager.create_assessment(
            client_id=assessment.client_id,
            standard_id=assessment.standard_id,
            scores=assessment.scores,
            weights=assessment.weights,
            notes=assessment.notes
        )
        
        # Calculate results
        results = data_manager.calculate_assessment_results(assessment_id)
        
        return AssessmentResponse(
            assessment_id=assessment_id,
            client_id=assessment.client_id,
            standard_id=assessment.standard_id,
            overall_score=results["overall_score"],
            function_scores=results["function_scores"],
            gap_analysis=results["gap_analysis"],
            created_date=datetime.now(),
            last_updated=datetime.now()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating assessment: {str(e)}")

@app.get("/assessments/{assessment_id}", response_model=AssessmentResponse)
async def get_assessment(assessment_id: str, token: str = Depends(verify_token)):
    """Get a specific assessment by ID."""
    try:
        data_manager = DataManager()
        assessment_data = data_manager.load_assessment(assessment_id)
        
        if not assessment_data:
            raise HTTPException(status_code=404, detail="Assessment not found")
        
        return AssessmentResponse(**assessment_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading assessment: {str(e)}")

@app.get("/clients/{client_id}/assessments", response_model=List[AssessmentResponse])
async def get_client_assessments(client_id: str, token: str = Depends(verify_token)):
    """Get all assessments for a client."""
    try:
        data_manager = DataManager()
        assessments = data_manager.get_client_assessments(client_id)
        
        return [AssessmentResponse(**assessment) for assessment in assessments]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading assessments: {str(e)}")

# Report endpoints
@app.post("/reports/generate")
async def generate_report_endpoint(report_request: ReportRequest, token: str = Depends(verify_token)):
    """Generate a report for an assessment."""
    try:
        data_manager = DataManager()
        assessment_data = data_manager.load_assessment(report_request.assessment_id)
        
        if not assessment_data:
            raise HTTPException(status_code=404, detail="Assessment not found")
        
        # Generate report
        report_content = generate_report(
            assessment_data=assessment_data,
            format=report_request.format,
            include_charts=report_request.include_charts,
            include_gap_analysis=report_request.include_gap_analysis
        )
        
        return {
            "report_id": f"report_{report_request.assessment_id}_{datetime.now().isoformat()}",
            "format": report_request.format,
            "content": report_content,
            "generated_date": datetime.now()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating report: {str(e)}")

# Statistics endpoints
@app.get("/stats/standards")
async def get_standards_stats():
    """Get statistics about available standards."""
    try:
        stats = standards_loader.get_statistics()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading statistics: {str(e)}")

@app.get("/stats/assessments")
async def get_assessments_stats(token: str = Depends(verify_token)):
    """Get statistics about assessments."""
    try:
        data_manager = DataManager()
        stats = data_manager.get_assessment_statistics()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading assessment statistics: {str(e)}")

# Cross-mapping endpoints
@app.get("/mappings/{standard_id}/{control_id}")
async def get_control_mappings(standard_id: str, control_id: str):
    """Get cross-mappings for a specific control."""
    try:
        mappings = standards_loader.get_cross_mappings(control_id, standard_id)
        return {
            "control_id": control_id,
            "standard_id": standard_id,
            "mappings": mappings
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading mappings: {str(e)}")

@app.get("/mappings/all")
async def get_all_mappings():
    """Get all cross-mappings across standards."""
    try:
        all_mappings = standards_loader.get_all_cross_mappings()
        return all_mappings
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading all mappings: {str(e)}")

# Error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return {"error": "Not found", "detail": str(exc.detail)}

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return {"error": "Internal server error", "detail": str(exc.detail)}

# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize API on startup."""
    print("Cyber Tonic API starting up...")
    print("Available endpoints:")
    print("- GET /standards - List all standards")
    print("- GET /standards/{id} - Get specific standard")
    print("- GET /clients - List all clients (requires auth)")
    print("- POST /clients - Create client (requires auth)")
    print("- POST /assessments - Create assessment (requires auth)")
    print("- POST /reports/generate - Generate report (requires auth)")
    print("See /docs for full API documentation")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
