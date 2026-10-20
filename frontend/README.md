# HydroSight React Frontend

This package is a React + Vite + TypeScript replacement for the Streamlit presentation layer.

## Install and run

```powershell
cd frontend
npm install
npm run dev
```

Open the Vite address, normally `http://localhost:5173`.

## Data mode

The UI starts immediately with fallback demonstration data. It is API-ready and tries:

`GET /api/dashboard`

The Vite development proxy sends `/api` requests to:

`http://127.0.0.1:8000`

Keep the existing Python `data/`, `models/`, `reports/`, and `src/groundwater_risk/` folders in the project root. Do not move them into the React frontend.
