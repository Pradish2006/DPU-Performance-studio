# DPU Performance Studio - API Documentation

## Base URL
```
http://localhost:8000
```

## Overview

The DPU Performance Studio API provides endpoints for analyzing audio-AI workloads, measuring performance, detecting bottlenecks, and generating optimization recommendations.

## Authentication
Currently, no authentication is required. This is a development setup.

## Endpoints

### 1. Health Check

#### GET /health
Check if the API is running.

**Response:**
```json
{
  "status": "healthy"
}
```

---

### 2. API Status

#### GET /
Get API information.

**Response:**
```json
{
  "message": "DPU Performance Studio API",
  "version": "1.0.0",
  "status": "running"
}
```

---

### 3. Complete Workload Analysis

#### POST /api/analyze
Run complete analysis on an audio file including CPU baseline, DPU simulation, bottleneck detection, operation placement, and performance comparison.

**Request:**
- Content-Type: `multipart/form-data`
- Body: `audio_file` (file) - Audio file to analyze (WAV, MP3, FLAC, etc.)

**Response:**
```json
{
  "cpu_baseline": {
    "execution_path": "CPU_ONLY",
    "total_latency_ms": 550.0,
    "throughput_samples_per_sec": 1.82,
    "avg_cpu_utilization_percent": 75.5,
    "peak_memory_mb": 512.0,
    "stages": {
      "audio_preprocessing": {
        "latency_ms": 50.0,
        "cpu_utilization_percent": 45.0,
        "memory_mb": 50.0,
        "throughput_ops_per_sec": 20.0
      },
      "feature_extraction": {
        "latency_ms": 100.0,
        "cpu_utilization_percent": 65.0,
        "memory_mb": 120.0,
        "throughput_ops_per_sec": 10.0
      },
      "model_inference": {
        "latency_ms": 300.0,
        "cpu_utilization_percent": 85.0,
        "memory_mb": 300.0,
        "throughput_ops_per_sec": 3.33
      },
      "post_processing": {
        "latency_ms": 80.0,
        "cpu_utilization_percent": 70.0,
        "memory_mb": 80.0,
        "throughput_ops_per_sec": 12.5
      },
      "output_generation": {
        "latency_ms": 20.0,
        "cpu_utilization_percent": 40.0,
        "memory_mb": 20.0,
        "throughput_ops_per_sec": 50.0
      }
    },
    "stage_breakdown": {
      "total_stage_time_ms": 550.0,
      "stage_analysis": [...],
      "primary_bottleneck": "model_inference"
    },
    "timestamp": 1234567890.0
  },
  "dpu_simulation": {
    "execution_path": "CPU_DPU_SIMULATED",
    "total_latency_ms": 180.0,
    "cpu_baseline_latency_ms": 550.0,
    "overall_speedup": 3.06,
    "throughput_samples_per_sec": 5.56,
    "total_transfer_time_ms": 25.0,
    "total_sync_time_ms": 10.0,
    "total_fallback_time_ms": 0,
    "stages": {
      "audio_preprocessing": {
        "latency_ms": 38.33,
        "cpu_latency_ms": 50.0,
        "speedup_factor": 1.3,
        "dpu_utilization_percent": 85.0,
        "transfer_time_ms": 5.0,
        "sync_time_ms": 2.0,
        "execution_location": "DPU_SIMULATED",
        "confidence": 0.9
      },
      ...
    },
    "simulation_note": "These are SIMULATED DPU results. Real DPU measurements require hardware.",
    "timestamp": 1234567890.5
  },
  "bottlenecks": {
    "cpu_bottlenecks": [
      {
        "type": "LATENCY",
        "stage": "model_inference",
        "severity": "HIGH",
        "percentage": 54.55,
        "latency_ms": 300.0,
        "description": "model_inference is consuming 54.55% of total execution time"
      }
    ],
    "stage_bottlenecks": [
      {
        "type": "ACCELERATION_OPPORTUNITY",
        "stage": "model_inference",
        "current_latency_ms": 300.0,
        "estimated_dpu_latency_ms": 65.0,
        "speedup_potential": 4.62,
        "transfer_overhead_ms": 5.0,
        "net_benefit_ms": 235.0,
        "recommendation": "MOVE_TO_DPU"
      }
    ],
    "resource_bottlenecks": [],
    "primary_bottleneck": {
      "type": "LATENCY",
      "stage": "model_inference",
      "description": "model_inference is consuming 54.55% of total execution time",
      "impact": "HIGH"
    },
    "potential_improvement": {
      "current_speedup_with_full_dpu": 3.06,
      "estimated_optimized_latency_ms": 180.0,
      "estimated_speedup": 3.06,
      "improvement_percentage": 67.27
    },
    "recommendations": [
      "Primary bottleneck: model_inference is consuming 54.55% of total execution time",
      "Move model_inference to DPU for 4.62x speedup"
    ]
  },
  "placement_decision": {
    "placements": {
      "audio_preprocessing": {
        "location": "CPU",
        "reason": "Stage too fast (50.0ms < 30.0ms threshold)",
        "estimated_cpu_latency_ms": 50.0,
        "estimated_dpu_latency_ms": 38.33,
        "confidence": 0.95
      },
      "feature_extraction": {
        "location": "DPU",
        "reason": "Good speedup potential (3.0x)",
        "estimated_cpu_latency_ms": 100.0,
        "estimated_dpu_latency_ms": 38.33,
        "confidence": 0.85
      },
      "model_inference": {
        "location": "DPU",
        "reason": "Excellent speedup potential (4.62x)",
        "estimated_cpu_latency_ms": 300.0,
        "estimated_dpu_latency_ms": 65.0,
        "confidence": 0.90
      },
      "post_processing": {
        "location": "DPU",
        "reason": "Good speedup potential (2.0x)",
        "estimated_cpu_latency_ms": 80.0,
        "estimated_dpu_latency_ms": 42.0,
        "confidence": 0.85
      },
      "output_generation": {
        "location": "CPU",
        "reason": "Stage too fast (20.0ms < 30.0ms threshold)",
        "estimated_cpu_latency_ms": 20.0,
        "estimated_dpu_latency_ms": 18.33,
        "confidence": 0.95
      }
    },
    "summary": {
      "total_stages": 5,
      "cpu_stages": 2,
      "dpu_stages": 3,
      "custom_kernel_stages": 0,
      "distribution": {
        "cpu_percent": 40.0,
        "dpu_percent": 60.0,
        "custom_percent": 0.0
      },
      "estimated_total_latency_ms": 185.33,
      "estimated_speedup": 2.97,
      "improvement_percentage": 66.31
    },
    "decision_logic": [...]
  },
  "optimized_results": {
    "execution_path": "OPTIMIZED_MIXED",
    "total_latency_ms": 185.33,
    "throughput_samples_per_sec": 5.4,
    "total_transfer_time_ms": 15.0,
    "total_sync_time_ms": 6.0,
    "total_fallback_time_ms": 0,
    "stages": {...},
    "placement_used": {...},
    "timestamp": 1234567891.0
  },
  "comparison": {
    "summary": {
      "baseline_latency_ms": 550.0,
      "optimized_latency_ms": 185.33,
      "speedup": 2.97,
      "improvement_percentage": 66.31,
      "latency_reduction_ms": 364.67
    },
    "stage_comparisons": [...],
    "resource_comparison": {
      "cpu_utilization": {
        "baseline": 75.5,
        "optimized": 35.0,
        "change": -40.5,
        "change_percentage": -53.64
      },
      "dpu_utilization": {
        "baseline": 0,
        "optimized": 70.0,
        "change": 70.0
      },
      "memory_usage": {
        "baseline_mb": 512.0,
        "optimized_mb": 512.0,
        "change_mb": 0
      }
    },
    "slow_stages_analysis": [...],
    "changes_made": [...],
    "assessment": {
      "verdict": "EXCELLENT",
      "message": "Significant performance improvement (2.97x speedup)",
      "num_changes": 3,
      "performance_improved": true
    },
    "recommendations": [
      "Optimization strategy is highly effective. Proceed with implementation."
    ]
  }
}
```

