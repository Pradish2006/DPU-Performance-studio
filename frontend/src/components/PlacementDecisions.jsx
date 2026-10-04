import React from 'react'
import { Cpu, Zap, Code } from 'lucide-react'
import './PlacementDecisions.css'

function PlacementDecisions({ placementDecision }) {
  const { placements, summary, decision_logic } = placementDecision

  return (
    <div className="placement-decisions">
      <h2>Operation Placement Decisions</h2>
      
      <div className="placement-summary">
        <div className="summary-stat">
          <div className="stat-value">{summary.cpu_stages}</div>
          <div className="stat-label">CPU Stages</div>
          <div className="stat-bar" style={{ width: `${summary.distribution.cpu_percent}%`, background: '#718096' }}></div>
        </div>
        
        <div className="summary-stat">
          <div className="stat-value">{summary.dpu_stages}</div>
          <div className="stat-label">DPU Stages</div>
          <div className="stat-bar" style={{ width: `${summary.distribution.dpu_percent}%`, background: '#3182ce' }}></div>
        </div>
        
        <div className="summary-stat">
          <div className="stat-value">{summary.custom_kernel_stages}</div>
          <div className="stat-label">Custom Kernel</div>
          <div className="stat-bar" style={{ width: `${summary.distribution.custom_percent}%`, background: '#dd6b20' }}></div>
        </div>
      </div>

      <div className="placement-list">
        {Object.entries(placements).map(([stage, decision]) => (
          <div key={stage} className={`placement-item ${decision.location.toLowerCase()}`}>
            <div className="placement-header">
              <h3>{stage.replace(/_/g, ' ').toUpperCase()}</h3>
              <div className={`location-badge ${decision.location.toLowerCase()}`}>
                {decision.location === 'CPU' && <Cpu size={16} />}
                {decision.location === 'DPU' && <Zap size={16} />}
                {decision.location === 'CUSTOM_KERNEL' && <Code size={16} />}
                <span>{decision.location.replace(/_/g, ' ')}</span>
              </div>
            </div>
            
            <div className="placement-reason">
              <strong>Reason:</strong> {decision.reason}
            </div>
            
            <div className="placement-metrics">
              <div className="metric-row">
                <span className="metric-label">CPU Latency:</span>
                <span className="metric-value">{decision.estimated_cpu_latency_ms}ms</span>
              </div>
              <div className="metric-row">
                <span className="metric-label">Optimized Latency:</span>
                <span className="metric-value">
                  {decision.location === 'CPU' 
                    ? decision.estimated_cpu_latency_ms 
                    : decision.estimated_dpu_latency_ms || decision.estimated_custom_latency_ms}ms
                </span>
              </div>
              <div className="metric-row">
                <span className="metric-label">Confidence:</span>
                <span className="metric-value">{(decision.confidence * 100).toFixed(0)}%</span>
              </div>
            </div>

            {decision.note && (
              <div className="placement-note">
                <strong>Note:</strong> {decision.note}
              </div>
            )}
          </div>
        ))}
      </div>

      <div className="expected-performance">
        <h3>Expected Performance</h3>
        <div className="performance-grid">
          <div className="performance-item">
            <span className="performance-label">Estimated Total Latency:</span>
            <span className="performance-value">{summary.estimated_total_latency_ms}ms</span>
          </div>
          <div className="performance-item">
            <span className="performance-label">Estimated Speedup:</span>
            <span className="performance-value improvement">{summary.estimated_speedup}x</span>
          </div>
          <div className="performance-item">
            <span className="performance-label">Improvement:</span>
            <span className="performance-value improvement">{summary.improvement_percentage}%</span>
          </div>
        </div>
      </div>
    </div>
  )
}

export default PlacementDecisions
