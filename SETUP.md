# DPU Performance Studio - Setup Guide

## Quick Start

### 1. Install Backend Dependencies
```bash
cd backend
pip install -r requirements.txt
```

**Note**: The requirements.txt uses flexible version ranges (>=) to support Python 3.12-3.14. If you encounter any issues, you can also install individual packages:
```bash
pip install fastapi uvicorn[standard] pydantic numpy scipy psutil python-multipart aiofiles pyyaml jinja2
```

### 2. Install Frontend Dependencies
```bash
cd frontend
npm install
```

### 3. Start Backend Server

**Option 1: Using the batch script (Windows)**
```bash
cd backend
start.bat
```

**Option 2: Direct Python command**
```bash
cd backend
python main.py
```

**Option 3: Using uvicorn directly**
```bash
cd backend
uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

Backend will run on http://localhost:8000
API Documentation: http://localhost:8000/docs

**Note:** The server will keep running until you press Ctrl+C to stop it.

### 4. Start Frontend Development Server
```bash
cd frontend
npm run dev
```
Frontend will run on http://localhost:3000

### 5. Access the Application
Open your browser and navigate to: http://localhost:3000

## Testing the Application

1. Upload any audio file (WAV, MP3, FLAC, etc.)
2. Click "Start Analysis"
3. View the comprehensive performance dashboard
4. Download reports in Markdown or JSON format

## Project Structure

```
dpu-performance-studio/
├── backend/
│   ├── engines/
│   │   ├── cpu_baseline.py       # CPU measurement engine
│   │   └── dpu_simulation.py     # DPU simulation engine
│   ├── analyzers/
│   │   └── bottleneck_detector.py # Bottleneck detection
│   ├── decision_engine/
│   │   └── operation_placer.py  # Operation placement logic
│   ├── benchmarking/
│   │   └── comparator.py         # Performance comparison
│   ├── utils/
│   │   ├── metrics.py           # Metrics collection
│   │   └── report_generator.py  # Report generation
│   └── main.py                  # FastAPI application
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── UploadSection.jsx
│   │   │   ├── ResultsPanel.jsx
│   │   │   ├── MetricsComparison.jsx
│   │   │   ├── StageBreakdown.jsx
│   │   │   ├── BottleneckAnalysis.jsx
│   │   │   ├── PlacementDecisions.jsx
│   │   │   └── ConfidenceBar.jsx
│   │   ├── App.jsx
│   │   └── index.css
│   └── package.json
└── README.md
```

## API Endpoints

- `GET /` - API status
- `GET /health` - Health check
- `POST /api/analyze` - Complete workload analysis
- `POST /api/cpu-baseline` - CPU baseline only
- `POST /api/dpu-simulate` - DPU simulation only
- `GET /api/models` - Available AI models
- `POST /api/report/markdown` - Generate markdown report
- `POST /api/report/json` - Generate JSON report

## Theme Configuration

The application uses a professional navy-white theme:

- **Primary Navy**: #1a365d
- **Secondary Navy**: #2c5282
- **Dark Navy**: #0f1f3a
- **Light Navy**: #4a6fa5
- **White**: #ffffff
- **Accent Blue**: #3182ce
- **Accent Green**: #38a169
- **Accent Orange**: #dd6b20

## Key Features Implemented

✅ CPU Baseline Measurement Engine
✅ DPU Simulation/Emulation Engine
✅ Stage-by-Stage Execution Profiling
✅ Bottleneck Detection and Analysis
✅ Intelligent Operation Placement Decision Engine
✅ Performance Comparison and Benchmarking
✅ Professional Navy-White Themed Dashboard
✅ Confidence Bar and Metrics Visualization
✅ Report Generation (Markdown & JSON)
✅ User-Friendly Interface

## Data Source Disclaimer

This platform uses a software-first approach:
- CPU Results: Actual measured values (High confidence)
- DPU Results: Simulated/emulated values (Medium confidence)
- Custom Kernel: Future real-DPU estimates (Lower confidence)

Real DPU integration is planned for future releases.
