import React from 'react'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import './MetricsComparison.css'

function MetricsComparison({ cpuBaseline, dpuSimulation, optimizedResults, comparison }) {
  const data = [
    {
      name: 'CPU Baseline',
      latency: cpuBaseline.total_latency_ms,
      throughput: cpuBaseline.throughput_samples_per_sec,
      cpuUtil: cpuBaseline.avg_cpu_utilization_percent
    },
    {
      name: 'DPU Simulated',
      latency: dpuSimulation.total_latency_ms,
      throughput: dpuSimulation.throughput_samples_per_sec,
      cpuUtil: 30  // Simulated lower CPU utilization
    },
    {
      name: 'Optimized',
      latency: optimizedResults.total_latency_ms,
      throughput: optimizedResults.throughput_samples_per_sec,
      cpuUtil: comparison.resource_comparison.cpu_utilization.optimized
    }
  ]

  return (
    <div className="metrics-comparison">
      <h2>Performance Metrics Comparison</h2>
      
      <div className="metrics-grid">
        <div className="metric-box">
          <h3>Latency (ms)</h3>
          <div className="metric-chart">
            <ResponsiveContainer width="100%" height={200}>
              <BarChart data={data}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="latency" fill="#1a365d" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="metric-box">
          <h3>Throughput (samples/sec)</h3>
          <div className="metric-chart">
            <ResponsiveContainer width="100%" height={200}>
              <BarChart data={data}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="throughput" fill="#3182ce" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="metric-box">
          <h3>CPU Utilization (%)</h3>
          <div className="metric-chart">
            <ResponsiveContainer width="100%" height={200}>
              <BarChart data={data}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="cpuUtil" fill="#38a169" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      <div className="metrics-table">
        <table>
          <thead>
            <tr>
              <th>Metric</th>
              <th>CPU Baseline</th>
              <th>DPU Simulated</th>
              <th>Optimized</th>
              <th>Improvement</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>Total Latency</td>
              <td>{cpuBaseline.total_latency_ms}ms</td>
              <td>{dpuSimulation.total_latency_ms}ms</td>
              <td>{optimizedResults.total_latency_ms}ms</td>
              <td className="improvement">-{comparison.summary.latency_reduction_ms}ms</td>
            </tr>
            <tr>
              <td>Throughput</td>
              <td>{cpuBaseline.throughput_samples_per_sec.toFixed(2)}</td>
              <td>{dpuSimulation.throughput_samples_per_sec.toFixed(2)}</td>
              <td>{optimizedResults.throughput_samples_per_sec.toFixed(2)}</td>
              <td className="improvement">+{comparison.summary.speedup}x</td>
            </tr>
            <tr>
              <td>CPU Utilization</td>
              <td>{cpuBaseline.avg_cpu_utilization_percent}%</td>
              <td>30% (sim)</td>
              <td>{comparison.resource_comparison.cpu_utilization.optimized}%</td>
              <td className="improvement">{comparison.resource_comparison.cpu_utilization.change_percentage}%</td>
            </tr>
            <tr>
              <td>Transfer Time</td>
              <td>0ms</td>
              <td>{dpuSimulation.total_transfer_time_ms}ms</td>
              <td>{optimizedResults.total_transfer_time_ms}ms</td>
              <td>-</td>
            </tr>
            <tr>
              <td>Sync Time</td>
              <td>0ms</td>
              <td>{dpuSimulation.total_sync_time_ms}ms</td>
              <td>{optimizedResults.total_sync_time_ms}ms</td>
              <td>-</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  )
}

export default MetricsComparison