**Error Response:**
```json
{
  "detail": "Error message"
}
```

---

### 4. CPU Baseline Only

#### POST /api/cpu-baseline
Run CPU baseline measurement only.

**Request:**
- Content-Type: `multipart/form-data`
- Body: `audio_file` (file) - Audio file to analyze

**Response:**
```json
{
  "execution_path": "CPU_ONLY",
  "total_latency_ms": 550.0,
  "throughput_samples_per_sec": 1.82,
  "avg_cpu_utilization_percent": 75.5,
  "peak_memory_mb": 512.0,
  "stages": {...},
  "stage_breakdown": {...},
  "timestamp": 1234567890.0
}
```

---

### 5. DPU Simulation Only

#### POST /api/dpu-simulate
Run DPU simulation only (includes CPU baseline for comparison).

**Request:**
- Content-Type: `multipart/form-data`
- Body: `audio_file` (file) - Audio file to analyze

**Response:**
```json
{
  "cpu_baseline": {...},
  "dpu_simulation": {...}
}
```

---

### 6. Available Models

#### GET /api/models
Get list of available AI models.

**Response:**
```json
{
  "models": [
    {
      "id": "whisper-tiny",
      "name": "Whisper Tiny",
      "type": "speech-to-text"
    },
    {
      "id": "whisper-base",
      "name": "Whisper Base",
      "type": "speech-to-text"
    },
    {
      "id": "wav2vec2",
      "name": "Wav2Vec2",
      "type": "speech-recognition"
    },
    {
      "id": "custom-model",
      "name": "Custom Model",
      "type": "custom"
    }
  ]
}
```

