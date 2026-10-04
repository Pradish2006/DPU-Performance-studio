import React from 'react'
import './StageBreakdown.css'

function StageBreakdown({ cpuBaseline, optimizedResults }) {
  const stages = Object.keys(cpuBaseline.stages)

  return (
    <div className="stage-breakdown">
      <h2>Stage-by-Stage Execution Analysis</h2>
      
      <div className="stage-list">
        {stages.map((stage, idx) => {
          const cpuStage = cpuBaseline.stages[stage]
          const optimizedStage = optimizedResults.stages[stage]
          const speedup = optimizedStage ? (cpuStage.latency_ms / optimizedStage.latency_ms).toFixed(2) : '1.00'
          const improvement = optimizedStage ? ((cpuStage.latency_ms - optimizedStage.latency_ms) / cpuStage.latency_ms * 100).toFixed(1) : '0.0'
          
          return (
            <div key={stage} className="stage-item">
              <div className="stage-header">
                <h3>{stage.replace(/_/g, ' ').toUpperCase()}</h3>
                <span className={`stage-badge ${!optimizedStage || optimizedStage.execution_location === 'CPU' ? 'cpu' : 
                                              optimizedStage.execution_location === 'DPU_SIMULATED' ? 'dpu' : 'custom'}`}>
                  {!optimizedStage || optimizedStage.execution_location === 'CPU' ? 'CPU' : 
                   optimizedStage.execution_location === 'DPU_SIMULATED' ? 'DPU' : 'CUSTOM'}
                </span>
              </div>
              
              <div className="stage-metrics">
                <div className="stage-metric">
                  <span className="metric-label">CPU Latency</span>
                  <span className="metric-value">{cpuStage.latency_ms}ms</span>
                </div>
                <div className="stage-metric">
                  <span className="metric-label">Optimized Latency</span>
                  <span className="metric-value">{optimizedStage ? optimizedStage.latency_ms : cpuStage.latency_ms}ms</span>
                </div>
                <div className="stage-metric">
                  <span className="metric-label">Speedup</span>
                  <span className="metric-value improvement">{speedup}x</span>
                </div>
                <div className="stage-metric">
                  <span className="metric-label">Improvement</span>
                  <span className="metric-value improvement">{improvement}%</span>
                </div>
              </div>

              {optimizedStage && optimizedStage.execution_location && optimizedStage.execution_location !== 'CPU' && (
                <div className="stage-details">
                  <div className="detail-item">
                    <span className="detail-label">CPU Utilization:</span>
                    <span className="detail-value">{optimizedStage.cpu_utilization_percent || 0}%</span>
                  </div>
                  <div className="detail-item">
                    <span className="detail-label">DPU Utilization:</span>
                    <span className="detail-value">{optimizedStage.dpu_utilization_percent || 0}%</span>
                  </div>
                  {optimizedStage.transfer_time_ms > 0 && (
                    <div className="detail-item">
                      <span className="detail-label">Transfer Time:</span>
                      <span className="detail-value">{optimizedStage.transfer_time_ms}ms</span>
                    </div>
                  )}
                  {optimizedStage.sync_time_ms > 0 && (
                    <div className="detail-item">
                      <span className="detail-label">Sync Time:</span>
                      <span className="detail-value">{optimizedStage.sync_time_ms}ms</span>
                    </div>
                  )}
                  <div className="detail-item">
                    <span className="detail-label">Confidence:</span>
                    <span className="detail-value">{(optimizedStage.confidence * 100).toFixed(0)}%</span>
                  </div>
                </div>
              )}
            </div>
          )
        })}
      </div>
    </div>
  )
}

export default StageBreakdown
