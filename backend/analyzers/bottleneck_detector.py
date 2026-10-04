from typing import Dict, List, Any

class BottleneckDetector:
    """
    Identifies bottlenecks in the execution pipeline
    """
    
    def __init__(self):
        self.bottleneck_threshold_percent = 25  # Stage taking >25% of total time is a bottleneck
        self.cpu_utilization_threshold = 80     # CPU utilization >80% is high
        self.memory_threshold_mb = 500          # Memory usage >500MB is high
    
    def detect(self, cpu_results: Dict, dpu_results: Dict) -> Dict[str, Any]:
        """
        Detect bottlenecks by comparing CPU and DPU simulation results
        """
        bottlenecks = []
        
        # Analyze CPU baseline
        cpu_bottlenecks = self._analyze_cpu_bottlenecks(cpu_results)
        
        # Analyze stage-by-stage
        stage_bottlenecks = self._analyze_stage_bottlenecks(cpu_results, dpu_results)
        
        # Analyze resource utilization
        resource_bottlenecks = self._analyze_resource_bottlenecks(cpu_results)
        
        # Determine primary bottleneck
        primary_bottleneck = self._determine_primary_bottleneck(
            cpu_bottlenecks, stage_bottlenecks, resource_bottlenecks
        )
        
        # Calculate potential improvement
        potential_improvement = self._calculate_potential_improvement(
            cpu_results, dpu_results, stage_bottlenecks
        )
        
        return {
            "cpu_bottlenecks": cpu_bottlenecks,
            "stage_bottlenecks": stage_bottlenecks,
            "resource_bottlenecks": resource_bottlenecks,
            "primary_bottleneck": primary_bottleneck,
            "potential_improvement": potential_improvement,
            "recommendations": self._generate_recommendations(
                primary_bottleneck, stage_bottlenecks
            )
        }
    
    def _analyze_cpu_bottlenecks(self, cpu_results: Dict) -> List[Dict]:
        """
        Analyze CPU baseline for bottlenecks
        """
        bottlenecks = []
        stage_breakdown = cpu_results["stage_breakdown"]["stage_analysis"]
        
        for stage in stage_breakdown:
            if stage["percentage_of_total"] > self.bottleneck_threshold_percent:
                bottlenecks.append({
                    "type": "LATENCY",
                    "stage": stage["stage"],
                    "severity": "HIGH" if stage["percentage_of_total"] > 40 else "MEDIUM",
                    "percentage": stage["percentage_of_total"],
                    "latency_ms": stage["latency_ms"],
                    "description": f"{stage['stage']} is consuming {stage['percentage_of_total']}% of total execution time"
                })
        
        return bottlenecks
    
    def _analyze_stage_bottlenecks(self, cpu_results: Dict, dpu_results: Dict) -> List[Dict]:
        """
        Analyze each stage for DPU acceleration potential
        """
        bottlenecks = []
        
        for stage_name, cpu_metrics in cpu_results["stages"].items():
            dpu_metrics = dpu_results["stages"].get(stage_name, {})
            
            if dpu_metrics:
                speedup = dpu_metrics.get("speedup_factor", 1.0)
                cpu_latency = cpu_metrics["latency_ms"]
                
                # If stage is slow and has good DPU potential
                if cpu_latency > 50 and speedup > 2.0:
                    bottlenecks.append({
                        "type": "ACCELERATION_OPPORTUNITY",
                        "stage": stage_name,
                        "current_latency_ms": cpu_latency,
                        "estimated_dpu_latency_ms": dpu_metrics["latency_ms"],
                        "speedup_potential": speedup,
                        "transfer_overhead_ms": dpu_metrics.get("transfer_time_ms", 0),
                        "net_benefit_ms": cpu_latency - dpu_metrics["latency_ms"],
                        "recommendation": "MOVE_TO_DPU" if speedup > 3.0 else "CONSIDER_DPU"
                    })
                elif cpu_latency > 100:
                    bottlenecks.append({
                        "type": "SLOW_STAGE",
                        "stage": stage_name,
                        "current_latency_ms": cpu_latency,
                        "recommendation": "CUSTOM_KERNEL_CANDIDATE",
                        "description": f"Stage is slow ({cpu_latency}ms) and may benefit from custom kernel optimization"
                    })
        
        return bottlenecks
    
    def _analyze_resource_bottlenecks(self, cpu_results: Dict) -> List[Dict]:
        """
        Analyze resource utilization bottlenecks
        """
        bottlenecks = []
        
        # Check CPU utilization
        avg_cpu = cpu_results["avg_cpu_utilization_percent"]
        if avg_cpu > self.cpu_utilization_threshold:
            bottlenecks.append({
                "type": "CPU_UTILIZATION",
                "severity": "HIGH",
                "current_utilization": avg_cpu,
                "threshold": self.cpu_utilization_threshold,
                "description": f"High CPU utilization ({avg_cpu}%) indicates CPU-bound workload"
            })
        
        # Check memory usage
        peak_memory = cpu_results["peak_memory_mb"]
        if peak_memory > self.memory_threshold_mb:
            bottlenecks.append({
                "type": "MEMORY",
                "severity": "MEDIUM",
                "current_usage_mb": peak_memory,
                "threshold_mb": self.memory_threshold_mb,
                "description": f"High memory usage ({peak_memory}MB) may cause swapping"
            })
        
        return bottlenecks
    
    def _determine_primary_bottleneck(self, cpu_bottlenecks: List, 
                                       stage_bottlenecks: List,
                                       resource_bottlenecks: List) -> Dict:
        """
        Determine the primary bottleneck affecting performance
        """
        # Priority: latency bottlenecks > acceleration opportunities > resource issues
        if cpu_bottlenecks:
            primary = cpu_bottlenecks[0]
            return {
                "type": primary["type"],
                "stage": primary["stage"],
                "description": primary["description"],
                "impact": "HIGH"
            }
        
        if stage_bottlenecks:
            primary = stage_bottlenecks[0]
            return {
                "type": primary["type"],
                "stage": primary["stage"],
                "description": f"Best acceleration opportunity in {primary['stage']}",
                "impact": "HIGH"
            }
        
        if resource_bottlenecks:
            primary = resource_bottlenecks[0]
            return {
                "type": primary["type"],
                "description": primary["description"],
                "impact": "MEDIUM"
            }
        
        return {
            "type": "NONE",
            "description": "No significant bottlenecks detected",
            "impact": "LOW"
        }
    
    def _calculate_potential_improvement(self, cpu_results: Dict, 
                                         dpu_results: Dict,
                                         stage_bottlenecks: List) -> Dict:
        """
        Calculate potential performance improvement with optimization
        """
        cpu_total = cpu_results["total_latency_ms"]
        dpu_total = dpu_results["total_latency_ms"]
        
        current_speedup = dpu_results.get("overall_speedup", 1.0)
        
        # Calculate best-case if we optimize all recommended stages
        total_benefit = sum(b["net_benefit_ms"] for b in stage_bottlenecks 
                           if b.get("net_benefit_ms", 0) > 0)
        
        estimated_optimized_latency = cpu_total - total_benefit
        estimated_speedup = cpu_total / estimated_optimized_latency if estimated_optimized_latency > 0 else 1.0
        
        return {
            "current_speedup_with_full_dpu": current_speedup,
            "estimated_optimized_latency_ms": round(estimated_optimized_latency, 2),
            "estimated_speedup": round(estimated_speedup, 2),
            "improvement_percentage": round((1 - estimated_optimized_latency / cpu_total) * 100, 2)
        }
    
    def _generate_recommendations(self, primary_bottleneck: Dict, 
                                  stage_bottlenecks: List) -> List[str]:
        """
        Generate actionable recommendations
        """
        recommendations = []
        
        if primary_bottleneck["type"] != "NONE":
            recommendations.append(
                f"Primary bottleneck: {primary_bottleneck['description']}"
            )
        
        for bottleneck in stage_bottlenecks:
            if bottleneck["recommendation"] == "MOVE_TO_DPU":
                recommendations.append(
                    f"Move {bottleneck['stage']} to DPU for {bottleneck['speedup_potential']}x speedup"
                )
            elif bottleneck["recommendation"] == "CUSTOM_KERNEL_CANDIDATE":
                recommendations.append(
                    f"Develop custom kernel for {bottleneck['stage']} to optimize performance"
                )
        
        if not recommendations:
            recommendations.append("Workload is well-optimized. Consider model architecture changes for further gains.")
        
        return recommendations
