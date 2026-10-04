# DPU Performance Studio

A professional engineering platform for audio-AI workload optimization. The software automatically determines how AI workloads should be executed across CPU, DPU, or custom-kernel paths for better performance.

## Features

- **CPU Baseline Measurement**: Accurate measurement of audio-AI workload performance on CPU
- **DPU Simulation/Emulation**: Simulated DPU performance estimation (software-first approach)
- **Stage-by-Stage Profiling**: Detailed breakdown of execution stages to identify bottlenecks
- **Bottleneck Detection**: Intelligent analysis to find performance bottlenecks
- **Operation Placement Decision**: AI-driven recommendations for optimal operation placement
- **Performance Comparison**: Before/after benchmarking with detailed metrics
- **Professional Dashboard**: Navy-white themed user-friendly interface
- **Confidence Metrics**: Clear distinction between measured, simulated, and estimated results
- **Report Generation**: Export analysis results as Markdown or JSON reports

## Architecture

### Backend (FastAPI + Python)
- **CPU Baseline Engine**: Measures actual CPU performance
- **DPU Simulation Engine**: Simulates DPU acceleration with estimated performance
- **Bottleneck Detector**: Identifies performance bottlenecks
- **Operation Placer**: Decides optimal placement for each operation
- **Performance Comparator**: Compares baseline vs optimized performance
- **Report Generator**: Creates detailed analysis reports

### Frontend (React + Vite)
- **Upload Section**: Audio file upload interface
- **Results Panel**: Comprehensive performance dashboard
- **Metrics Comparison**: Visual comparison charts
- **Stage Breakdown**: Detailed stage-by-stage analysis
- **Bottleneck Analysis**: Bottleneck identification and recommendations
- **Placement Decisions**: Operation placement visualization
- **Confidence Bar**: Measurement confidence indicators

## Installation

### Option 1: Docker (Recommended)

#### Prerequisites
- Docker Engine 20.10+
- Docker Compose 2.0+

#### Quick Start
```bash
# Clone the repository
git clone <repository-url>
cd dpu-performance-studio

# Build and start all services
docker-compose up --build

# Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

#### Production Deployment
```bash
# Build and start production containers
docker-compose -f docker-compose.prod.yml up --build -d

# Access the application
# Frontend: http://localhost:80
# Backend API: http://localhost:8000
```

For detailed Docker documentation, see [docs/DOCKER_DOCUMENTATION.md](docs/DOCKER_DOCUMENTATION.md)

### Option 2: Local Development

#### Prerequisites
- Python 3.12+ (tested with 3.14)
- Node.js 16+
- npm or yarn
- Docker and Docker Compose (for Docker deployment)

#### Backend Setup
```bash
cd backend
pip install -r requirements.txt

# Windows
start.bat

# Linux/Mac
bash start.sh

# Or directly
python main.py
```

The backend will start on `http://localhost:8000`
API Documentation: `http://localhost:8000/docs`

**Note:** Keep the terminal open - the server runs until you press Ctrl+C

#### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

The frontend will start on `http://localhost:3000`

#### Run Both Services
```bash
# From project root
npm run install-all
npm run dev
```

## Usage

1. Open the application in your browser at `http://localhost:3000`
2. Upload an audio file (WAV, MP3, FLAC, etc.)
3. Click "Start Analysis" to begin the performance analysis
4. View the comprehensive results including:
   - Performance metrics comparison
   - Stage-by-stage execution analysis
   - Bottleneck identification
   - Operation placement recommendations
   - Confidence scores
5. Download reports in Markdown or JSON format

## Data Source Notice

This platform uses a **software-first approach**:

- **CPU Results**: Actual measured values from CPU baseline execution (High confidence)
- **DPU Results**: Simulated/emulated values. Real DPU measurements require hardware (Medium confidence)
- **Custom Kernel**: Future real-DPU implementation. Performance is estimated (Lower confidence)

Real DPU integration is planned for future releases.

## Technology Stack

### Backend
- FastAPI - Web framework
- Python 3.8+ - Programming language
- NumPy - Numerical computing
- PyTorch - Deep learning framework (for AI model execution)
- psutil - System metrics collection

### Frontend
- React 18 - UI framework
- Vite - Build tool
- Recharts - Data visualization
- Lucide React - Icons
- Axios - HTTP client

## Project Structure

```
dpu-performance-studio/
├── backend/
│   ├── engines/          # Execution engines
│   ├── analyzers/        # Performance analyzers
│   ├── decision_engine/  # Operation placement logic
│   ├── benchmarking/     # Performance comparison
│   ├── utils/           # Utilities (metrics, reports)
│   ├── Dockerfile       # Backend Docker configuration
│   └── main.py          # FastAPI application
├── frontend/
│   ├── src/
│   │   ├── components/  # React components
│   │   ├── App.jsx      # Main application
│   │   └── index.css    # Global styles
│   ├── Dockerfile       # Frontend Docker configuration
│   ├── nginx.conf       # Nginx configuration
│   └── package.json
├── docs/
│   ├── API_DOCUMENTATION.md      # API endpoint documentation
│   ├── FRONTEND_DOCUMENTATION.md # Frontend component documentation
│   └── DOCKER_DOCUMENTATION.md   # Docker deployment guide
├── docker-compose.yml            # Development Docker Compose
├── docker-compose.prod.yml       # Production Docker Compose
├── .dockerignore                # Docker ignore files
├── .gitignore
├── README.md
├── SETUP.md
└── PROJECT_SUMMARY.md
```

## Core Innovation

Unlike traditional accelerators that simply speed up models, DPU Performance Studio:

1. **Measures the entire pipeline** - Not just model inference, but preprocessing, feature extraction, and post-processing
2. **Finds the real bottleneck** - Stage-by-stage analysis identifies where time is actually spent
3. **Intelligently chooses placement** - Each operation is evaluated for CPU, DPU, or custom-kernel execution
4. **Proves the optimization** - Runs the recommended configuration and benchmarks against baseline
5. **Distinguishes data sources** - Clearly labels measured vs simulated vs estimated results

## Docker Support

The project includes full Docker support with:

- **Multi-container setup** with Docker Compose
- **Development configuration** with live code mounting
- **Production configuration** with optimized builds
- **Nginx reverse proxy** for frontend
- **Health checks** for service monitoring
- **Log rotation** for production

### Docker Commands

```bash
# Development
docker-compose up --build
docker-compose down

# Production
docker-compose -f docker-compose.prod.yml up --build -d
docker-compose -f docker-compose.prod.yml down

# View logs
docker-compose logs -f
docker-compose logs backend
docker-compose logs frontend

# Rebuild without cache
docker-compose build --no-cache
```

For detailed Docker documentation, see [docs/DOCKER_DOCUMENTATION.md](docs/DOCKER_DOCUMENTATION.md)

## License

MIT

## Future Roadmap

- [ ] Real DPU hardware integration
- [ ] Support for more AI models
- [ ] Custom kernel development tools
- [ ] Historical performance tracking
- [ ] Multi-workload batch analysis
- [ ] Cloud deployment options
