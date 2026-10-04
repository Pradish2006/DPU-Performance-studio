import React from 'react'
import { AlertTriangle, Zap, TrendingUp } from 'lucide-react'
import './BottleneckAnalysis.css'

function BottleneckAnalysis({ bottlenecks, cpuBaseline }) {
  const allBottlenecks = [
    ...bottlenecks.cpu_bottlenecks,
    ...bottlenecks.stage_bottlenecks,
    ...bottlenecks.resource_bottlenecks
  ]

  return (
    <div className="bottleneck-analysis">
      <h2>Bottleneck Analysis</h2>
      
      <div className="bottleneck-summary">
        <div className="summary-item">
          <AlertTriangle className="summary-icon" size={24} />
          <div>
            <h3>Primary Bottleneck</h3>
            <p>{bottlenecks.primary_bottleneck.description}</p>
          </div>
        </div>
        
        <div className="summary-item">
          <TrendingUp className="summary-icon" size={24} />
          <div>
            <h3>Potential Improvement</h3>
            <p>{bottlenecks.potential_improvement.improvement_percentage}% faster with optimization</p>
          </div>
        </div>
      </div>

      {allBottlenecks.length > 0 ? (
        <div className="bottleneck-list">
          <h3>Detected Bottlenecks</h3>
          {allBottlenecks.map((bottleneck, idx) => (
            <div key={idx} className={`bottleneck-item ${bottleneck.severity?.toLowerCase() || 'medium'}`}>
              <div className="bottleneck-header">
                <div className="bottleneck-type">
                  <Zap size={20} />
                  <span>{bottleneck.type.replace(/_/g, ' ')}</span>
                </div>
                {bottleneck.severity && (
                  <span className={`severity-badge ${bottleneck.severity.toLowerCase()}`}>
                    {bottleneck.severity}
                  </span>
                )}
              </div>
              
              <div className="bottleneck-content">
                {bottleneck.stage && (
                  <p className="bottleneck-stage">
                    <strong>Stage:</strong> {bottleneck.stage.replace(/_/g, ' ')}
                  </p>
                )}
                <p className="bottleneck-description">{bottleneck.description}</p>
                
                {bottleneck.current_latency_ms && (
                  <div className="bottleneck-metrics">
                    <span className="metric">Current: {bottleneck.current_latency_ms}ms</span>
                    {bottleneck.estimated_dpu_latency_ms && (
                      <span className="metric">DPU Est: {bottleneck.estimated_dpu_latency_ms}ms</span>
                    )}
                    {bottleneck.speedup_potential && (
                      <span className="metric highlight">Speedup: {bottleneck.speedup_potential}x</span>
                    )}
                  </div>
                )}
                
                {bottleneck.recommendation && (
                  <div className="bottleneck-recommendation">
                    <strong>Recommendation:</strong> {bottleneck.recommendation.replace(/_/g, ' ')}
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="no-bottlenecks">
          <p>No significant bottlenecks detected. The workload is well-optimized.</p>
        </div>
      )}

      <div className="recommendations-section">
        <h3>Recommendations</h3>
        <ul>
          {bottlenecks.recommendations.map((rec, idx) => (
            <li key={idx}>{rec}</li>
          ))}
        </ul>
      </div>
    </div>
  )
}

export default BottleneckAnalysis
