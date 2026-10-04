from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from engines.cpu_baseline import CPUBaselineEngine
from engines.dpu_simulation import DPUSimulationEngine
from analyzers.bottleneck_detector import BottleneckDetector
from decision_engine.operation_placer import OperationPlacer
from benchmarking.comparator import PerformanceComparator
from utils.metrics import MetricsCollector
from utils.report_generator import ReportGenerator
from fastapi.responses import PlainTextResponse

app = FastAPI(
    title="DPU Performance Studio API",
    description="Audio-AI Workload Optimization Platform",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize engines
cpu_engine = CPUBaselineEngine()
dpu_engine = DPUSimulationEngine()
bottleneck_detector = BottleneckDetector()
operation_placer = OperationPlacer()
comparator = PerformanceComparator()
metrics_collector = MetricsCollector()
report_generator = ReportGenerator()

@app.get("/")
async def root():
    return {
        "message": "DPU Performance Studio API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/api/analyze")
async def analyze_workload(audio_file: UploadFile = File(...)):
    """
    Main endpoint to analyze audio-AI workload and generate optimization recommendations
    """
    try:
        # Save uploaded file
        temp_path = f"temp_{audio_file.filename}"
        with open(temp_path, "wb") as buffer:
            content = await audio_file.read()
            buffer.write(content)
        
        # Step 1: Run CPU baseline
        cpu_results = await cpu_engine.run_baseline(temp_path)
        
        # Step 2: Run DPU simulation
        dpu_results = await dpu_engine.simulate_execution(temp_path, cpu_results)
        
        # Step 3: Detect bottlenecks
        bottlenecks = bottleneck_detector.detect(cpu_results, dpu_results)
        
        # Step 4: Determine optimal operation placement
        placement_decision = operation_placer.decide_placement(cpu_results, dpu_results, bottlenecks)
        
        # Step 5: Run optimized configuration
        optimized_results = await dpu_engine.run_optimized(temp_path, placement_decision)
        
        # Step 6: Compare performance
        comparison = comparator.compare(cpu_results, optimized_results, placement_decision)
        
        # Cleanup
        if os.path.exists(temp_path):
            os.remove(temp_path)
        
        return {
            "cpu_baseline": cpu_results,
            "dpu_simulation": dpu_results,
            "bottlenecks": bottlenecks,
            "placement_decision": placement_decision,
            "optimized_results": optimized_results,
            "comparison": comparison
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/cpu-baseline")
async def run_cpu_baseline(audio_file: UploadFile = File(...)):
    """Run CPU baseline measurement only"""
    try:
        temp_path = f"temp_{audio_file.filename}"
        with open(temp_path, "wb") as buffer:
            content = await audio_file.read()
            buffer.write(content)
        
        results = await cpu_engine.run_baseline(temp_path)
        
        if os.path.exists(temp_path):
            os.remove(temp_path)
        
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/dpu-simulate")
async def run_dpu_simulation(audio_file: UploadFile = File(...)):
    """Run DPU simulation only"""
    try:
        temp_path = f"temp_{audio_file.filename}"
        with open(temp_path, "wb") as buffer:
            content = await audio_file.read()
            buffer.write(content)
        
        cpu_results = await cpu_engine.run_baseline(temp_path)
        dpu_results = await dpu_engine.simulate_execution(temp_path, cpu_results)
        
        if os.path.exists(temp_path):
            os.remove(temp_path)
        
        return {
            "cpu_baseline": cpu_results,
            "dpu_simulation": dpu_results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/models")
async def get_available_models():
    """Get list of available AI models"""
    return {
        "models": [
            {"id": "whisper-tiny", "name": "Whisper Tiny", "type": "speech-to-text"},
            {"id": "whisper-base", "name": "Whisper Base", "type": "speech-to-text"},
            {"id": "wav2vec2", "name": "Wav2Vec2", "type": "speech-recognition"},
            {"id": "custom-model", "name": "Custom Model", "type": "custom"}
        ]
    }

@app.post("/api/report/markdown")
async def generate_markdown_report(analysis_results: dict):
    """Generate markdown report from analysis results"""
    try:
        report = report_generator.generate_report(analysis_results)
        return PlainTextResponse(content=report, media_type="text/markdown")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/report/json")
async def generate_json_report(analysis_results: dict):
    """Generate JSON report from analysis results"""
    try:
        report = report_generator.generate_json_report(analysis_results)
        return JSONResponse(content=report)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
