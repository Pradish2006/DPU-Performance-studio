import React from 'react'
import { CheckCircle, AlertCircle, HelpCircle } from 'lucide-react'
import './ConfidenceBar.css'

function ConfidenceBar({ results }) {
  const { cpu_baseline, dpu_simulation, optimized_results, comparison } = results

  // Calculate overall confidence based on data sources
  const cpuConfidence = 95  // CPU measurements are actual, high confidence
  const dpuConfidence = 80  // DPU is simulated, medium confidence
  const customConfidence = 70  // Custom kernel is future/estimated, lower confidence
  
  const overallConfidence = Math.round(
    (cpuConfidence * 0.4 + dpuConfidence * 0.4 + customConfidence * 0.2)
  )

  const confidenceLevels = [
    {
      name: 'CPU Measurements',
      confidence: cpuConfidence,
      icon: <CheckCircle size={20} />,
      description: 'Actual measured values from CPU baseline execution',
      color: '#38a169'
    },
    {
      name: 'DPU Simulation',
      confidence: dpuConfidence,
      icon: <AlertCircle size={20} />,
      description: 'Simulated/emulated values. Real DPU requires hardware.',
      color: '#3182ce'
    },
    {
      name: 'Custom Kernel Estimates',
      confidence: customConfidence,
      icon: <HelpCircle size={20} />,
      description: 'Future real-DPU implementation. Performance is estimated.',
      color: '#dd6b20'
    }
  ]

  const getConfidenceLabel = (confidence) => {
    if (confidence >= 90) return 'High'
    if (confidence >= 70) return 'Medium'
    return 'Low'
  }

  const getConfidenceColor = (confidence) => {
    if (confidence >= 90) return '#38a169'
    if (confidence >= 70) return '#3182ce'
    return '#dd6b20'
  }

  return (
    <div className="confidence-bar">
      <h2>Measurement Confidence</h2>
      
      <div className="overall-confidence">
        <div className="overall-header">
          <h3>Overall Confidence Score</h3>
          <div className={`overall-score ${getConfidenceLabel(overallConfidence).toLowerCase()}`}>
            {overallConfidence}%
          </div>
        </div>
        <div className="overall-bar">
          <div 
            className="overall-fill"
            style={{ 
              width: `${overallConfidence}%`,
              background: getConfidenceColor(overallConfidence)
            }}
          ></div>
        </div>
        <p className="overall-description">
          This score reflects the reliability of the performance measurements and recommendations.
          CPU measurements are actual, while DPU and custom kernel values are simulated/estimated.
        </p>
      </div>

      <div className="confidence-breakdown">
        <h3>Confidence Breakdown by Data Source</h3>
        
        {confidenceLevels.map((level, idx) => (
          <div key={idx} className="confidence-item">
            <div className="confidence-item-header">
              <div className="confidence-icon" style={{ color: level.color }}>
                {level.icon}
              </div>
              <div className="confidence-info">
                <h4>{level.name}</h4>
                <span className={`confidence-badge ${getConfidenceLabel(level.confidence).toLowerCase()}`}>
                  {getConfidenceLabel(level.confidence)} Confidence
                </span>
              </div>
              <div className="confidence-percentage">
                {level.confidence}%
              </div>
            </div>
            
            <div className="confidence-progress">
              <div 
                className="confidence-fill"
                style={{ 
                  width: `${level.confidence}%`,
                  background: level.color
                }}
              ></div>
            </div>
            
            <p className="confidence-description">{level.description}</p>
          </div>
        ))}
      </div>

      <div className="confidence-legend">
        <h4>Confidence Levels</h4>
        <div className="legend-items">
          <div className="legend-item">
            <div className="legend-color high"></div>
            <span>High (90-100%): Actual measurements, highly reliable</span>
          </div>
          <div className="legend-item">
            <div className="legend-color medium"></div>
            <span>Medium (70-89%): Simulated values, reasonably reliable</span>
          </div>
          <div className="legend-item">
            <div className="legend-color low"></div>
            <span>Low (0-69%): Estimated values, requires verification</span>
          </div>
        </div>
      </div>
    </div>
  )
}

export default ConfidenceBar
