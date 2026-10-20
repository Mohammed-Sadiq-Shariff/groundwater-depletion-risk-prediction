from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response

from app.schemas.dashboard import HealthResponse
from app.services import data_service, report_service, import_service


app = FastAPI(
    title="HydroSight API 2.0",
    description="Real-Time Machine Learning Intelligence API for Mysore District Groundwater Depletion Risk",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health", response_model=HealthResponse)
def health():
    return {
        "status": "healthy",
        "message": "HydroSight Live Intelligence API is operational",
    }


@app.get("/api/dashboard/overview")
def dashboard_overview():
    return data_service.get_overview()


@app.get("/api/dashboard")
def dashboard():
    return {
        "overview": data_service.get_overview(),
        "stations": data_service.get_stations(),
        "predictions": data_service.get_predictions(),
        "risk_distribution": data_service.get_risk_distribution(),
        "features": data_service.get_features(),
        "map_summary": report_service.get_map_classification_summary(),
    }


@app.get("/api/stations")
def stations():
    return data_service.get_stations()


@app.get("/api/stations/{station_name}")
def station_details(station_name: str):
    result = data_service.get_station_details(station_name)
    if result is None:
        raise HTTPException(
            status_code=404,
            detail=f"Station not found: {station_name}",
        )
    return result


@app.get("/api/stations/{station_name}/history")
def station_history(station_name: str):
    history = data_service.get_station_history(station_name)
    if not history:
        raise HTTPException(
            status_code=404,
            detail=f"No history found for: {station_name}",
        )
    return history


@app.get("/api/blocks")
def blocks():
    return data_service.get_blocks()


@app.get("/api/predictions")
def predictions():
    return data_service.get_predictions()


@app.get("/api/predictions/latest")
def latest_predictions():
    preds = data_service.get_predictions()
    if not preds:
        raise HTTPException(
            status_code=404,
            detail="No predictions available",
        )
    return preds


@app.get("/api/analytics/risk-distribution")
def risk_distribution():
    return data_service.get_risk_distribution()


@app.get("/api/analytics/features")
def features():
    return data_service.get_features()


# =========================================================================
# BOUNDARY & GIS ENDPOINTS
# =========================================================================

@app.get("/api/boundaries/taluks")
def taluk_boundaries():
    """Return real OpenStreetMap GeoJSON polygon boundaries for all Mysuru taluks."""
    return report_service.get_taluk_boundaries()


@app.get("/api/boundaries/district")
def district_boundary():
    """Return real OpenStreetMap GeoJSON polygon boundary for Mysuru District."""
    return report_service.get_district_boundary()


# =========================================================================
# IMPORT & TEMPLATE EXCEL ENDPOINTS
# =========================================================================

@app.get("/api/data/template")
def download_template_excel():
    """Download the official template Excel file matching project schema."""
    excel_bytes = report_service.generate_template_excel()
    return Response(
        content=excel_bytes,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": "attachment; filename=mysore_groundwater_import_template.xlsx"
        }
    )


@app.post("/api/data/upload")
async def upload_and_predict(file: UploadFile = File(...)):
    """
    Upload a new Excel (.xlsx) or CSV dataset, validate columns,
    and execute real-time model inference for all monitoring wells.
    """
    try:
        contents = await file.read()
        res = import_service.process_uploaded_file(contents, file.filename or "uploaded_data.xlsx")
        return res
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# =========================================================================
# REPORT EXPORT ENDPOINTS
# =========================================================================

@app.get("/api/reports/excel")
def download_comprehensive_report():
    """Download the executive multi-sheet Excel intelligence report."""
    excel_bytes = report_service.generate_comprehensive_excel_report()
    return Response(
        content=excel_bytes,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": "attachment; filename=mysore_groundwater_intelligence_report.xlsx"
        }
    )


@app.get("/api/reports/map")
def get_map_classification_report():
    """Return map classification payload with real-time taluk colors and summary."""
    return report_service.get_map_classification_summary()