---

### 7. Generate Markdown Report

#### POST /api/report/markdown
Generate a Markdown report from analysis results.

**Request:**
- Content-Type: `application/json`
- Body: Analysis results object (same as /api/analyze response)

**Response:**
- Content-Type: `text/markdown`
- Body: Markdown formatted report

---

### 8. Generate JSON Report

#### POST /api/report/json
Generate a JSON report from analysis results.

**Request:**
- Content-Type: `application/json`
- Body: Analysis results object (same as /api/analyze response)

**Response:**
```json
{
  "metadata": {
    "generated_at": "2024-01-01T12:00:00",
    "tool": "DPU Performance Studio",
    "version": "1.0.0"
  },
  "summary": {
    "cpu_baseline_latency_ms": 550.0,
    "optimized_latency_ms": 185.33,
    "speedup": 2.97,
    "improvement_percentage": 66.31,
    "assessment": "EXCELLENT"
  },
  "detailed_results": {...}
}
```

---

## Error Handling

All endpoints may return the following error responses:

### 400 Bad Request
```json
{
  "detail": "Invalid request"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Error message describing what went wrong"
}
```

---

## Data Source Notice

The API returns data from three sources with different confidence levels:

1. **CPU Results**: Actual measured values from CPU baseline execution (High confidence)
2. **DPU Results**: Simulated/emulated values. Real DPU measurements require hardware (Medium confidence)
3. **Custom Kernel**: Future real-DPU implementation. Performance is estimated (Lower confidence)

---

## Rate Limiting

Currently, no rate limiting is implemented. This is a development setup.

---

## CORS

The API allows cross-origin requests from all origins (`*`). This is configured for development purposes.

---

## Interactive API Documentation

When the backend is running, visit:
```
http://localhost:8000/docs
```

This provides an interactive Swagger UI where you can test all endpoints.
