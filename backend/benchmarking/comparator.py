from typing import Dict, List, Any

class PerformanceComparator:
    """
    Compares baseline vs optimized performance and generates detailed reports
    """
    
    def compare(self, cpu_results: Dict, optimized_results: Dict, 
                placement_decision: Dict) -> Dict[str, Any]:
        """
        Compare CPU baseline against optimized configuration
        """
        baseline_latency = cpu_results["total_latency_ms"]
        optimized_latency = optimized_results["total_latency_ms"]
        
        speedup = baseline_latency / optimized_latency if optimized_latency > 0 else 1.0
        improvement = ((baseline_latency - optimized_latency) / baseline_latency * 100) if baseline_latency > 0 else 0
        
        # Compare each stage
        stage_comparisons = []
        for stage_name in cpu_results["stages"].keys():
            baseline_stage = cpu_results["stages"][stage_name]
            optimized_stage = optimized_results["stages"].get(stage_name, {})
            
            if optimized_stage:
                stage_comparison = {
                    "stage": stage_name,
                    "baseline_latency_ms": baseline_stage["latency_ms"],
                    "optimized_latency_ms": optimized_stage["latency_ms"],
                    "speedup": round(baseline_stage["latency_ms"] / optimized_stage["latency_ms"], 2) if optimized_stage["latency_ms"] > 0 else 1.0,
                    "improvement_ms": round(baseline_stage["latency_ms"] - optimized_stage["latency_ms"], 2),
                    "baseline_location": "CPU",
                    "optimized_location": optimized_stage.get("execution_location", "UNKNOWN"),
                    "changed": baseline_stage["latency_ms"] != optimized_stage["latency_ms"]
                }
                stage_comparisons.append(stage_comparison)
        
        # Analyze resource utilization changes
        resource_comparison = self._compare_resources(cpu_results, optimized_results)
        
        # Determine what was slow and why
        slow_stages = self._identify_slow_stages(cpu_results)
        
        # Determine what changed
        changes = self._identify_changes(cpu_results, optimized_results, placement_decision)
        
        # Overall assessment
        assessment = self._generate_assessment(speedup, improvement, changes)
        
        return {
            "summary": {
                "baseline_latency_ms": baseline_latency,
                "optimized_latency_ms": optimized_latency,
                "speedup": round(speedup, 2),
                "improvement_percentage": round(improvement, 2),
                "latency_reduction_ms": round(baseline_latency - optimized_latency, 2)
            },
            "stage_comparisons": stage_comparisons,
            "resource_comparison": resource_comparison,
            "slow_stages_analysis": slow_stages,
            "changes_made": changes,
            "assessment": assessment,
            "recommendations": self._generate_final_recommendations(assessment, changes)
        }
    
    def _compare_resources(self, cpu_results: Dict, optimized_results: Dict) -> Dict:
        """
        Compare resource utilization between baseline and optimized
        """
        baseline_cpu = cpu_results["avg_cpu_utilization_percent"]
        baseline_memory = cpu_results["peak_memory_mb"]
        
        # Calculate optimized CPU utilization (weighted by placement)
        optimized_cpu = 0
        optimized_dpu = 0
        total_stages = len(optimized_results["stages"])
        
        for stage_data in optimized_results["stages"].values():
            optimized_cpu += stage_data.get("cpu_utilization_percent", 0)
            optimized_dpu += stage_data.get("dpu_utilization_percent", 0)
        
        optimized_cpu = round(optimized_cpu / total_stages, 2) if total_stages > 0 else 0
        optimized_dpu = round(optimized_dpu / total_stages, 2) if total_stages > 0 else 0
        
        return {
            "cpu_utilization": {
                "baseline": baseline_cpu,
                "optimized": optimized_cpu,
                "change": round(optimized_cpu - baseline_cpu, 2),
                "change_percentage": round(((optimized_cpu - baseline_cpu) / baseline_cpu * 100) if baseline_cpu > 0 else 0, 2)
            },
            "dpu_utilization": {
                "baseline": 0,
                "optimized": optimized_dpu,
                "change": optimized_dpu
            },
            "memory_usage": {
                "baseline_mb": baseline_memory,
                "optimized_mb": baseline_memory,  # Assume similar for now
                "change_mb": 0
            }
        }
    
    def _identify_slow_stages(self, cpu_results: Dict) -> List[Dict]:
        """
        Identify which stages were slow in the baseline
        """
        stage_breakdown = cpu_results["stage_breakdown"]["stage_analysis"]
        slow_stages = []
        
        for stage in stage_breakdown:
            if stage["latency_ms"] > 50:  # >50ms is considered slow
                slow_stages.append({
                    "stage": stage["stage"],
                    "latency_ms": stage["latency_ms"],
                    "percentage_of_total": stage["percentage_of_total"],
                    "reason": self._explain_why_slow(stage["stage"], stage["latency_ms"])
                })
        
        return slow_stages
    
    def _explain_why_slow(self, stage: str, latency: float) -> str:
        """
        Explain why a stage might be slow
        """
        reasons = {
            "audio_preprocessing": "I/O bound - reading and processing audio data",
            "feature_extraction": "Compute intensive - extracting audio features",
            "model_inference": "Most compute intensive - running neural network layers",
            "post_processing": "Compute and memory intensive - beam search and LM",
            "output_generation": "Minimal overhead - formatting results"
        }
        return reasons.get(stage, "General computational overhead")
    
    def _identify_changes(self, cpu_results: Dict, optimized_results: Dict,
                          placement_decision: Dict) -> List[Dict]:
        """
        Identify what changed between baseline and optimized
        """
        changes = []
        
        for stage_name, placement in placement_decision["placements"].items():
            if placement["location"] != "CPU":
                baseline_location = "CPU"
                optimized_location = placement["location"]
                
                change = {
                    "stage": stage_name,
                    "change_type": "LOCATION_CHANGE",
                    "from": baseline_location,
                    "to": optimized_location,
                    "reason": placement["reason"],
                    "expected_benefit": f"{placement.get('estimated_speedup', 'N/A')}x speedup"
                }
                changes.append(change)
        
        return changes
    
    def _generate_assessment(self, speedup: float, improvement: float, 
                             changes: List) -> Dict:
        """
        Generate overall assessment of the optimization
        """
        if speedup > 2.0:
            verdict = "EXCELLENT"
            message = f"Significant performance improvement ({speedup}x speedup)"
        elif speedup > 1.5:
            verdict = "GOOD"
            message = f"Noticeable performance improvement ({speedup}x speedup)"
        elif speedup > 1.1:
            verdict = "MODERATE"
            message = f"Some performance improvement ({speedup}x speedup)"
        else:
            verdict = "MINIMAL"
            message = f"Minimal performance improvement ({speedup}x speedup)"
        
        return {
            "verdict": verdict,
            "message": message,
            "num_changes": len(changes),
            "performance_improved": speedup > 1.0
        }
    
    def _generate_final_recommendations(self, assessment: Dict, 
                                        changes: List) -> List[str]:
        """
        Generate final recommendations based on comparison
        """
        recommendations = []
        
        if assessment["verdict"] == "EXCELLENT":
            recommendations.append("Optimization strategy is highly effective. Proceed with implementation.")
        elif assessment["verdict"] == "GOOD":
            recommendations.append("Optimization shows good results. Consider fine-tuning for additional gains.")
        elif assessment["verdict"] == "MODERATE":
            recommendations.append("Moderate improvement. Review custom kernel candidates for better optimization.")
        else:
            recommendations.append("Minimal improvement detected. Reconsider operation placement strategy.")
        
        if len(changes) == 0:
            recommendations.append("No changes were made. The workload may already be optimized.")
        
        # Check for custom kernel stages
        custom_stages = [c for c in changes if c["to"] == "CUSTOM_KERNEL"]
        if custom_stages:
            recommendations.append(
                f"{len(custom_stages)} stage(s) marked for custom kernel optimization. "
                "This requires real DPU hardware implementation."
            )
        
        return recommendations
