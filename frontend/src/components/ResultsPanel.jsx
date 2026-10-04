import React from 'react'
import { ArrowLeft, TrendingUp, Cpu, Zap, AlertTriangle, CheckCircle, Clock, Activity, Download } from 'lucide-react'
import './ResultsPanel.css'
import MetricsComparison from './MetricsComparison'
import StageBreakdown from './StageBreakdown'
import BottleneckAnalysis from './BottleneckAnalysis'
import PlacementDecisions from './PlacementDecisions'
import ConfidenceBar from './ConfidenceBar'

function ResultsPanel({ results, onReset }) {
  const { cpu_baseline, dpu_simulation, bottlenecks, placement_decision, optimized_results, comparison } = results

  const downloadReport = async (format = 'markdown') => {
    try {
      const endpoint = format === 'markdown' ? '/api/report/markdown' : '/api/report/json'
      const response = await fetch(`http://localhost:8000${endpoint}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(results)
      })

      if (response.ok) {
        const content = await response.text()
        const blob = new Blob([content], { type: format === 'markdown' ? 'text/markdown' : 'application/json' })
        const url = URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = `dpu-performance-report.${format === 'markdown' ? 'md' : 'json'}`
        document.body.appendChild(a)
        a.click()
        document.body.removeChild(a)
        URL.revokeObjectURL(url)
      }
    } catch (error) {
      console.error('Failed to download report:', error)
      alert('Failed to download report')
    }
  }

  return (
    <div className="results-panel">
      <div className="results-header">
        <button onClick={onReset} className="back-button">
          <ArrowLeft size={20} />
          Back to Upload
        </button>
        <h1>Analysis Results</h1>
        <p className="subtitle">Complete performance analysis and optimization recommendations</p>
        <div className="header-actions">
          <button onClick={() => downloadReport('markdown')} className="download-button">
            <Download size={18} />
            Download Markdown Report
          </button>
          <button onClick={() => downloadReport('json')} className="download-button secondary">
            <Download size={18} />
            Download JSON Report
          </button>
        </div>
      </div>

      <div className="results-grid">
        {/* Summary Cards */}
        <div className="summary-section">
          <div className="summary-card primary">
            <div className="card-icon">
              <TrendingUp size={32} />
            </div>
            <div className="card-content">
              <h3>Performance Improvement</h3>
              <div className="metric-value">
                {comparison.summary.speedup}x
              </div>
              <p className="metric-label">Speedup Achieved</p>
            </div>
          </div>

          <div className="summary-card">
            <div className="card-icon">
              <Clock size={32} />
            </div>
            <div className="card-content">
              <h3>Latency Reduction</h3>
              <div className="metric-value">
                {comparison.summary.latency_reduction_ms}ms
              </div>
              <p className="metric-label">
                {cpu_baseline.total_latency_ms}ms → {optimized_results.total_latency_ms}ms
              </p>
            </div>
          </div>

          <div className="summary-card">
            <div className="card-icon">
              <Cpu size={32} />
            </div>
            <div className="card-content">
              <h3>Operations Optimized</h3>
              <div className="metric-value">
                {placement_decision.summary.dpu_stages + placement_decision.summary.custom_kernel_stages}
              </div>
              <p className="metric-label">
                {placement_decision.summary.dpu_stages} DPU + {placement_decision.summary.custom_kernel_stages} Custom
              </p>
            </div>
          </div>

          <div className="summary-card">
            <div className="card-icon">
              <Activity size={32} />
            </div>
            <div className="card-content">
              <h3>Confidence Score</h3>
              <div className="metric-value">
                {Math.round(comparison.assessment.verdict === 'EXCELLENT' ? 95 : 
                            comparison.assessment.verdict === 'GOOD' ? 80 : 60)}%
              </div>
              <p className="metric-label">Analysis Confidence</p>
            </div>
          </div>
        </div>

        {/* Metrics Comparison */}
        <div className="panel-section">
          <MetricsComparison
            cpuBaseline={cpu_baseline}
            dpuSimulation={dpu_simulation}
            optimizedResults={optimized_results}
            comparison={comparison}
          />
        </div>

        {/* Stage Breakdown */}
        <div className="panel-section">
          <StageBreakdown
            cpuBaseline={cpu_baseline}
            optimizedResults={optimized_results}
          />
        </div>

        {/* Bottleneck Analysis */}
        <div className="panel-section">
          <BottleneckAnalysis
            bottlenecks={bottlenecks}
            cpuBaseline={cpu_baseline}
          />
        </div>

        {/* Placement Decisions */}
        <div className="panel-section">
          <PlacementDecisions
            placementDecision={placement_decision}
          />
        </div>

        {/* Confidence Bar */}
        <div className="panel-section">
          <ConfidenceBar
            results={results}
          />
        </div>

        {/* Final Assessment */}
        <div className="panel-section">
          <div className="assessment-card">
            <div className="assessment-header">
              <div className={`assessment-icon ${comparison.assessment.verdict.toLowerCase()}`}>
                {comparison.assessment.verdict === 'EXCELLENT' && <CheckCircle size={32} />}
                {comparison.assessment.verdict === 'GOOD' && <CheckCircle size={32} />}
                {comparison.assessment.verdict === 'MODERATE' && <AlertTriangle size={32} />}
                {comparison.assessment.verdict === 'MINIMAL' && <AlertTriangle size={32} />}
              </div>
              <div>
                <h3>Overall Assessment</h3>
                <p className={`assessment-verdict ${comparison.assessment.verdict.toLowerCase()}`}>
                  {comparison.assessment.verdict}
                </p>
              </div>
            </div>
            <p className="assessment-message">{comparison.assessment.message}</p>
            <div className="recommendations">
              <h4>Recommendations:</h4>
              <ul>
                {comparison.recommendations.map((rec, idx) => (
                  <li key={idx}>{rec}</li>
                ))}
              </ul>
            </div>
          </div>
        </div>

        {/* Data Source Notice */}
        <div className="panel-section">
          <div className="notice-card">
            <AlertTriangle size={24} className="notice-icon" />
            <div className="notice-content">
              <h4>Data Source Notice</h4>
              <p>
                <strong>CPU Results:</strong> Actual measured values from CPU baseline execution.<br />
                <strong>DPU Results:</strong> Simulated/emulated values. Real DPU measurements require hardware.<br />
                <strong>Custom Kernel:</strong> Future real-DPU implementation. Performance is estimated.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default ResultsPanel
