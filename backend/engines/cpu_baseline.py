import time
import psutil
import numpy as np
from typing import Dict, List, Any
import asyncio

class CPUBaselineEngine:
    """Runs audio-AI workload on CPU baseline and measures performance"""
    
    def __init__(self):
        self.stages = [
            "audio_preprocessing",
            "feature_extraction",
            "model_inference",
            "post_processing",
            "output_generation"
        ]
    
    async def run_baseline(self, audio_path: str) -> Dict[str, Any]:
        """
        Run the complete audio-AI workload on CPU and measure all metrics
        """
        start_time = time.time()
        
        # Collect initial CPU metrics
        cpu_before = psutil.cpu_percent(interval=0.1)
        memory_before = psutil.virtual_memory()
        
        # Execute each stage and measure
        stage_results = {}
        total_latency = 0
        
        for stage in self.stages:
            stage_start = time.time()
            cpu_start = psutil.cpu_percent(interval=0.01)
            
            # Simulate stage execution (in real implementation, this would run actual AI model)
            stage_result = await self._execute_stage(stage, audio_path)
            
            stage_end = time.time()
            stage_cpu = psutil.cpu_percent(interval=0.01)
            memory_after = psutil.virtual_memory()
            
            stage_latency = stage_end - stage_start
            stage_cpu_util = (cpu_start + stage_cpu) / 2
            
            stage_results[stage] = {
                "latency_ms": round(stage_latency * 1000, 2),
                "cpu_utilization_percent": round(stage_cpu_util, 2),
                "memory_mb": round((memory_after.used - memory_before.used) / (1024 * 1024), 2),
                "throughput_ops_per_sec": round(1 / stage_latency if stage_latency > 0 else 0, 2),
                "details": stage_result
            }
            
            total_latency += stage_latency
            memory_before = memory_after
        
        total_end = time.time()
        total_cpu = psutil.cpu_percent(interval=0.1)
        
        # Calculate aggregate metrics
        results = {
            "execution_path": "CPU_ONLY",
            "total_latency_ms": round(total_latency * 1000, 2),
            "throughput_samples_per_sec": round(1 / total_latency if total_latency > 0 else 0, 2),
            "avg_cpu_utilization_percent": round(total_cpu, 2),
            "peak_memory_mb": round(psutil.virtual_memory().used / (1024 * 1024), 2),
            "stages": stage_results,
            "stage_breakdown": self._analyze_stage_breakdown(stage_results),
            "timestamp": time.time()
        }
        
        return results
    
    async def _execute_stage(self, stage: str, audio_path: str) -> Dict[str, Any]:
        """
        Execute a single stage of the pipeline
        In real implementation, this would run actual AI operations
        """
        # Simulate different workloads for different stages
        if stage == "audio_preprocessing":
            # Simulate audio loading and preprocessing
            await asyncio.sleep(0.05)
            return {
                "operations": ["load_audio", "resample", "normalize"],
                "input_shape": "(16000,)",
                "output_shape": "(16000,)"
            }
        
        elif stage == "feature_extraction":
            # Simulate feature extraction (MFCC, spectrogram, etc.)
            await asyncio.sleep(0.1)
            return {
                "operations": ["mfcc_extraction", "spectrogram"],
                "feature_dim": 80,
                "num_frames": 100
            }
        
        elif stage == "model_inference":
            # Simulate model inference (most intensive)
            await asyncio.sleep(0.3)
            return {
                "operations": ["encoder_forward", "decoder_forward"],
                "model_layers": 12,
                "parameters": "74M"
            }
        
        elif stage == "post_processing":
            # Simulate post-processing
            await asyncio.sleep(0.08)
            return {
                "operations": ["beam_search", "language_model"],
                "vocabulary_size": 51865
            }
        
        elif stage == "output_generation":
            # Simulate output generation
            await asyncio.sleep(0.02)
            return {
                "operations": ["format_output", "timestamp_alignment"],
                "output_length": 150
            }
        
        return {}
    
    def _analyze_stage_breakdown(self, stage_results: Dict) -> Dict[str, Any]:
        """
        Analyze which stages are taking the most time
        """
        total_time = sum(s["latency_ms"] for s in stage_results.values())
        
        breakdown = []
        for stage_name, metrics in stage_results.items():
            percentage = (metrics["latency_ms"] / total_time * 100) if total_time > 0 else 0
            breakdown.append({
                "stage": stage_name,
                "latency_ms": metrics["latency_ms"],
                "percentage_of_total": round(percentage, 2),
                "is_bottleneck": percentage > 30  # Stage taking >30% is potential bottleneck
            })
        
        # Sort by latency descending
        breakdown.sort(key=lambda x: x["latency_ms"], reverse=True)
        
        return {
            "total_stage_time_ms": round(total_time, 2),
            "stage_analysis": breakdown,
            "primary_bottleneck": breakdown[0]["stage"] if breakdown else None
        }
