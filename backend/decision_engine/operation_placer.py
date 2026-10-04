from typing import Dict, List, Any

class OperationPlacer:
    """
    Intelligently decides where each operation should run:
    - CPU: for small, fast operations where DPU overhead isn't worth it
    - DPU: for compute-intensive operations that benefit from acceleration
    - Custom Kernel: for operations that need specialized optimization (future real-DPU)
    """
    
    def __init__(self):
        self.dpu_benefit_threshold_ms = 30      # Stage must be >30ms to consider DPU
        self.speedup_threshold = 2.0           # Need >2x speedup to justify DPU
        self.transfer_overhead_tolerance = 0.3 # Transfer overhead should be <30% of stage time
    
    def decide_placement(self, cpu_results: Dict, dpu_results: Dict, 
                         bottlenecks: Dict) -> Dict[str, Any]:
        """
        Decide optimal placement for each operation based on analysis
        """
        placements = {}
        stage_bottlenecks = bottlenecks.get("stage_bottlenecks", [])
        
        # Build a map of stage to bottleneck info
        bottleneck_map = {b["stage"]: b for b in stage_bottlenecks}
        
        for stage_name, cpu_metrics in cpu_results["stages"].items():
            dpu_metrics = dpu_results["stages"].get(stage_name, {})
            bottleneck_info = bottleneck_map.get(stage_name)
            
            placement = self._decide_single_placement(
                stage_name, cpu_metrics, dpu_metrics, bottleneck_info
            )
            placements[stage_name] = placement
        
        # Calculate overall configuration summary
        summary = self._calculate_summary(placements, cpu_results, dpu_results)
        
        return {
            "placements": placements,
            "summary": summary,
            "decision_logic": self._explain_decision_logic(placements, stage_bottlenecks)
        }
    
    def _decide_single_placement(self, stage_name: str, cpu_metrics: Dict,
                                  dpu_metrics: Dict, bottleneck_info: Dict) -> Dict:
        """
        Decide placement for a single stage
        """
        cpu_latency = cpu_metrics["latency_ms"]
        
        # If no DPU metrics available, default to CPU
        if not dpu_metrics:
            return {
                "location": "CPU",
                "reason": "No DPU simulation available",
                "estimated_cpu_latency_ms": cpu_latency,
                "estimated_dpu_latency_ms": cpu_latency,
                "confidence": 0.90
            }
        
        dpu_latency = dpu_metrics["latency_ms"]
        speedup = dpu_metrics.get("speedup_factor", 1.0)
        transfer_time = dpu_metrics.get("transfer_time_ms", 0)
        
        # Decision logic
        if cpu_latency < self.dpu_benefit_threshold_ms:
            # Stage is too fast - DPU overhead not worth it
            return {
                "location": "CPU",
                "reason": f"Stage too fast ({cpu_latency}ms < {self.dpu_benefit_threshold_ms}ms threshold)",
                "estimated_cpu_latency_ms": cpu_latency,
                "estimated_dpu_latency_ms": dpu_latency,
                "confidence": 0.95
            }
        
        if speedup < self.speedup_threshold:
            # Not enough speedup to justify DPU
            return {
                "location": "CPU",
                "reason": f"Speedup ({speedup}x) below threshold ({self.speedup_threshold}x)",
                "estimated_cpu_latency_ms": cpu_latency,
                "estimated_dpu_latency_ms": dpu_latency,
                "confidence": 0.90
            }
        
        # Check if transfer overhead is too high relative to benefit
        if transfer_time > (cpu_latency * self.transfer_overhead_tolerance):
            # Transfer overhead too high
            if cpu_latency > 100 and bottleneck_info and bottleneck_info.get("recommendation") == "CUSTOM_KERNEL_CANDIDATE":
                # Large stage with high overhead - candidate for custom kernel
                return {
                    "location": "CUSTOM_KERNEL",
                    "reason": "High transfer overhead + large workload = custom kernel candidate",
                    "estimated_cpu_latency_ms": cpu_latency,
                    "estimated_dpu_latency_ms": dpu_latency,
                    "estimated_custom_latency_ms": cpu_latency / 4.0,  # Estimate 4x improvement
                    "confidence": 0.70,
                    "note": "Requires real DPU hardware for implementation"
                }
            else:
                return {
                    "location": "CPU",
                    "reason": f"Transfer overhead ({transfer_time}ms) too high relative to benefit",
                    "estimated_cpu_latency_ms": cpu_latency,
                    "estimated_dpu_latency_ms": dpu_latency,
                    "confidence": 0.85
                }
        
        # Good candidate for DPU
        if speedup > 4.0:
            # Excellent speedup - definitely move to DPU
            return {
                "location": "DPU",
                "reason": f"Excellent speedup potential ({speedup}x)",
                "estimated_cpu_latency_ms": cpu_latency,
                "estimated_dpu_latency_ms": dpu_latency,
                "confidence": 0.90
            }
        else:
            # Moderate speedup - move to DPU
            return {
                "location": "DPU",
                "reason": f"Good speedup potential ({speedup}x)",
                "estimated_cpu_latency_ms": cpu_latency,
                "estimated_dpu_latency_ms": dpu_latency,
                "confidence": 0.85
            }
    
    def _calculate_summary(self, placements: Dict, cpu_results: Dict, 
                           dpu_results: Dict) -> Dict:
        """
        Calculate summary of placement decisions
        """
        cpu_count = sum(1 for p in placements.values() if p["location"] == "CPU")
        dpu_count = sum(1 for p in placements.values() if p["location"] == "DPU")
        custom_count = sum(1 for p in placements.values() if p["location"] == "CUSTOM_KERNEL")
        total = len(placements)
        
        # Calculate estimated latency with this placement
        estimated_latency = 0
        for stage_name, placement in placements.items():
            if placement["location"] == "CPU":
                estimated_latency += placement["estimated_cpu_latency_ms"]
            elif placement["location"] == "DPU":
                estimated_latency += placement["estimated_dpu_latency_ms"]
            elif placement["location"] == "CUSTOM_KERNEL":
                estimated_latency += placement.get("estimated_custom_latency_ms", 
                                                  placement["estimated_cpu_latency_ms"])
        
        cpu_baseline = cpu_results["total_latency_ms"]
        estimated_speedup = cpu_baseline / estimated_latency if estimated_latency > 0 else 1.0
        
        return {
            "total_stages": total,
            "cpu_stages": cpu_count,
            "dpu_stages": dpu_count,
            "custom_kernel_stages": custom_count,
            "distribution": {
                "cpu_percent": round(cpu_count / total * 100, 1),
                "dpu_percent": round(dpu_count / total * 100, 1),
                "custom_percent": round(custom_count / total * 100, 1)
            },
            "estimated_total_latency_ms": round(estimated_latency, 2),
            "estimated_speedup": round(estimated_speedup, 2),
            "improvement_percentage": round((1 - estimated_latency / cpu_baseline) * 100, 2)
        }
    
    def _explain_decision_logic(self, placements: Dict, 
                                 stage_bottlenecks: List) -> List[Dict]:
        """
        Explain the decision logic for each placement
        """
        explanations = []
        
        for stage_name, placement in placements.items():
            explanations.append({
                "stage": stage_name,
                "decision": placement["location"],
                "reason": placement["reason"],
                "confidence": placement["confidence"]
            })
        
        return explanations
