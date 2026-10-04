import time
import psutil
from typing import Dict, List, Any

class MetricsCollector:
    """
    Collects and aggregates performance metrics
    """
    
    def __init__(self):
        self.metrics_history = []
    
    def start_measurement(self) -> Dict[str, Any]:
        """
        Start a new measurement session
        """
        return {
            "start_time": time.time(),
            "cpu_before": psutil.cpu_percent(interval=0.1),
            "memory_before": psutil.virtual_memory(),
            "disk_io_before": psutil.disk_io_counters()
        }
    
    def end_measurement(self, start_data: Dict) -> Dict[str, Any]:
        """
        End measurement and calculate deltas
        """
        end_time = time.time()
        cpu_after = psutil.cpu_percent(interval=0.1)
        memory_after = psutil.virtual_memory()
        disk_io_after = psutil.disk_io_counters()
        
        duration = end_time - start_data["start_time"]
        
        return {
            "duration_seconds": round(duration, 4),
            "cpu_utilization_avg": round((start_data["cpu_before"] + cpu_after) / 2, 2),
            "memory_used_mb": round((memory_after.used - start_data["memory_before"].used) / (1024 * 1024), 2),
            "memory_peak_mb": round(memory_after.used / (1024 * 1024), 2),
            "disk_read_mb": round((disk_io_after.read_bytes - start_data["disk_io_before"].read_bytes) / (1024 * 1024), 2),
            "disk_write_mb": round((disk_io_after.write_bytes - start_data["disk_io_before"].write_bytes) / (1024 * 1024), 2)
        }
    
    def record_metrics(self, metrics: Dict):
        """
        Record metrics to history
        """
        self.metrics_history.append({
            "timestamp": time.time(),
            "metrics": metrics
        })
    
    def get_metrics_history(self) -> List[Dict]:
        """
        Get metrics history
        """
        return self.metrics_history
    
    def clear_history(self):
        """
        Clear metrics history
        """
        self.metrics_history = []
